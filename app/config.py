from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')  # 为 mysql 容器名称

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

DB = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'  # noqa E501

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    SQLALCHEMY_DATABASE_URI = DB
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/test.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # SQLALCHEMY_ECHO = True

    UPLOAD_DIR = 'upload'

    # Celery 临时性配置，需要修改
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL',
                                  f'redis://:{REDIS_PASSWORD}@redis:6379/0')
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 5

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    # MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # redis
    REDIS_HOST = 'redis'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = REDIS_PASSWORD
    REDIS_EXPIRE = 60

    # celery
    REDIS_URI = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/1'
    CELERY_BROKER = REDIS_URI
    CELERY_BACKEND = REDIS_URI

    FRONT_URL_ROOT = 'http://localhost:8080/'
    FRONT_REGISTER_VALID_PREFIX = f'{FRONT_URL_ROOT}user/valid/'  # 发送邮件的激活地址前缀
    FRONT_RESET_PWD_PREFIX = f'{FRONT_URL_ROOT}user/resetpwd/'

    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 7  # 7天

    # 超级管理员
    SUPER_ADMIN_NAME = os.getenv('SUPER_ADMIN_EMAIL', 'studyxiao')
    SUPER_ADMIN_EMAIL = os.getenv('SUPER_ADMIN_EMAIL', 'dev@studyxiao.cn')
    SUPER_ADMIN_PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD', '123456')
    # 分页
    PAGE_DEFAULT = 0  # 起始页
    COUNT_DEFAULT = 10  # 个数


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI =
    pass


class TestingConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
