FROM public.ecr.aws/lambda/python:3.13

# psycopg[binary] に必要な依存をインストール
RUN yum install -y gcc postgresql-devel

# ワーキングディレクトリ作成
WORKDIR /var/task

# 依存ライブラリをコピー（app 配下から）
COPY app/requirements.txt .

# 依存をインストール（バイナリ版含む）
RUN pip3 install --upgrade pip \
 && pip3 install --no-cache-dir -r requirements.txt

# Lambda ソースコードをコピー
COPY app/ .

# Lambda handler の指定（handler.py に lambda_handler 関数がある）
CMD ["handler.lambda_handler"]