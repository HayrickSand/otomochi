"""
書き起こし関連スキーマ
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
from ..models.transcription import TranscriptionStatus, TranscriptSegment


class DownloadFormat(str, Enum):
    """ダウンロード形式"""
    TXT = "txt"
    JSON = "json"
    HTML = "html"


class TranscriptionCreateRequest(BaseModel):
    """書き起こし作成リクエスト"""
    session_log: Optional[str] = None  # セッションログ（ユーザーメモ）


class TranscriptionResponse(BaseModel):
    """書き起こしレスポンス"""
    id: str
    status: TranscriptionStatus
    audio_filename: str
    audio_duration: Optional[float] = None
    audio_size: int
    full_text: Optional[str] = None
    segments: List[TranscriptSegment] = []
    session_log: Optional[str] = None
    mixed_output: Optional[str] = None
    processing_time: Optional[float] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class TranscriptionListResponse(BaseModel):
    """書き起こしリストレスポンス"""
    transcriptions: List[TranscriptionResponse]
    total: int
    page: int
    page_size: int
