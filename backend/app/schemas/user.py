"""
ユーザー関連スキーマ
"""
from typing import Optional
from pydantic import BaseModel, EmailStr
from ..models.user import UserPlan, PlanType


class UserResponse(BaseModel):
    """ユーザーレスポンス"""
    id: str
    email: EmailStr
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    plan: UserPlan
    is_admin: bool = False


class UserUpdateRequest(BaseModel):
    """ユーザー更新リクエスト"""
    display_name: Optional[str] = None


class PlanUpdateRequest(BaseModel):
    """プラン更新リクエスト"""
    plan_type: PlanType
    auto_renew: bool = True
