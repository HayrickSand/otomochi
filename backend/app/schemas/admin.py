"""
管理者関連スキーマ
"""
from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr
from ..models.user import PlanType


class AdminUserResponse(BaseModel):
    """管理者用ユーザー情報"""
    id: str
    email: EmailStr
    display_name: str | None
    plan_type: PlanType
    sessions_used: int
    hours_used: float
    sessions_limit: int
    hours_limit: float
    created_at: datetime
    last_transcription_at: datetime | None


class MonthlyRevenue(BaseModel):
    """月次収益"""
    month: str  # YYYY-MM
    total_revenue: int  # 円
    total_cost: float  # USD
    user_count: int
    transcription_count: int


class PlanStats(BaseModel):
    """プラン別統計"""
    plan_type: PlanType
    user_count: int
    total_revenue: int


class AdminStatsResponse(BaseModel):
    """管理者統計レスポンス"""
    total_users: int
    active_users: int  # 今月アクティブなユーザー数
    total_transcriptions: int
    total_hours_processed: float

    # 今月の統計
    monthly_revenue: int  # 円
    monthly_cost: float  # USD
    monthly_profit: float  # USD（収益 - コスト）

    # プラン別統計
    plan_stats: List[PlanStats]

    # GPU統計
    average_processing_ratio: float  # 平均処理速度比
    total_gpu_hours: float

    # 月次推移
    monthly_history: List[MonthlyRevenue]
