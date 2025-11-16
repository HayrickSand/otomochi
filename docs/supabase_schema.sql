-- otomochi Supabase データベーススキーマ
-- TRPG専用音声書き起こしサービス

-- ユーザープロフィール拡張テーブル
CREATE TABLE IF NOT EXISTS public.user_profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    display_name TEXT,
    avatar_url TEXT,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ユーザー課金プラン
CREATE TABLE IF NOT EXISTS public.user_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    plan_type TEXT NOT NULL CHECK (plan_type IN ('free', 'lite', 'standard', 'unlimited')),
    sessions_limit INTEGER NOT NULL,
    hours_limit NUMERIC(10, 2) NOT NULL,
    sessions_used INTEGER DEFAULT 0,
    hours_used NUMERIC(10, 2) DEFAULT 0,
    billing_cycle_start TIMESTAMP WITH TIME ZONE NOT NULL,
    billing_cycle_end TIMESTAMP WITH TIME ZONE NOT NULL,
    auto_renew BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- 書き起こしジョブ
CREATE TABLE IF NOT EXISTS public.transcriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'cancelled')),

    -- 音声ファイル情報
    audio_filename TEXT NOT NULL,
    audio_duration NUMERIC(10, 2),
    audio_size BIGINT NOT NULL,

    -- 書き起こし結果
    full_text TEXT,
    segments JSONB,
    language TEXT DEFAULT 'ja',

    -- セッションログ
    session_log TEXT,
    mixed_output TEXT,

    -- メタデータ
    whisper_model TEXT DEFAULT 'large-v3-turbo',
    processing_time NUMERIC(10, 2),
    error_message TEXT,

    -- タイムスタンプ
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    will_be_deleted_at TIMESTAMP WITH TIME ZONE,

    -- インデックス用
    INDEX idx_transcriptions_user_id (user_id),
    INDEX idx_transcriptions_status (status),
    INDEX idx_transcriptions_created_at (created_at DESC),
    INDEX idx_transcriptions_will_be_deleted_at (will_be_deleted_at)
);

-- 使用量記録
CREATE TABLE IF NOT EXISTS public.usage_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    transcription_id UUID REFERENCES public.transcriptions(id) ON DELETE CASCADE,

    -- 使用量
    audio_duration NUMERIC(10, 2) NOT NULL,
    processing_time NUMERIC(10, 2) NOT NULL,

    -- 課金情報
    plan_type TEXT NOT NULL,
    is_oneshot BOOLEAN DEFAULT FALSE,
    charge_amount INTEGER,

    -- RunPod コスト
    gpu_usage_time NUMERIC(10, 2) NOT NULL,
    estimated_cost NUMERIC(10, 4) NOT NULL,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    INDEX idx_usage_records_user_id (user_id),
    INDEX idx_usage_records_created_at (created_at DESC)
);

-- Stripe 顧客情報
CREATE TABLE IF NOT EXISTS public.stripe_customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE,
    stripe_customer_id TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    INDEX idx_stripe_customers_user_id (user_id),
    INDEX idx_stripe_customers_stripe_id (stripe_customer_id)
);

-- Stripe サブスクリプション
CREATE TABLE IF NOT EXISTS public.stripe_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    stripe_subscription_id TEXT NOT NULL UNIQUE,
    stripe_customer_id TEXT NOT NULL,
    plan_type TEXT NOT NULL,
    status TEXT NOT NULL,
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    INDEX idx_stripe_subscriptions_user_id (user_id),
    INDEX idx_stripe_subscriptions_stripe_id (stripe_subscription_id),
    INDEX idx_stripe_subscriptions_status (status)
);

-- Row Level Security (RLS) 設定

-- user_profiles
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "ユーザーは自分のプロフィールを閲覧可能"
    ON public.user_profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "ユーザーは自分のプロフィールを更新可能"
    ON public.user_profiles FOR UPDATE
    USING (auth.uid() = id);

-- user_plans
ALTER TABLE public.user_plans ENABLE ROW LEVEL SECURITY;

CREATE POLICY "ユーザーは自分のプランを閲覧可能"
    ON public.user_plans FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "管理者はすべてのプランを閲覧可能"
    ON public.user_plans FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE id = auth.uid() AND is_admin = TRUE
        )
    );

-- transcriptions
ALTER TABLE public.transcriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "ユーザーは自分の書き起こしを閲覧可能"
    ON public.transcriptions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "ユーザーは自分の書き起こしを作成可能"
    ON public.transcriptions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "ユーザーは自分の書き起こしを更新可能"
    ON public.transcriptions FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "ユーザーは自分の書き起こしを削除可能"
    ON public.transcriptions FOR DELETE
    USING (auth.uid() = user_id);

-- usage_records
ALTER TABLE public.usage_records ENABLE ROW LEVEL SECURITY;

CREATE POLICY "ユーザーは自分の使用量を閲覧可能"
    ON public.usage_records FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "管理者はすべての使用量を閲覧可能"
    ON public.usage_records FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE id = auth.uid() AND is_admin = TRUE
        )
    );

-- stripe_customers
ALTER TABLE public.stripe_customers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "ユーザーは自分のStripe顧客情報を閲覧可能"
    ON public.stripe_customers FOR SELECT
    USING (auth.uid() = user_id);

-- stripe_subscriptions
ALTER TABLE public.stripe_subscriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "ユーザーは自分のサブスクリプションを閲覧可能"
    ON public.stripe_subscriptions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "管理者はすべてのサブスクリプションを閲覧可能"
    ON public.stripe_subscriptions FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE id = auth.uid() AND is_admin = TRUE
        )
    );

-- 関数: 新規ユーザー登録時の初期データ作成
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    -- ユーザープロフィール作成
    INSERT INTO public.user_profiles (id, display_name)
    VALUES (NEW.id, NEW.email);

    -- 無料プラン作成
    INSERT INTO public.user_plans (
        user_id,
        plan_type,
        sessions_limit,
        hours_limit,
        billing_cycle_start,
        billing_cycle_end
    ) VALUES (
        NEW.id,
        'free',
        3,
        0.25,
        NOW(),
        NOW() + INTERVAL '1 month'
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- トリガー: 新規ユーザー登録時
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 関数: 月次使用量リセット
CREATE OR REPLACE FUNCTION public.reset_monthly_usage()
RETURNS void AS $$
BEGIN
    UPDATE public.user_plans
    SET
        sessions_used = 0,
        hours_used = 0,
        billing_cycle_start = billing_cycle_end,
        billing_cycle_end = billing_cycle_end + INTERVAL '1 month',
        updated_at = NOW()
    WHERE billing_cycle_end <= NOW();
END;
$$ LANGUAGE plpgsql;

-- 関数: 使用量記録を作成し、プラン使用量を更新
CREATE OR REPLACE FUNCTION public.record_usage(
    p_user_id UUID,
    p_transcription_id UUID,
    p_audio_duration NUMERIC,
    p_processing_time NUMERIC,
    p_gpu_usage_time NUMERIC,
    p_estimated_cost NUMERIC
)
RETURNS void AS $$
DECLARE
    v_plan_type TEXT;
    v_is_oneshot BOOLEAN;
    v_charge_amount INTEGER;
BEGIN
    -- 現在のプランタイプを取得
    SELECT plan_type INTO v_plan_type
    FROM public.user_plans
    WHERE user_id = p_user_id;

    -- ワンショット課金かどうか判定（使用量超過の場合）
    v_is_oneshot := FALSE;
    v_charge_amount := NULL;

    -- 使用量記録作成
    INSERT INTO public.usage_records (
        user_id,
        transcription_id,
        audio_duration,
        processing_time,
        plan_type,
        is_oneshot,
        charge_amount,
        gpu_usage_time,
        estimated_cost
    ) VALUES (
        p_user_id,
        p_transcription_id,
        p_audio_duration,
        p_processing_time,
        v_plan_type,
        v_is_oneshot,
        v_charge_amount,
        p_gpu_usage_time,
        p_estimated_cost
    );

    -- プラン使用量更新
    UPDATE public.user_plans
    SET
        sessions_used = sessions_used + 1,
        hours_used = hours_used + (p_audio_duration / 3600),
        updated_at = NOW()
    WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- インデックス作成
CREATE INDEX IF NOT EXISTS idx_user_plans_user_id ON public.user_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_transcriptions_user_status ON public.transcriptions(user_id, status);
CREATE INDEX IF NOT EXISTS idx_usage_records_user_created ON public.usage_records(user_id, created_at DESC);

-- コメント
COMMENT ON TABLE public.user_profiles IS 'ユーザープロフィール拡張情報';
COMMENT ON TABLE public.user_plans IS 'ユーザー課金プラン情報';
COMMENT ON TABLE public.transcriptions IS '書き起こしジョブ';
COMMENT ON TABLE public.usage_records IS '使用量記録（課金・統計用）';
COMMENT ON TABLE public.stripe_customers IS 'Stripe顧客情報（Stripe Customer ID管理）';
COMMENT ON TABLE public.stripe_subscriptions IS 'Stripeサブスクリプション情報';
COMMENT ON COLUMN public.transcriptions.will_be_deleted_at IS '削除予定日時（完了から8時間後、プライバシー保護）';
