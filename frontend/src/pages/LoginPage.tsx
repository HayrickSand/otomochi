import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../utils/api';
import type { User } from '../types';

interface LoginPageProps {
  setUser: (user: User) => void;
}

export default function LoginPage({ setUser }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignup, setIsSignup] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = isSignup
        ? await authApi.signup(email, password)
        : await authApi.login(email, password);

      localStorage.setItem('access_token', data.access_token);
      setUser(data.user || { id: data.user_id, email: data.email });
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || '認証に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="card max-w-md w-full">
        <h1 className="text-3xl font-bold text-center mb-8 text-primary">
          🎲 otomochi
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">メールアドレス</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-field"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">パスワード</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-field"
              required
            />
          </div>

          {error && (
            <div className="bg-red-100 text-red-700 px-4 py-2 rounded">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="btn-primary w-full"
            disabled={loading}
          >
            {loading ? '処理中...' : isSignup ? '新規登録' : 'ログイン'}
          </button>

          <button
            type="button"
            className="w-full text-center text-sm text-primary hover:underline"
            onClick={() => setIsSignup(!isSignup)}
          >
            {isSignup ? 'ログインはこちら' : '新規登録はこちら'}
          </button>
        </form>

        <div className="mt-6 pt-6 border-t">
          <p className="text-sm text-gray-600 text-center mb-4">
            または、ソーシャルログイン
          </p>
          <div className="space-y-2">
            <button className="btn-secondary w-full">
              Googleでログイン
            </button>
            <button className="btn-secondary w-full">
              Twitterでログイン
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
