"""
課金・決済 API エンドポイント
"""
from fastapi import APIRouter, HTTPException, Depends, Request, Header
from typing import Annotated, Optional

from ..schemas.billing import (
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    PortalSessionResponse,
    SubscriptionResponse,
    WebhookEvent
)
from ..services.stripe_service import stripe_service
from ..services.supabase_auth import supabase_auth
from ..api.auth import get_current_user_from_token
from ..models.user import User, PlanType
from ..core.config import settings

router = APIRouter()


@router.post("/checkout", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    request: CheckoutSessionRequest,
    current_user: Annotated[User, Depends(get_current_user_from_token)]
):
    """
    Stripe Checkout セッションを作成

    プラン購入のためのStripe Checkoutページへのリダイレクト用URLを生成
    """
    try:
        # Stripe Customer がない場合は作成
        # TODO: user_profiles テーブルに stripe_customer_id を保存
        customer = await stripe_service.create_customer(
            email=current_user.email,
            name=current_user.display_name,
            metadata={"user_id": current_user.id}
        )

        # Checkout セッション作成
        session = await stripe_service.create_checkout_session(
            customer_id=customer.id,
            plan_type=request.plan_type,
            success_url=f"{settings.ALLOWED_ORIGINS[0]}/billing/success",
            cancel_url=f"{settings.ALLOWED_ORIGINS[0]}/billing/cancel"
        )

        return CheckoutSessionResponse(
            session_id=session.id,
            url=session.url
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create checkout session: {str(e)}")


@router.post("/portal", response_model=PortalSessionResponse)
async def create_portal_session(
    current_user: Annotated[User, Depends(get_current_user_from_token)]
):
    """
    Stripe Customer Portal セッションを作成

    顧客が自分でサブスクリプションを管理できるポータルへのリンクを生成
    """
    try:
        # TODO: user_profiles テーブルから stripe_customer_id を取得
        # 仮実装：新規作成
        customer = await stripe_service.create_customer(
            email=current_user.email,
            name=current_user.display_name,
            metadata={"user_id": current_user.id}
        )

        session = await stripe_service.create_portal_session(
            customer_id=customer.id,
            return_url=f"{settings.ALLOWED_ORIGINS[0]}/profile"
        )

        return PortalSessionResponse(url=session.url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create portal session: {str(e)}")


@router.post("/oneshot", response_model=CheckoutSessionResponse)
async def create_oneshot_payment(
    hours: float,
    current_user: Annotated[User, Depends(get_current_user_from_token)]
):
    """
    ワンショット課金セッションを作成

    Args:
        hours: 購入する時間数
    """
    try:
        # 金額計算
        amount = int(hours * settings.ONESHOT_PRICE_PER_HOUR)

        # Stripe Customer がない場合は作成
        customer = await stripe_service.create_customer(
            email=current_user.email,
            name=current_user.display_name,
            metadata={"user_id": current_user.id}
        )

        # ワンタイム決済セッション作成
        session = await stripe_service.create_one_time_payment(
            customer_id=customer.id,
            amount=amount,
            description=f"{hours}時間分のワンショット課金",
            success_url=f"{settings.ALLOWED_ORIGINS[0]}/billing/success",
            cancel_url=f"{settings.ALLOWED_ORIGINS[0]}/billing/cancel"
        )

        return CheckoutSessionResponse(
            session_id=session.id,
            url=session.url
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create oneshot payment: {str(e)}")


@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: Annotated[User, Depends(get_current_user_from_token)],
    subscription_id: str,
    at_period_end: bool = True
):
    """
    サブスクリプションをキャンセル

    Args:
        subscription_id: Subscription ID
        at_period_end: 期間終了時にキャンセルするか
    """
    try:
        subscription = await stripe_service.cancel_subscription(
            subscription_id,
            at_period_end
        )

        return {
            "message": "Subscription cancelled successfully",
            "subscription_id": subscription.id,
            "cancel_at": subscription.cancel_at if hasattr(subscription, 'cancel_at') else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel subscription: {str(e)}")


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: Annotated[str, Header(alias="stripe-signature")]
):
    """
    Stripe Webhook ハンドラー

    Stripe からのイベント通知を受け取り、処理する
    """
    try:
        # リクエストボディを取得
        payload = await request.body()

        # Webhook イベントを構築・検証
        event = await stripe_service.construct_webhook_event(
            payload,
            stripe_signature
        )

        # イベントタイプに応じて処理
        event_type = event["type"]

        if event_type == "checkout.session.completed":
            # チェックアウト完了
            await handle_checkout_completed(event)

        elif event_type == "customer.subscription.created":
            # サブスクリプション作成
            await handle_subscription_created(event)

        elif event_type == "customer.subscription.updated":
            # サブスクリプション更新
            await handle_subscription_updated(event)

        elif event_type == "customer.subscription.deleted":
            # サブスクリプション削除
            await handle_subscription_deleted(event)

        elif event_type == "invoice.payment_succeeded":
            # 支払い成功
            await handle_payment_succeeded(event)

        elif event_type == "invoice.payment_failed":
            # 支払い失敗
            await handle_payment_failed(event)

        return {"status": "success"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook error: {str(e)}")


# Webhook イベントハンドラー

async def handle_checkout_completed(event):
    """チェックアウト完了時の処理"""
    session = event["data"]["object"]
    customer_id = session.get("customer")
    metadata = session.get("metadata", {})

    # TODO: user_profiles を更新（stripe_customer_id を保存）
    # TODO: plan_type に応じて user_plans を更新

    print(f"Checkout completed: {session['id']}, customer: {customer_id}")


async def handle_subscription_created(event):
    """サブスクリプション作成時の処理"""
    subscription = event["data"]["object"]
    customer_id = subscription.get("customer")

    # TODO: user_plans を更新（サブスクリプション開始）

    print(f"Subscription created: {subscription['id']}, customer: {customer_id}")


async def handle_subscription_updated(event):
    """サブスクリプション更新時の処理"""
    subscription = event["data"]["object"]

    # TODO: user_plans を更新（プラン変更など）

    print(f"Subscription updated: {subscription['id']}")


async def handle_subscription_deleted(event):
    """サブスクリプション削除時の処理"""
    subscription = event["data"]["object"]
    customer_id = subscription.get("customer")

    # TODO: user_plans を更新（無料プランに戻す）

    print(f"Subscription deleted: {subscription['id']}, customer: {customer_id}")


async def handle_payment_succeeded(event):
    """支払い成功時の処理"""
    invoice = event["data"]["object"]

    # TODO: 支払い記録を保存

    print(f"Payment succeeded: {invoice['id']}")


async def handle_payment_failed(event):
    """支払い失敗時の処理"""
    invoice = event["data"]["object"]

    # TODO: ユーザーに通知

    print(f"Payment failed: {invoice['id']}")


@router.get("/config")
async def get_stripe_config():
    """
    Stripe 公開可能キーを取得

    フロントエンドでStripe.jsを初期化するために使用
    """
    return {
        "publishable_key": settings.STRIPE_PUBLISHABLE_KEY
    }
