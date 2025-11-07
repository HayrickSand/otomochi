import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../utils/api';
import type { User } from '../types';

interface AdminPageProps {
  user: User;
}

interface AdminStats {
  total_users: number;
  active_users: number;
  total_transcriptions: number;
  total_hours_processed: number;
  monthly_revenue: number;
  monthly_cost: number;
  monthly_profit: number;
}

export default function AdminPage({ user }: AdminPageProps) {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await apiClient.get('/admin/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load admin stats:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-white shadow-sm mb-8">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary">🎲 otomochi - 管理者</h1>
          <Link to="/dashboard" className="btn-secondary">
            ダッシュボードに戻る
          </Link>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8">管理者ダッシュボード</h2>

        {loading ? (
          <div className="text-center py-8">読み込み中...</div>
        ) : stats ? (
          <div className="space-y-6">
            <div className="grid md:grid-cols-4 gap-4">
              <div className="card">
                <div className="text-sm text-gray-600">総ユーザー数</div>
                <div className="text-3xl font-bold text-primary">{stats.total_users}</div>
              </div>
              <div className="card">
                <div className="text-sm text-gray-600">アクティブユーザー</div>
                <div className="text-3xl font-bold text-primary">{stats.active_users}</div>
              </div>
              <div className="card">
                <div className="text-sm text-gray-600">総書き起こし数</div>
                <div className="text-3xl font-bold text-primary">{stats.total_transcriptions}</div>
              </div>
              <div className="card">
                <div className="text-sm text-gray-600">処理時間合計</div>
                <div className="text-3xl font-bold text-primary">
                  {stats.total_hours_processed.toFixed(1)}h
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-xl font-bold mb-4">今月の収益</h3>
              <div className="grid md:grid-cols-3 gap-4">
                <div>
                  <div className="text-sm text-gray-600">売上</div>
                  <div className="text-2xl font-bold text-green-600">
                    ¥{stats.monthly_revenue.toLocaleString()}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">コスト</div>
                  <div className="text-2xl font-bold text-red-600">
                    ${stats.monthly_cost.toFixed(2)}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">利益</div>
                  <div className="text-2xl font-bold text-primary">
                    ${stats.monthly_profit.toFixed(2)}
                  </div>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold">データエクスポート</h3>
              </div>
              <div className="space-y-2">
                <button className="btn-primary w-full">
                  収益データをCSVでエクスポート
                </button>
                <button className="btn-secondary w-full">
                  ユーザーリストをエクスポート
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-red-600">
            データの読み込みに失敗しました
          </div>
        )}
      </main>
    </div>
  );
}
