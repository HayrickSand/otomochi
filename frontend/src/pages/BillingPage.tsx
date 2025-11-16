import { useState } from 'react';
import { Link } from 'react-router-dom';
import { billingApi } from '../utils/api';
import type { User } from '../types';

interface BillingPageProps {
  user: User;
}

export default function BillingPage({ user }: BillingPageProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const plans = [
    {
      type: 'free',
      name: '無料',
      price: 0,
      sessions: 3,
      hours: 0.25,
      description: '試しに使ってみたい方向け',
    },
    {
      type: 'lite',
      name: 'ライト',
      price: 680,
      sessions: 3,
      hours: 9,
      description: '月に数回遊ぶ方向け',
    },
    {
      type: 'standard',
      name: 'スタンダード',
      price: 1200,
      sessions: 5,
      hours: 15,
      description: '定期的に遊ぶ方向け',
      recommended: true,
    },
    {
      type: 'unlimited',
      name: '無制限',
      price: 4000,
      sessions: -1,
      hours: -1,
      description: 'たくさん遊ぶ方向け',
    },
  ];

  const handleSubscribe = async (planType: string) => {
    if (planType === 'free') {
      setError('無料プランは選択できません');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const data = await billingApi.createCheckout(planType);
      // Stripe Checkout にリダイレクト
      window.location.href = data.url;
    } catch (err: any) {
      setError('決済ページの作成に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleManageBilling = async () => {
    setLoading(true);
    setError('');

    try {
      const data = await billingApi.createPortalSession();
      // Stripe Customer Portal にリダイレクト
      window.location.href = data.url;
    } catch (err: any) {
      setError('課金管理ページの作成に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-white shadow-sm mb-8">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <Link to="/dashboard" className="text-primary hover:underline">
            ← ダッシュボードに戻る
          </Link>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 pb-8">
        <h1 className="text-3xl font-bold mb-4">プラン変更</h1>
        <p className="text-gray-600 mb-8">
          現在のプラン: <span className="font-bold text-primary">{user.plan.plan_type.toUpperCase()}</span>
        </p>

        {error && (
          <div className="bg-red-100 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        <div className="grid md:grid-cols-4 gap-6 mb-12">
          {plans.map((plan) => (
            <div
              key={plan.type}
              className={`card relative ${
                plan.recommended ? 'border-2 border-primary' : ''
              }`}
            >
              {plan.recommended && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-primary text-white px-4 py-1 rounded-full text-sm">
                  おすすめ
                </div>
              )}

              <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
              <div className="text-3xl font-bold text-primary mb-4">
                ¥{plan.price.toLocaleString()}
                <span className="text-sm text-gray-600">/月</span>
              </div>

              <ul className="space-y-2 mb-6 text-sm text-gray-600">
                <li>
                  ✓ {plan.sessions === -1 ? '無制限' : `月${plan.sessions}セッション`}
                </li>
                <li>
                  ✓ {plan.hours === -1 ? '無制限' : `合計${plan.hours}時間`}
                </li>
                <li className="text-xs text-gray-500">{plan.description}</li>
              </ul>

              <button
                onClick={() => handleSubscribe(plan.type)}
                disabled={loading || user.plan.plan_type === plan.type}
                className={`btn-primary w-full ${
                  user.plan.plan_type === plan.type
                    ? 'opacity-50 cursor-not-allowed'
                    : ''
                }`}
              >
                {user.plan.plan_type === plan.type
                  ? '現在のプラン'
                  : plan.type === 'free'
                  ? '利用中'
                  : '選択'}
              </button>
            </div>
          ))}
        </div>

        <div className="card">
          <h2 className="text-xl font-bold mb-4">ワンショット課金</h2>
          <p className="text-gray-600 mb-4">
            プランの上限を超えた場合、追加で時間を購入できます。
          </p>
          <p className="text-2xl font-bold text-primary mb-4">
            ¥120 <span className="text-sm text-gray-600">/ 時間</span>
          </p>
          <p className="text-sm text-gray-600 mb-4">
            ※ ワンショット課金は書き起こし実行時に選択できます
          </p>
        </div>

        {user.plan.plan_type !== 'free' && (
          <div className="mt-8 text-center">
            <button
              onClick={handleManageBilling}
              disabled={loading}
              className="btn-secondary"
            >
              課金情報を管理
            </button>
            <p className="text-sm text-gray-600 mt-2">
              サブスクリプションのキャンセルや支払い方法の変更ができます
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
