"""
FastAPI メインアプリケーション
TRPG専用音声書き起こしサービス「otomochi」
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from .core.config import settings
from .api import auth, transcription, user, admin, billing

# ロギング設定
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI アプリケーション
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="TRPG専用音声書き起こしサービス",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS ミドルウェア
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# リクエスト処理時間ロギングミドルウェア
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """リクエスト処理時間をログに記録"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response


# エラーハンドラー
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """グローバル例外ハンドラー"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


# ヘルスチェック
@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# ルーター登録
app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["認証"])
app.include_router(transcription.router, prefix=f"{settings.API_PREFIX}/transcriptions", tags=["書き起こし"])
app.include_router(user.router, prefix=f"{settings.API_PREFIX}/users", tags=["ユーザー"])
app.include_router(admin.router, prefix=f"{settings.API_PREFIX}/admin", tags=["管理者"])
app.include_router(billing.router, prefix=f"{settings.API_PREFIX}/billing", tags=["課金・決済"])


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "otomochi API",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "disabled"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
