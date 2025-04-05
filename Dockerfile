# === Build stage ===
FROM amazonlinux:2023 AS build

# 基本ツールと Python、PostgreSQL ビルド用依存をインストール
RUN yum install -y \
      gcc \
      postgresql-devel \
      python3 \
      python3-pip \
      python3-devel \
      libpq-devel

RUN python3 -m ensurepip && pip3 install --upgrade pip

WORKDIR /app

# 依存関係インストール
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir --target /app/python -r requirements.txt


# === Runtime stage ===
FROM public.ecr.aws/lambda/python:3.11

# /opt/python に置くと Lambda が認識してくれる（レイヤー相当）
COPY --from=build /app/python /opt/python

# Lambda 関数のコードをコピー
COPY app/ /var/task/

# Lambda handler のエントリーポイント
CMD ["handler.lambda_handler"]