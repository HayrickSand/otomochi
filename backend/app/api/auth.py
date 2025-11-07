"""
認証 API エンドポイント
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

from ..schemas.auth import LoginRequest, LoginResponse, TokenData
from ..core.config import settings

router = APIRouter()
security = HTTPBearer()


# TODO: Supabase Auth との統合を実装
@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    ログイン
    Supabase Auth を使用した認証
    """
    # TODO: Supabase Auth との統合
    raise HTTPException(
        status_code=501,
        detail="Supabase Auth integration is not yet implemented"
    )


@router.post("/signup", response_model=LoginResponse)
async def signup(request: LoginRequest):
    """
    新規登録
    """
    # TODO: Supabase Auth との統合
    raise HTTPException(
        status_code=501,
        detail="Supabase Auth integration is not yet implemented"
    )


@router.post("/logout")
async def logout(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    """
    ログアウト
    """
    # TODO: トークン無効化処理
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    """
    現在のユーザー情報を取得
    """
    # TODO: JWT トークンからユーザー情報を取得
    raise HTTPException(
        status_code=501,
        detail="Token validation is not yet implemented"
    )
