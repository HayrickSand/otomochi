import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { transcriptionApi } from '../utils/api';
import type { User, Transcription } from '../types';

interface DashboardPageProps {
  user: User;
}

export default function DashboardPage({ user }: DashboardPageProps) {
  const [transcriptions, setTranscriptions] = useState<Transcription[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTranscriptions();
  }, []);

  const loadTranscriptions = async () => {
    try {
      const data = await transcriptionApi.list(1, 20);
      setTranscriptions(data.transcriptions);
    } catch (error) {
      console.error('Failed to load transcriptions:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const badges: Record<string, string> = {
      pending: 'bg-yellow-100 text-yellow-800',
      processing: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
    };
    return badges[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary">🎲 otomochi</h1>
          <div className="flex gap-4">
            <Link to="/profile" className="btn-secondary">
              プロフィール
            </Link>
            {user.is_admin && (
              <Link to="/admin" className="btn-secondary">
                管理者
              </Link>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-4">ダッシュボード</h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="card">
              <div className="text-sm text-gray-600">今月の使用</div>
              <div className="text-2xl font-bold text-primary">
                {user.plan.sessions_used} / {user.plan.sessions_limit} セッション
              </div>
            </div>
            <div className="card">
              <div className="text-sm text-gray-600">使用時間</div>
              <div className="text-2xl font-bold text-primary">
                {user.plan.hours_used.toFixed(1)} / {user.plan.hours_limit} 時間
              </div>
            </div>
            <div className="card">
              <div className="text-sm text-gray-600">プラン</div>
              <div className="text-2xl font-bold text-primary">
                {user.plan.plan_type.toUpperCase()}
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold">書き起こし履歴</h3>
            <Link to="/upload" className="btn-primary">
              新規アップロード
            </Link>
          </div>

          {loading ? (
            <div className="text-center py-8">読み込み中...</div>
          ) : transcriptions.length === 0 ? (
            <div className="text-center py-8 text-gray-600">
              まだ書き起こしがありません
            </div>
          ) : (
            <div className="space-y-4">
              {transcriptions.map((t) => (
                <Link
                  key={t.id}
                  to={`/transcription/${t.id}`}
                  className="block p-4 border rounded-lg hover:bg-gray-50 transition"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-bold">{t.audio_filename}</h4>
                      <p className="text-sm text-gray-600">
                        {new Date(t.created_at).toLocaleString('ja-JP')}
                      </p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm ${getStatusBadge(t.status)}`}>
                      {t.status}
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
