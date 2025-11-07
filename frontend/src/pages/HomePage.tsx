import { Link } from 'react-router-dom';
import type { User } from '../types';

interface HomePageProps {
  user: User | null;
}

export default function HomePage({ user }: HomePageProps) {
  return (
    <div className="min-h-screen bg-background">
      {/* ヘッダー */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary">🎲 otomochi</h1>
          <div>
            {user ? (
              <Link to="/dashboard" className="btn-primary">
                ダッシュボード
              </Link>
            ) : (
              <Link to="/login" className="btn-primary">
                ログイン
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* ヒーローセクション */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-5xl font-bold mb-6 text-gray-900">
            TRPG専用<br />音声書き起こしサービス
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            セッションの音声を高精度で文字起こし。<br />
            タイムスタンプ付きで、あとから振り返りも簡単。
          </p>
          <Link to={user ? '/dashboard' : '/login'} className="btn-primary text-lg px-8 py-3">
            今すぐ始める
          </Link>
        </div>
      </section>

      {/* 特徴セクション */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-center mb-12 text-gray-900">
            otomochi の特徴
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="card text-center">
              <div className="text-4xl mb-4">⚡</div>
              <h4 className="text-xl font-bold mb-2">高速処理</h4>
              <p className="text-gray-600">
                3時間の音声を15分以内に書き起こし。
                最新のAI技術で高速処理を実現。
              </p>
            </div>
            <div className="card text-center">
              <div className="text-4xl mb-4">🎯</div>
              <h4 className="text-xl font-bold mb-2">高精度</h4>
              <p className="text-gray-600">
                TRPG用語に特化した辞書で、
                専門用語も正確に認識。
              </p>
            </div>
            <div className="card text-center">
              <div className="text-4xl mb-4">🔒</div>
              <h4 className="text-xl font-bold mb-2">プライバシー重視</h4>
              <p className="text-gray-600">
                音声データはクラウドに保存せず、
                処理後は自動削除。
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 料金プラン */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-center mb-12 text-gray-900">
            料金プラン
          </h3>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="card">
              <h4 className="text-xl font-bold mb-2">無料</h4>
              <div className="text-3xl font-bold text-primary mb-4">¥0</div>
              <ul className="space-y-2 text-gray-600">
                <li>✓ 月3回（5分まで）</li>
              </ul>
            </div>
            <div className="card border-2 border-primary">
              <h4 className="text-xl font-bold mb-2">ライト</h4>
              <div className="text-3xl font-bold text-primary mb-4">¥680</div>
              <ul className="space-y-2 text-gray-600">
                <li>✓ 月3セッション</li>
                <li>✓ 合計9時間</li>
              </ul>
            </div>
            <div className="card">
              <h4 className="text-xl font-bold mb-2">スタンダード</h4>
              <div className="text-3xl font-bold text-primary mb-4">¥1,200</div>
              <ul className="space-y-2 text-gray-600">
                <li>✓ 月5セッション</li>
                <li>✓ 合計15時間</li>
              </ul>
            </div>
            <div className="card">
              <h4 className="text-xl font-bold mb-2">無制限</h4>
              <div className="text-3xl font-bold text-primary mb-4">¥4,000</div>
              <ul className="space-y-2 text-gray-600">
                <li>✓ 無制限</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* フッター */}
      <footer className="bg-white py-8 px-4">
        <div className="max-w-7xl mx-auto text-center text-gray-600">
          <p>© 2024 otomochi. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
