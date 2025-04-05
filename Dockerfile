# ベースイメージ
FROM python:3.11-slim

# システムパッケージ（psycopg[binary] や orjson 用）をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを作成
WORKDIR /app

# 依存ファイルをコピーしてインストール
COPY app/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# アプリケーション本体をコピー
COPY app/ .

# ポート開放（FastAPIのデフォルトポート）
EXPOSE 8000

# Uvicorn を起動（main.py の app オブジェクト）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]