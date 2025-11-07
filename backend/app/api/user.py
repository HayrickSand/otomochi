"""
ユーザー API エンドポイント
"""
from fastapi import APIRouter, HTTPException, Depends

from ..schemas.user import UserResponse, UserUpdateRequest, PlanUpdateRequest
from ..core.config import settings

router = APIRouter()


# TODO: 認証依存性を実装
async def get_current_user_id() -> str:
    """現在のユーザーIDを取得（仮実装）"""
    return "user_123"


@router.get("/me", response_model=UserResponse)
async def get_my_profile(user_id: str = Depends(get_current_user_id)):
    """
    自分のプロフィールを取得
    """
    # TODO: データベースから取得
    raise HTTPException(
        status_code=501,
        detail="Get user profile is not yet implemented"
    )


@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    request: UserUpdateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    自分のプロフィールを更新
    """
    # TODO: データベース更新
    raise HTTPException(
        status_code=501,
        detail="Update user profile is not yet implemented"
    )


@router.get("/me/usage")
async def get_my_usage(user_id: str = Depends(get_current_user_id)):
    """
    自分の使用量を取得
    """
    # TODO: 使用量集計
    raise HTTPException(
        status_code=501,
        detail="Get usage is not yet implemented"
    )


@router.post("/me/plan", response_model=UserResponse)
async def update_my_plan(
    request: PlanUpdateRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    プランを変更
    """
    # TODO: プラン変更処理
    # TODO: 課金処理との連携
    raise HTTPException(
        status_code=501,
        detail="Update plan is not yet implemented"
    )
