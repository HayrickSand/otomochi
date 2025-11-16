"""
課金・決済関連スキーマ
"""
from typing import Optional
from pydantic import BaseModel
from ..models.user import PlanType


class CheckoutSessionRequest(BaseModel):
    """Checkout セッション作成リクエスト"""
    plan_type: PlanType


class CheckoutSessionResponse(BaseModel):
    """Checkout セッションレスポンス"""
    session_id: str
    url: str  # Stripe Checkout URL


class PortalSessionResponse(BaseModel):
    """Customer Portal セッションレスポンス"""
    url: str  # Stripe Portal URL


class SubscriptionResponse(BaseModel):
    """サブスクリプション情報"""
    subscription_id: str
    status: str
    plan_type: str
    current_period_start: int
    current_period_end: int
    cancel_at_period_end: bool


class WebhookEvent(BaseModel):
    """Webhook イベント"""
    type: str
    data: dict
