import { useState } from 'react';
import { Link } from 'react-router-dom';
import { userApi, authApi } from '../utils/api';
import type { User } from '../types';

interface ProfilePageProps {
  user: User;
  setUser: (user: User) => void;
}

export default function ProfilePage({ user, setUser }: ProfilePageProps) {
  const [displayName, setDisplayName] = useState(user.display_name || '');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const updatedUser = await userApi.updateProfile(displayName);
      setUser(updatedUser);
      setMessage('プロフィールを更新しました');
    } catch (error) {
      setMessage('更新に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await authApi.logout();
    window.location.href = '/';
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

      <main className="max-w-2xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8">プロフィール</h1>

        <div className="card mb-6">
          <h2 className="text-xl font-bold mb-4">基本情報</h2>
          <form onSubmit={handleUpdateProfile} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">メールアドレス</label>
              <input
                type="email"
                value={user.email}
                className="input-field"
                disabled
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">表示名</label>
              <input
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                className="input-field"
              />
            </div>

            {message && (
              <div className="bg-green-100 text-green-700 px-4 py-2 rounded">
                {message}
              </div>
            )}

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? '更新中...' : '更新'}
            </button>
          </form>
        </div>

        <div className="card mb-6">
          <h2 className="text-xl font-bold mb-4">プラン情報</h2>
          <div className="space-y-4">
            <div>
              <div className="text-sm text-gray-600">現在のプラン</div>
              <div className="text-2xl font-bold text-primary">
                {user.plan.plan_type.toUpperCase()}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="text-sm text-gray-600">今月の使用セッション</div>
                <div className="font-bold">
                  {user.plan.sessions_used} / {user.plan.sessions_limit}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">今月の使用時間</div>
                <div className="font-bold">
                  {user.plan.hours_used.toFixed(1)} / {user.plan.hours_limit} 時間
                </div>
              </div>
            </div>
            <button className="btn-secondary w-full">
              プランを変更
            </button>
          </div>
        </div>

        <div className="card">
          <button onClick={handleLogout} className="btn-secondary w-full text-red-600 border-red-600 hover:bg-red-50">
            ログアウト
          </button>
        </div>
      </main>
    </div>
  );
}
