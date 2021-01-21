FROM python:3.8.3

ENV PYTHONUNBUFFERED 1 \
  # 禁止生成 .pyc 文件
  PYTHONDONTWRITEBYTECODE=1 \
  #### pip
  PIP_NO_CACHE_DIR=1 \
  # PIP_DISABLE_PIP_VERSION_CHECK=1 \  # not working
  PIP_DEFAULT_TIMEOUT=100 \
  TZ=Asia/Shanghai

WORKDIR /app

ARG APP_CONFIG='production'
ENV FLASK_ENV=${APP_CONFIG}
COPY . /app
RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check -i https://pypi.tuna.tsinghua.edu.cn/simple

# ENTRYPOINT ["sh", "/code/docker/boot.sh"]
