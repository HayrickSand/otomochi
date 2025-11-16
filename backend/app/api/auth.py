"""
認証 API エンドポイント
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated, Optional

from ..schemas.auth import LoginRequest, LoginResponse, OAuthRequest, OAuthResponse
from ..schemas.user import UserResponse
from ..services.supabase_auth import supabase_auth
from ..core.config import settings
from ..models.user import User

router = APIRouter()
security = HTTPBearer()


async def get_current_user_from_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> User:
    """
    トークンから現在のユーザーを取得（依存性注入用）

    Args:
        credentials: Bearer トークン

    Returns:
        ユーザー情報

    Raises:
        HTTPException: 認証失敗時
    """
    token = credentials.credentials
    user = await supabase_auth.get_user_from_token(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return user


@router.post("/signup", response_model=LoginResponse)
async def signup(request: LoginRequest):
    """
    メール・パスワードで新規登録

    Supabase Auth を使用した新規ユーザー登録
    """
    try:
        result = await supabase_auth.sign_up_with_email(
            request.email,
            request.password
        )

        return LoginResponse(
            access_token=result["access_token"],
            token_type="bearer",
            user_id=result["user"].id,
            email=result["user"].email,
            display_name=None
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Sign up failed: {str(e)}"
        )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    メール・パスワードでログイン

    Supabase Auth を使用した認証
    """
    try:
        result = await supabase_auth.sign_in_with_email(
            request.email,
            request.password
        )

        return LoginResponse(
            access_token=result["access_token"],
            token_type="bearer",
            user_id=result["user"].id,
            email=result["user"].email,
            display_name=result["user"].user_metadata.get("display_name")
        )

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


@router.post("/oauth", response_model=OAuthResponse)
async def oauth_login(request: OAuthRequest):
    """
    OAuth プロバイダーでログイン

    Google または Twitter OAuth を使用した認証
    サポートされているプロバイダー: google, twitter
    """
    if request.provider not in ["google", "twitter"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported OAuth provider. Supported: google, twitter"
        )

    try:
        result = await supabase_auth.sign_in_with_oauth(request.provider)

        return OAuthResponse(
            provider=result["provider"],
            url=result["url"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"OAuth login failed: {str(e)}"
        )


@router.get("/callback")
async def oauth_callback(
    access_token: str = Query(...),
    refresh_token: str = Query(...)
):
    """
    OAuth コールバック

    OAuth プロバイダーからのリダイレクト先
    """
    # フロントエンドにトークンを渡すためリダイレクト
    redirect_url = f"{settings.ALLOWED_ORIGINS[0]}/auth/callback?access_token={access_token}&refresh_token={refresh_token}"

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=redirect_url)


@router.post("/logout")
async def logout(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    """
    ログアウト

    Supabase セッションを無効化
    """
    try:
        token = credentials.credentials
        await supabase_auth.sign_out(token)
        return {"message": "Logged out successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Logout failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: Annotated[User, Depends(get_current_user_from_token)]
):
    """
    現在のユーザー情報を取得

    Bearer トークンから認証されたユーザー情報を返す
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        avatar_url=current_user.avatar_url,
        plan=current_user.plan,
        is_admin=current_user.is_admin
    )


@router.post("/verify-token")
async def verify_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    """
    トークンの有効性を検証
    """
    token = credentials.credentials
    is_valid = await supabase_auth.verify_token(token)

    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return {"valid": True}
