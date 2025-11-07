# RunPod 対応 Dockerfile - NVIDIA GPU + CUDA サポート
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# 環境変数
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    CUDA_HOME=/usr/local/cuda

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python のシンボリックリンク作成
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# 作業ディレクトリ
WORKDIR /app

# Python依存関係のインストール
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# RAM ディスク用のマウントポイント作成
RUN mkdir -p /tmp/ramdisk

# ポート公開
EXPOSE 8000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# アプリケーション起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
