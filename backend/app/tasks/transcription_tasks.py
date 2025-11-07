"""
書き起こしタスク

Celery ワーカーで実行される非同期処理
"""
import logging
import os
import time
from datetime import datetime

from .celery_app import celery_app
from ..services.whisper_service import whisper_service
from ..services.audio_preprocessing import audio_preprocessor
from ..services.output_formatter import output_formatter
from ..core.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="process_transcription")
def process_transcription(
    self,
    transcription_id: str,
    audio_path: str,
    session_log: str = None
):
    """
    書き起こし処理タスク

    Args:
        transcription_id: 書き起こしID
        audio_path: 音声ファイルパス（RAMディスク内）
        session_log: セッションログ

    Returns:
        処理結果辞書
    """
    logger.info(f"Starting transcription task: {transcription_id}")
    start_time = time.time()

    try:
        # ステータス更新: 処理中
        self.update_state(
            state="PROCESSING",
            meta={
                "transcription_id": transcription_id,
                "status": "processing",
                "progress": 0
            }
        )

        # 1. 音声前処理
        logger.info("Step 1/4: Audio preprocessing")
        self.update_state(
            state="PROCESSING",
            meta={
                "transcription_id": transcription_id,
                "status": "preprocessing",
                "progress": 25
            }
        )

        preprocessed_path = audio_preprocessor.preprocess(
            audio_path,
            apply_noise_reduction=True,
            normalize_audio=True
        )

        audio_duration = audio_preprocessor.get_audio_duration(preprocessed_path)
        logger.info(f"Audio duration: {audio_duration:.2f} seconds")

        # 2. Whisper書き起こし
        logger.info("Step 2/4: Whisper transcription")
        self.update_state(
            state="PROCESSING",
            meta={
                "transcription_id": transcription_id,
                "status": "transcribing",
                "progress": 50
            }
        )

        segments, full_text = whisper_service.transcribe(
            preprocessed_path,
            language="ja",
            task="transcribe"
        )

        # 3. 出力生成
        logger.info("Step 3/4: Generating outputs")
        self.update_state(
            state="PROCESSING",
            meta={
                "transcription_id": transcription_id,
                "status": "formatting",
                "progress": 75
            }
        )

        mixed_output = output_formatter.generate_mixed_output(
            segments,
            session_log=session_log
        )

        # 4. クリーンアップ
        logger.info("Step 4/4: Cleanup")
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
            if os.path.exists(preprocessed_path) and preprocessed_path != audio_path:
                os.remove(preprocessed_path)
            logger.info("Temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Failed to cleanup temporary files: {e}")

        # GPU メモリクリーンアップ
        whisper_service.cleanup()

        processing_time = time.time() - start_time
        logger.info(
            f"Transcription completed: {transcription_id} "
            f"in {processing_time:.2f} seconds"
        )

        # 結果を返す
        return {
            "transcription_id": transcription_id,
            "status": "completed",
            "segments": [
                {
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text,
                    "confidence": seg.confidence
                }
                for seg in segments
            ],
            "full_text": full_text,
            "mixed_output": mixed_output,
            "audio_duration": audio_duration,
            "processing_time": processing_time,
            "completed_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Transcription task failed: {e}", exc_info=True)

        # クリーンアップ（エラー時も実行）
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
        except:
            pass

        # エラー情報を返す
        return {
            "transcription_id": transcription_id,
            "status": "failed",
            "error_message": str(e),
            "processing_time": time.time() - start_time
        }
