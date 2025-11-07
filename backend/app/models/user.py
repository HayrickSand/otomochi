"""
ユーザーモデル定義
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


class PlanType(str, Enum):
    """課金プランタイプ"""
    FREE = "free"
    LITE = "lite"
    STANDARD = "standard"
    UNLIMITED = "unlimited"


class UserPlan(BaseModel):
    """ユーザー課金プラン"""
    plan_type: PlanType
    sessions_limit: int  # 月間セッション数上限（無制限の場合は-1）
    hours_limit: float  # 月間時間上限（無制限の場合は-1）
    sessions_used: int = 0  # 今月の使用セッション数
    hours_used: float = 0.0  # 今月の使用時間
    billing_cycle_start: datetime
    billing_cycle_end: datetime
    auto_renew: bool = True


class User(BaseModel):
    """ユーザーモデル"""
    id: str  # Supabase Auth UID
    email: EmailStr
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    plan: UserPlan
    is_admin: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "display_name": "山田太郎",
                "plan": {
                    "plan_type": "lite",
                    "sessions_limit": 3,
                    "hours_limit": 9.0,
                    "sessions_used": 1,
                    "hours_used": 2.5,
                    "billing_cycle_start": "2024-01-01T00:00:00Z",
                    "billing_cycle_end": "2024-02-01T00:00:00Z",
                    "auto_renew": True
                },
                "is_admin": False
            }
        }
