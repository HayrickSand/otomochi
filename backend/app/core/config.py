"""
アプリケーション設定モジュール
環境変数から設定を読み込み、型安全なアクセスを提供
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """アプリケーション設定"""

    # アプリケーション基本設定
    APP_NAME: str = "otomochi"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API設定
    API_PREFIX: str = "/api"

    # CORS設定
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:80"
    ]

    # Supabase設定
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str = ""

    # JWT設定
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24時間

    # Redis設定
    REDIS_URL: str = "redis://redis:6379/0"

    # RunPod設定
    RUNPOD_API_KEY: str = ""

    # Whisper設定
    WHISPER_MODEL: str = "large-v3-turbo"
    WHISPER_DEVICE: str = "cuda"
    WHISPER_COMPUTE_TYPE: str = "float16"
    WHISPER_BEAM_SIZE: int = 5
    WHISPER_PATIENCE: float = 0.2
    WHISPER_TEMPERATURE: List[float] = [0.0, 0.2, 0.4]
    WHISPER_VAD_FILTER: bool = True
    WHISPER_CONDITION_ON_PREVIOUS_TEXT: bool = True

    # ファイル設定
    MAX_UPLOAD_SIZE: int = 500 * 1024 * 1024  # 500MB
    RAMDISK_PATH: str = "/tmp/ramdisk"
    ALLOWED_AUDIO_FORMATS: List[str] = ["mp3", "wav", "m4a", "flac"]

    # 課金プラン設定（円）
    FREE_PLAN_SESSIONS: int = 3
    FREE_PLAN_HOURS: float = 0.25  # 5分

    LITE_PLAN_PRICE: int = 680
    LITE_PLAN_SESSIONS: int = 3
    LITE_PLAN_HOURS: float = 9.0

    STANDARD_PLAN_PRICE: int = 1200
    STANDARD_PLAN_SESSIONS: int = 5
    STANDARD_PLAN_HOURS: float = 15.0

    UNLIMITED_PLAN_PRICE: int = 4000

    ONESHOT_PRICE_PER_HOUR: int = 120

    # 処理目標
    TARGET_PROCESSING_RATIO: float = 0.083  # 3時間を15分で処理 = 15/180

    class Config:
        env_file = ".env"
        case_sensitive = True


# グローバル設定インスタンス
settings = Settings()
