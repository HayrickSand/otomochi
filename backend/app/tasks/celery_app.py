"""
Celery アプリケーション設定
非同期ジョブ処理用
"""
from celery import Celery
from ..core.config import settings

# Celery アプリケーション
celery_app = Celery(
    "otomochi",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.transcription_tasks"]
)

# Celery 設定
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Tokyo",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600 * 4,  # 4時間タイムアウト
    task_soft_time_limit=3600 * 3.5,  # 3.5時間でソフトタイムアウト
    worker_prefetch_multiplier=1,  # GPU処理は1つずつ
    worker_max_tasks_per_child=10,  # メモリリーク対策
)
