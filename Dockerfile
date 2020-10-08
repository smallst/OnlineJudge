FROM python:3.7-alpine3.9
ENV OJ_ENV production

ADD . /app
WORKDIR /app

HEALTHCHECK --interval=5s --retries=3 CMD python2 /app/deploy/health_check.py
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
		sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
apk add --update --no-cache build-base nginx openssl curl unzip supervisor jpeg-dev zlib-dev postgresql-dev freetype-dev && \
    pip install --no-cache-dir -r /app/deploy/requirements.txt && \
    apk del build-base --purge


ENTRYPOINT /app/deploy/entrypoint.sh
