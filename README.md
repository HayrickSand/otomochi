# 🎲 otomochi

**TRPG専用の音声録音書き起こしサービス**

RunPod + Faster-Whisper large-v3-turbo ベースで実現する、高速・高精度なTRPGセッション書き起こしプラットフォーム。

---

## 📌 概要

otomochi は、TRPGセッションの音声を高速・高精度で文字起こしするサービスです。

### 主な特徴

- ⚡ **高速処理**: 3時間の音声を15分以内に書き起こし
- 🎯 **高精度**: TRPG用語に特化した辞書で専門用語も正確に認識
- 🔒 **プライバシー重視**: 音声データはRAMディスクで一時処理、完了後は自動削除
- ⏱️ **タイムスタンプ付き**: 発話区間ごとにタイムコードを付与
- 📝 **ミックス出力**: セッションログと書き起こし結果を統合
- 💸 **柔軟な課金プラン**: 無料プランから無制限プランまで

---

## 🏗️ 技術スタック

### バックエンド
- **FastAPI**: 高速な非同期Webフレームワーク
- **Faster-Whisper**: large-v3-turbo モデルによる音声認識
- **Celery + Redis**: 非同期ジョブ処理
- **Supabase**: 認証・データベース管理

### フロントエンド
- **React + TypeScript**: モダンなSPA
- **TailwindCSS**: ユーティリティファーストCSS
- **Vite**: 高速ビルドツール

### インフラ
- **RunPod**: NVIDIA A100 80GB GPU インスタンス
- **Docker**: コンテナ化
- **RAM Disk**: 一時ファイル処理

---

## 📋 プロジェクト構造

```
otomochi/
├── backend/              # FastAPI バックエンド
│   ├── app/
│   │   ├── api/          # APIエンドポイント
│   │   ├── core/         # コア設定
│   │   ├── models/       # データモデル
│   │   ├── schemas/      # Pydanticスキーマ
│   │   ├── services/     # ビジネスロジック
│   │   │   ├── whisper_service.py          # Whisper音声認識
│   │   │   ├── audio_preprocessing.py      # 音声前処理
│   │   │   └── output_formatter.py         # 出力フォーマット
│   │   ├── tasks/        # Celeryタスク
│   │   └── main.py       # アプリケーションエントリーポイント
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # React フロントエンド
│   ├── src/
│   │   ├── components/   # UIコンポーネント
│   │   ├── pages/        # ページコンポーネント
│   │   ├── types/        # TypeScript型定義
│   │   ├── utils/        # ユーティリティ
│   │   └── App.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 セットアップ

### 1. 環境変数の設定

```bash
cp .env.example .env
```

`.env` ファイルを編集して、必要な値を設定してください：

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# JWT
SECRET_KEY=your-secret-key-here

# Redis
REDIS_URL=redis://redis:6379/0
```

### 2. Docker Compose で起動

```bash
docker-compose up -d
```

### 3. アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs

---

## 💻 開発

### バックエンド開発

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### フロントエンド開発

```bash
cd frontend
npm install
npm run dev
```

### Celery ワーカー起動

```bash
cd backend
celery -A app.tasks.celery_app worker --loglevel=info
```

### Celery Beat 起動（定期タスク）

```bash
cd backend
celery -A app.tasks.celery_app beat --loglevel=info
```

---

## 📊 機能一覧

### ✅ 実装済み

- [x] プロジェクト構造とディレクトリ構成
- [x] Docker設定（RunPod対応）
- [x] FastAPI バックエンドの基本構造
- [x] Faster-Whisper 音声処理モジュール
- [x] 音声前処理（ノイズ除去、正規化）
- [x] Redis + Celery ジョブ管理
- [x] Celery Beat 定期タスクスケジューラ
- [x] 8時間後のデータ自動削除機能
- [x] React フロントエンド基本構造
- [x] TailwindCSS 配色テーマ (#de8f7d / #FFF4E9)
- [x] ページコンポーネント（Home, Login, Dashboard, Transcription, Profile, Admin, Billing）
- [x] 出力フォーマット（TXT, JSON, HTML）
- [x] ミックスログ生成
- [x] Supabase Auth 統合（OAuth: Google/Twitter + メール/パスワード）
- [x] データベーススキーマ作成
- [x] 課金プラン管理機能
- [x] Stripe 連携（サブスクリプション + ワンショット課金）
- [x] 削除予定時刻の表示とダウンロード促進UI

### 🚧 実装予定

- [ ] Discord Bot 連携
- [ ] 話者分離機能
- [ ] TRPG用語辞書管理UI
- [ ] n-best リランキング
- [ ] KenLM 文体補正

---

## 💰 課金プラン

| プラン | 月額料金 | セッション数 | 合計時間 |
|--------|----------|--------------|----------|
| 無料 | ¥0 | 3回 | 5分 |
| ライト | ¥680 | 3回 | 9時間 |
| スタンダード | ¥1,200 | 5回 | 15時間 |
| 無制限 | ¥4,000 | 無制限 | 無制限 |

**ワンショット**: ¥120/時間

---

## 🔧 処理フロー

1. **音声アップロード**: ユーザーが音声ファイル（MP3/WAV）をアップロード
2. **前処理**: ノイズ除去、音量正規化、リサンプリング（16kHz）
3. **Whisper処理**: Faster-Whisper large-v3-turbo で書き起こし
4. **後処理**: カタカナ正規化、TRPG用語補正
5. **出力生成**: TXT/JSON/HTML形式で出力
6. **クリーンアップ**: RAMディスク上の一時ファイルを削除

---

## 📈 パフォーマンス目標

- **処理速度**: 音声3時間を15分以内（処理速度比 1:12）
- **GPU使用率**: A100 80GB で 80% 以上
- **同時処理**: キューイングによる順次処理
- **スケーラビリティ**: RunPod オートスケールで負荷分散

---

## 🔐 セキュリティ

- **データ保護**: 音声/テキストはクラウド非保存
- **RAM処理**: 一時ファイルは RAM ディスクで処理、完了後削除
- **自動削除ポリシー**: 書き起こし完了から8時間後にデータを自動削除
  - 完了した書き起こしは8時間後に自動削除されます
  - フロントエンドに削除予定時刻と残り時間を表示
  - ダウンロード推奨の警告バナーを表示
  - Celery Beat による30分間隔の定期クリーンアップ
- **認証**: Supabase Auth (OAuth: Google/Twitter + メール/パスワード)
- **API保護**: JWT トークン認証

---

## 📝 API エンドポイント

### 認証

- `POST /api/auth/login` - ログイン
- `POST /api/auth/signup` - 新規登録
- `POST /api/auth/logout` - ログアウト
- `GET /api/auth/me` - 現在のユーザー情報

### 書き起こし

- `POST /api/transcriptions` - 新規書き起こしジョブ作成
- `GET /api/transcriptions` - 書き起こしリスト取得
- `GET /api/transcriptions/{id}` - 書き起こし詳細取得
- `GET /api/transcriptions/{id}/download` - ダウンロード
- `DELETE /api/transcriptions/{id}` - 削除

### ユーザー

- `GET /api/users/me` - プロフィール取得
- `PATCH /api/users/me` - プロフィール更新
- `GET /api/users/me/usage` - 使用量取得
- `POST /api/users/me/plan` - プラン変更

### 管理者

- `GET /api/admin/stats` - 統計情報取得
- `GET /api/admin/users` - ユーザーリスト取得
- `GET /api/admin/revenue/export` - 収益CSV出力

---

## 🤝 コントリビューション

プルリクエストを歓迎します！

### コミットメッセージ規約

- `feat:` 新機能追加
- `fix:` バグ修正
- `docs:` ドキュメント更新
- `refactor:` リファクタリング

すべてのコミットメッセージは**日本語**で記述してください。

---

## 📄 ライセンス

MIT License

---

## 📧 お問い合わせ

バグ報告や機能リクエストは GitHub Issues にお願いします。

---

**otomochi** - TRPG をもっと楽しく、もっと便利に 🎲
