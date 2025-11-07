"""
管理者 API エンドポイント
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List

from ..schemas.admin import AdminStatsResponse, AdminUserResponse
from ..core.config import settings

router = APIRouter()


# TODO: 管理者権限チェック依存性を実装
async def require_admin() -> str:
    """管理者権限チェック（仮実装）"""
    return "admin_123"


@router.get("/stats", response_model=AdminStatsResponse)
async def get_admin_stats(admin_id: str = Depends(require_admin)):
    """
    管理者統計を取得

    - 総ユーザー数、アクティブユーザー数
    - 総書き起こし数、処理時間
    - 月次収益・コスト
    - プラン別統計
    - GPU使用統計
    """
    # TODO: データベースから集計
    raise HTTPException(
        status_code=501,
        detail="Admin stats is not yet implemented"
    )


@router.get("/users", response_model=List[AdminUserResponse])
async def get_all_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    admin_id: str = Depends(require_admin)
):
    """
    全ユーザー一覧を取得
    """
    # TODO: データベースから取得
    raise HTTPException(
        status_code=501,
        detail="Get all users is not yet implemented"
    )


@router.get("/users/{user_id}", response_model=AdminUserResponse)
async def get_user_details(
    user_id: str,
    admin_id: str = Depends(require_admin)
):
    """
    特定ユーザーの詳細を取得
    """
    # TODO: データベースから取得
    raise HTTPException(
        status_code=501,
        detail="Get user details is not yet implemented"
    )


@router.get("/revenue/export")
async def export_revenue_csv(
    year: int = Query(..., ge=2024),
    month: int = Query(..., ge=1, le=12),
    admin_id: str = Depends(require_admin)
):
    """
    収益データをCSV形式でエクスポート（確定申告用）

    月次の収益・コストデータをCSV形式で出力します。
    """
    # TODO: CSV生成
    raise HTTPException(
        status_code=501,
        detail="Revenue export is not yet implemented"
    )
