"""
Supabase 認証サービス

Supabase Auth を使用した認証処理を提供
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from supabase import create_client, Client
from jose import JWTError, jwt

from ..core.config import settings
from ..models.user import User, UserPlan, PlanType

logger = logging.getLogger(__name__)


class SupabaseAuthService:
    """Supabase 認証サービス"""

    def __init__(self):
        """Supabase クライアントを初期化"""
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.admin_client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_KEY
        ) if settings.SUPABASE_SERVICE_KEY else None

    async def sign_up_with_email(self, email: str, password: str) -> Dict[str, Any]:
        """
        メール・パスワードで新規登録

        Args:
            email: メールアドレス
            password: パスワード

        Returns:
            認証情報（ユーザー、セッション、アクセストークン）
        """
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })

            if response.user:
                logger.info(f"User signed up: {email}")
                return {
                    "user": response.user,
                    "session": response.session,
                    "access_token": response.session.access_token if response.session else None
                }
            else:
                raise Exception("Sign up failed")

        except Exception as e:
            logger.error(f"Sign up error: {e}")
            raise

    async def sign_in_with_email(self, email: str, password: str) -> Dict[str, Any]:
        """
        メール・パスワードでログイン

        Args:
            email: メールアドレス
            password: パスワード

        Returns:
            認証情報
        """
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if response.user:
                logger.info(f"User signed in: {email}")
                return {
                    "user": response.user,
                    "session": response.session,
                    "access_token": response.session.access_token if response.session else None
                }
            else:
                raise Exception("Sign in failed")

        except Exception as e:
            logger.error(f"Sign in error: {e}")
            raise

    async def sign_in_with_oauth(self, provider: str) -> Dict[str, str]:
        """
        OAuth プロバイダーでログイン

        Args:
            provider: プロバイダー名 ('google', 'twitter' など)

        Returns:
            OAuth URL
        """
        try:
            response = self.client.auth.sign_in_with_oauth({
                "provider": provider,
                "options": {
                    "redirect_to": f"{settings.ALLOWED_ORIGINS[0]}/auth/callback"
                }
            })

            return {
                "provider": provider,
                "url": response.url
            }

        except Exception as e:
            logger.error(f"OAuth sign in error: {e}")
            raise

    async def sign_out(self, access_token: str) -> bool:
        """
        ログアウト

        Args:
            access_token: アクセストークン

        Returns:
            成功フラグ
        """
        try:
            # トークンを設定
            self.client.auth.set_session(access_token, "")
            self.client.auth.sign_out()
            logger.info("User signed out")
            return True

        except Exception as e:
            logger.error(f"Sign out error: {e}")
            return False

    async def get_user_from_token(self, access_token: str) -> Optional[User]:
        """
        アクセストークンからユーザー情報を取得

        Args:
            access_token: アクセストークン

        Returns:
            ユーザー情報
        """
        try:
            # Supabase JWT を検証
            user_response = self.client.auth.get_user(access_token)

            if not user_response.user:
                return None

            supabase_user = user_response.user

            # データベースからプロフィールとプラン情報を取得
            profile_response = self.client.table("user_profiles").select("*").eq("id", supabase_user.id).single().execute()
            plan_response = self.client.table("user_plans").select("*").eq("user_id", supabase_user.id).single().execute()

            if not plan_response.data:
                logger.warning(f"No plan found for user {supabase_user.id}")
                return None

            plan_data = plan_response.data
            profile_data = profile_response.data if profile_response.data else {}

            # User モデルに変換
            user = User(
                id=supabase_user.id,
                email=supabase_user.email,
                display_name=profile_data.get("display_name"),
                avatar_url=profile_data.get("avatar_url"),
                plan=UserPlan(
                    plan_type=PlanType(plan_data["plan_type"]),
                    sessions_limit=plan_data["sessions_limit"],
                    hours_limit=plan_data["hours_limit"],
                    sessions_used=plan_data["sessions_used"],
                    hours_used=plan_data["hours_used"],
                    billing_cycle_start=plan_data["billing_cycle_start"],
                    billing_cycle_end=plan_data["billing_cycle_end"],
                    auto_renew=plan_data["auto_renew"]
                ),
                is_admin=profile_data.get("is_admin", False),
                created_at=profile_data.get("created_at", datetime.now()),
                updated_at=profile_data.get("updated_at", datetime.now())
            )

            return user

        except Exception as e:
            logger.error(f"Get user from token error: {e}")
            return None

    async def verify_token(self, access_token: str) -> bool:
        """
        トークンの有効性を検証

        Args:
            access_token: アクセストークン

        Returns:
            有効フラグ
        """
        try:
            user = await self.get_user_from_token(access_token)
            return user is not None

        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return False

    async def update_user_profile(self, user_id: str, display_name: Optional[str] = None) -> bool:
        """
        ユーザープロフィールを更新

        Args:
            user_id: ユーザーID
            display_name: 表示名

        Returns:
            成功フラグ
        """
        try:
            update_data = {"updated_at": datetime.now().isoformat()}
            if display_name is not None:
                update_data["display_name"] = display_name

            self.client.table("user_profiles").update(update_data).eq("id", user_id).execute()

            logger.info(f"User profile updated: {user_id}")
            return True

        except Exception as e:
            logger.error(f"Update user profile error: {e}")
            return False

    async def update_user_plan(
        self,
        user_id: str,
        plan_type: PlanType,
        auto_renew: bool = True
    ) -> bool:
        """
        ユーザープランを更新

        Args:
            user_id: ユーザーID
            plan_type: プランタイプ
            auto_renew: 自動更新フラグ

        Returns:
            成功フラグ
        """
        try:
            # プラン制限を取得
            sessions_limit, hours_limit = self._get_plan_limits(plan_type)

            update_data = {
                "plan_type": plan_type.value,
                "sessions_limit": sessions_limit,
                "hours_limit": hours_limit,
                "auto_renew": auto_renew,
                "updated_at": datetime.now().isoformat()
            }

            self.client.table("user_plans").update(update_data).eq("user_id", user_id).execute()

            logger.info(f"User plan updated: {user_id} -> {plan_type}")
            return True

        except Exception as e:
            logger.error(f"Update user plan error: {e}")
            return False

    def _get_plan_limits(self, plan_type: PlanType) -> tuple[int, float]:
        """
        プランタイプから制限値を取得

        Args:
            plan_type: プランタイプ

        Returns:
            (セッション数制限, 時間制限)
        """
        limits = {
            PlanType.FREE: (settings.FREE_PLAN_SESSIONS, settings.FREE_PLAN_HOURS),
            PlanType.LITE: (settings.LITE_PLAN_SESSIONS, settings.LITE_PLAN_HOURS),
            PlanType.STANDARD: (settings.STANDARD_PLAN_SESSIONS, settings.STANDARD_PLAN_HOURS),
            PlanType.UNLIMITED: (-1, -1.0)  # 無制限
        }
        return limits.get(plan_type, (3, 0.25))


# シングルトンインスタンス
supabase_auth = SupabaseAuthService()
