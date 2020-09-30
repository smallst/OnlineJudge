# coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "onlinejudge",
        'USER': "onlinejudge",
        'PASSWORD': 'onlinejudge',
        'HOST': 'host.docker.internal',
        'PORT': 5435
    }
}

REDIS_CONF = {
    "host": "127.0.0.1",
    "port": "6380"
}


DEBUG = True

ALLOWED_HOSTS = ["*"]

DATA_DIR = f"{BASE_DIR}/data"
