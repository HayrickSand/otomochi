"""
データクリーンアップタスク

プライバシー保護のため、8時間経過した書き起こしデータを自動削除
"""
import logging
from datetime import datetime, timedelta
from typing import List
import os

from .celery_app import celery_app
from ..core.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.cleanup_tasks.cleanup_old_transcriptions")
def cleanup_old_transcriptions():
    """
    8時間以上経過した書き起こしデータを削除

    プライバシー保護のため、完了後8時間経過したデータは自動削除されます。
    - データベースの transcription レコード削除
    - 関連する usage_records も削除
    """
    try:
        from supabase import create_client

        # Supabase クライアント
        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

        # 8時間前の時刻を計算
        cutoff_time = datetime.utcnow() - timedelta(hours=8)
        cutoff_time_str = cutoff_time.isoformat()

        logger.info(f"Starting cleanup for transcriptions completed before {cutoff_time_str}")

        # 削除対象のtranscriptionを取得
        response = client.table("transcriptions").select("id, audio_filename, user_id").lte(
            "completed_at", cutoff_time_str
        ).eq("status", "completed").execute()

        if not response.data:
            logger.info("No transcriptions to cleanup")
            return {
                "status": "success",
                "deleted_count": 0,
                "message": "No transcriptions to cleanup"
            }

        transcription_ids = [t["id"] for t in response.data]
        deleted_count = len(transcription_ids)

        logger.info(f"Found {deleted_count} transcriptions to delete")

        # usage_records を先に削除（外部キー制約）
        for trans_id in transcription_ids:
            try:
                client.table("usage_records").delete().eq("transcription_id", trans_id).execute()
            except Exception as e:
                logger.warning(f"Failed to delete usage_records for {trans_id}: {e}")

        # transcriptions を削除
        for trans_id in transcription_ids:
            try:
                client.table("transcriptions").delete().eq("id", trans_id).execute()
                logger.info(f"Deleted transcription: {trans_id}")
            except Exception as e:
                logger.error(f"Failed to delete transcription {trans_id}: {e}")

        logger.info(f"Cleanup completed: {deleted_count} transcriptions deleted")

        return {
            "status": "success",
            "deleted_count": deleted_count,
            "cutoff_time": cutoff_time_str
        }

    except Exception as e:
        logger.error(f"Cleanup task failed: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }


@celery_app.task(name="app.tasks.cleanup_tasks.cleanup_failed_transcriptions")
def cleanup_failed_transcriptions():
    """
    失敗したtranscriptionを24時間後に削除

    エラーで失敗したジョブも一定時間後に削除してデータベースをクリーンに保ちます
    """
    try:
        from supabase import create_client

        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

        # 24時間前の時刻を計算
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        cutoff_time_str = cutoff_time.isoformat()

        logger.info(f"Cleaning up failed transcriptions before {cutoff_time_str}")

        # 失敗したtranscriptionを削除
        response = client.table("transcriptions").delete().lte(
            "created_at", cutoff_time_str
        ).eq("status", "failed").execute()

        deleted_count = len(response.data) if response.data else 0

        logger.info(f"Deleted {deleted_count} failed transcriptions")

        return {
            "status": "success",
            "deleted_count": deleted_count
        }

    except Exception as e:
        logger.error(f"Failed transcriptions cleanup failed: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }


def get_deletion_time(completed_at: datetime) -> datetime:
    """
    削除予定時刻を計算

    Args:
        completed_at: 完了日時

    Returns:
        削除予定日時（完了から8時間後）
    """
    return completed_at + timedelta(hours=8)


def time_until_deletion(completed_at: datetime) -> timedelta:
    """
    削除までの残り時間を計算

    Args:
        completed_at: 完了日時

    Returns:
        削除までの残り時間
    """
    deletion_time = get_deletion_time(completed_at)
    now = datetime.utcnow()
    remaining = deletion_time - now

    # マイナスの場合は0を返す
    if remaining.total_seconds() < 0:
        return timedelta(0)

    return remaining


def format_time_remaining(remaining: timedelta) -> str:
    """
    残り時間を人間が読みやすい形式にフォーマット

    Args:
        remaining: 残り時間

    Returns:
        フォーマット済み文字列
    """
    total_seconds = int(remaining.total_seconds())

    if total_seconds <= 0:
        return "まもなく削除されます"

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours > 0:
        return f"あと{hours}時間{minutes}分"
    else:
        return f"あと{minutes}分"
