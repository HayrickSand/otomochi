"""
認証関連スキーマ
"""
from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """ログインリクエスト"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """ログインレスポンス"""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    display_name: Optional[str] = None


class OAuthRequest(BaseModel):
    """OAuth ログインリクエスト"""
    provider: str  # 'google' or 'twitter'


class OAuthResponse(BaseModel):
    """OAuth ログインレスポンス"""
    provider: str
    url: str  # OAuth 認証URL


class TokenData(BaseModel):
    """JWTトークンデータ"""
    user_id: str
    email: str
    exp: int
