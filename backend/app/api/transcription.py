"""
書き起こし API エンドポイント
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Query
from fastapi.responses import FileResponse, Response
from typing import Annotated, Optional
import os

from ..schemas.transcription import (
    TranscriptionCreateRequest,
    TranscriptionResponse,
    TranscriptionListResponse,
    DownloadFormat
)
from ..core.config import settings

router = APIRouter()


# TODO: 認証依存性を実装
async def get_current_user_id() -> str:
    """現在のユーザーIDを取得（仮実装）"""
    return "user_123"


@router.post("/", response_model=TranscriptionResponse)
async def create_transcription(
    audio_file: UploadFile = File(...),
    session_log: Optional[str] = Form(None),
    user_id: str = Depends(get_current_user_id)
):
    """
    新規書き起こしジョブを作成

    音声ファイルをアップロードし、書き起こしジョブをキューに追加します。
    処理は非同期で実行され、ステータスは別途確認できます。
    """
    # ファイル形式チェック
    file_ext = audio_file.filename.split('.')[-1].lower()
    if file_ext not in settings.ALLOWED_AUDIO_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format. Allowed: {', '.join(settings.ALLOWED_AUDIO_FORMATS)}"
        )

    # ファイルサイズチェック
    audio_file.file.seek(0, os.SEEK_END)
    file_size = audio_file.file.tell()
    audio_file.file.seek(0)

    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size ({settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB)"
        )

    # TODO: ユーザーのプラン制限チェック
    # TODO: Celery タスクをキューに追加
    # TODO: Transcription レコード作成

    raise HTTPException(
        status_code=501,
        detail="Transcription creation is not yet implemented"
    )


@router.get("/", response_model=TranscriptionListResponse)
async def list_transcriptions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: str = Depends(get_current_user_id)
):
    """
    書き起こしジョブ一覧を取得
    """
    # TODO: データベースから取得
    raise HTTPException(
        status_code=501,
        detail="List transcriptions is not yet implemented"
    )


@router.get("/{transcription_id}", response_model=TranscriptionResponse)
async def get_transcription(
    transcription_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    書き起こしジョブの詳細を取得
    """
    # TODO: データベースから取得
    # TODO: ユーザー権限チェック
    raise HTTPException(
        status_code=501,
        detail="Get transcription is not yet implemented"
    )


@router.get("/{transcription_id}/download")
async def download_transcription(
    transcription_id: str,
    format: DownloadFormat = Query(DownloadFormat.TXT),
    user_id: str = Depends(get_current_user_id)
):
    """
    書き起こし結果をダウンロード

    対応形式：
    - txt: プレーンテキスト
    - json: JSON形式（タイムスタンプ付き）
    - html: HTML形式（読みやすい整形済み）
    """
    # TODO: ダウンロード機能実装
    raise HTTPException(
        status_code=501,
        detail="Download transcription is not yet implemented"
    )


@router.delete("/{transcription_id}")
async def delete_transcription(
    transcription_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    書き起こしジョブを削除
    """
    # TODO: 削除機能実装
    raise HTTPException(
        status_code=501,
        detail="Delete transcription is not yet implemented"
    )
