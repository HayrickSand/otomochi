# Multi-stage build for React frontend
FROM node:20-alpine AS builder

WORKDIR /app

# 依存関係のインストール
COPY package.json package-lock.json* ./
RUN npm install

# アプリケーションのビルド
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# カスタム nginx 設定
COPY nginx.conf /etc/nginx/conf.d/default.conf

# ビルドされたファイルをコピー
COPY --from=builder /app/dist /usr/share/nginx/html

# ポート公開
EXPOSE 80

# nginx 起動
CMD ["nginx", "-g", "daemon off;"]
