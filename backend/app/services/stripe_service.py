"""
Stripe 決済サービス

Stripe を使用した課金処理を提供
"""
import logging
from typing import Dict, Any, Optional
import stripe
from datetime import datetime, timedelta

from ..core.config import settings
from ..models.user import PlanType

logger = logging.getLogger(__name__)

# Stripe API キー設定
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Stripe 決済サービス"""

    # プラン価格マッピング（円）
    PLAN_PRICES = {
        PlanType.FREE: 0,
        PlanType.LITE: settings.LITE_PLAN_PRICE,
        PlanType.STANDARD: settings.STANDARD_PLAN_PRICE,
        PlanType.UNLIMITED: settings.UNLIMITED_PLAN_PRICE,
    }

    # Stripe Price ID（本番環境では実際のPrice IDに置き換える）
    STRIPE_PRICE_IDS = {
        PlanType.LITE: "price_lite_monthly",
        PlanType.STANDARD: "price_standard_monthly",
        PlanType.UNLIMITED: "price_unlimited_monthly",
    }

    async def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> stripe.Customer:
        """
        Stripe 顧客を作成

        Args:
            email: メールアドレス
            name: 顧客名
            metadata: メタデータ

        Returns:
            Stripe Customer オブジェクト
        """
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata or {}
            )
            logger.info(f"Stripe customer created: {customer.id}")
            return customer

        except Exception as e:
            logger.error(f"Failed to create Stripe customer: {e}")
            raise

    async def create_checkout_session(
        self,
        customer_id: str,
        plan_type: PlanType,
        success_url: str,
        cancel_url: str
    ) -> stripe.checkout.Session:
        """
        Stripe Checkout セッションを作成

        Args:
            customer_id: Stripe Customer ID
            plan_type: プランタイプ
            success_url: 成功時のリダイレクトURL
            cancel_url: キャンセル時のリダイレクトURL

        Returns:
            Stripe Checkout Session
        """
        try:
            if plan_type == PlanType.FREE:
                raise ValueError("Free plan does not require checkout")

            # Price IDを取得（本番では実際のStripe Price IDを使用）
            price_id = self.STRIPE_PRICE_IDS.get(plan_type)

            if not price_id:
                raise ValueError(f"Invalid plan type: {plan_type}")

            session = stripe.checkout.Session.create(
                customer=customer_id,
                mode="subscription",
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=cancel_url,
                metadata={
                    "plan_type": plan_type.value
                }
            )

            logger.info(f"Checkout session created: {session.id}")
            return session

        except Exception as e:
            logger.error(f"Failed to create checkout session: {e}")
            raise

    async def create_portal_session(
        self,
        customer_id: str,
        return_url: str
    ) -> stripe.billing_portal.Session:
        """
        Stripe Customer Portal セッションを作成

        顧客が自分でサブスクリプションを管理できるポータルへのリンクを生成

        Args:
            customer_id: Stripe Customer ID
            return_url: ポータルから戻るときのURL

        Returns:
            Stripe Portal Session
        """
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url
            )

            logger.info(f"Portal session created: {session.id}")
            return session

        except Exception as e:
            logger.error(f"Failed to create portal session: {e}")
            raise

    async def create_one_time_payment(
        self,
        customer_id: str,
        amount: int,
        description: str,
        success_url: str,
        cancel_url: str
    ) -> stripe.checkout.Session:
        """
        ワンタイム決済セッションを作成

        Args:
            customer_id: Stripe Customer ID
            amount: 金額（円）
            description: 説明
            success_url: 成功時のリダイレクトURL
            cancel_url: キャンセル時のリダイレクトURL

        Returns:
            Stripe Checkout Session
        """
        try:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                mode="payment",
                line_items=[
                    {
                        "price_data": {
                            "currency": "jpy",
                            "product_data": {
                                "name": "otomochi ワンショット課金",
                                "description": description,
                            },
                            "unit_amount": amount,
                        },
                        "quantity": 1,
                    }
                ],
                success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=cancel_url,
                metadata={
                    "payment_type": "oneshot"
                }
            )

            logger.info(f"One-time payment session created: {session.id}")
            return session

        except Exception as e:
            logger.error(f"Failed to create one-time payment: {e}")
            raise

    async def get_subscription(self, subscription_id: str) -> Optional[stripe.Subscription]:
        """
        サブスクリプション情報を取得

        Args:
            subscription_id: Subscription ID

        Returns:
            Stripe Subscription またはNone
        """
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return subscription

        except stripe.error.InvalidRequestError:
            return None
        except Exception as e:
            logger.error(f"Failed to get subscription: {e}")
            raise

    async def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True
    ) -> stripe.Subscription:
        """
        サブスクリプションをキャンセル

        Args:
            subscription_id: Subscription ID
            at_period_end: 期間終了時にキャンセルするか（True）、即座にキャンセルするか（False）

        Returns:
            Stripe Subscription
        """
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            else:
                subscription = stripe.Subscription.delete(subscription_id)

            logger.info(f"Subscription cancelled: {subscription_id}")
            return subscription

        except Exception as e:
            logger.error(f"Failed to cancel subscription: {e}")
            raise

    async def construct_webhook_event(
        self,
        payload: bytes,
        sig_header: str
    ) -> stripe.Event:
        """
        Webhook イベントを構築・検証

        Args:
            payload: リクエストボディ
            sig_header: Stripe-Signature ヘッダー

        Returns:
            Stripe Event

        Raises:
            ValueError: 署名検証失敗
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )

            logger.info(f"Webhook event received: {event['type']}")
            return event

        except ValueError as e:
            logger.error(f"Invalid webhook signature: {e}")
            raise
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            raise

    def get_plan_price(self, plan_type: PlanType) -> int:
        """
        プランタイプから価格を取得

        Args:
            plan_type: プランタイプ

        Returns:
            価格（円）
        """
        return self.PLAN_PRICES.get(plan_type, 0)


# シングルトンインスタンス
stripe_service = StripeService()
