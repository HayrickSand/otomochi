"""
書き起こしジョブモデル定義
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class TranscriptionStatus(str, Enum):
    """書き起こしステータス"""
    PENDING = "pending"  # 待機中
    PROCESSING = "processing"  # 処理中
    COMPLETED = "completed"  # 完了
    FAILED = "failed"  # 失敗
    CANCELLED = "cancelled"  # キャンセル


class TranscriptSegment(BaseModel):
    """書き起こしセグメント（タイムスタンプ付き）"""
    start: float  # 開始時刻（秒）
    end: float  # 終了時刻（秒）
    text: str  # 書き起こしテキスト
    confidence: Optional[float] = None  # 信頼度


class Transcription(BaseModel):
    """書き起こしジョブ"""
    id: str
    user_id: str
    status: TranscriptionStatus
    audio_filename: str
    audio_duration: Optional[float] = None  # 音声長（秒）
    audio_size: int  # ファイルサイズ（バイト）

    # 処理結果
    segments: List[TranscriptSegment] = []
    full_text: Optional[str] = None
    language: str = "ja"

    # セッションログ（ユーザーが入力したメモなど）
    session_log: Optional[str] = None

    # ミックス出力（セッションログ + 書き起こし結果の統合）
    mixed_output: Optional[str] = None

    # メタデータ
    whisper_model: str = "large-v3-turbo"
    processing_time: Optional[float] = None  # 処理時間（秒）
    error_message: Optional[str] = None

    # タイムスタンプ
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "completed",
                "audio_filename": "session_2024_01_15.mp3",
                "audio_duration": 7200.0,
                "audio_size": 144000000,
                "full_text": "これはTRPGセッションの書き起こし例です...",
                "language": "ja",
                "whisper_model": "large-v3-turbo",
                "processing_time": 900.0
            }
        }
