"""
使用量記録モデル
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UsageRecord(BaseModel):
    """使用量記録"""
    id: str
    user_id: str
    transcription_id: str

    # 使用量
    audio_duration: float  # 処理した音声長（秒）
    processing_time: float  # 処理時間（秒）

    # 課金情報
    plan_type: str  # 使用したプラン
    is_oneshot: bool = False  # ワンショット課金かどうか
    charge_amount: Optional[int] = None  # 課金額（円）

    # RunPod コスト
    gpu_usage_time: float  # GPU使用時間（秒）
    estimated_cost: float  # 推定コスト（USD）

    # タイムスタンプ
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "transcription_id": "550e8400-e29b-41d4-a716-446655440001",
                "audio_duration": 7200.0,
                "processing_time": 900.0,
                "plan_type": "lite",
                "is_oneshot": False,
                "charge_amount": None,
                "gpu_usage_time": 900.0,
                "estimated_cost": 0.5
            }
        }
