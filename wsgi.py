from pathlib import Path
import os

from dotenv import load_dotenv

from haw.celery import celery  # noqa # haw中自带celery，需要与app实例在同一文件

from app.app import create_app
from app.cli import register_cli_commands

APP_CONFIG = os.getenv('APP_CONFIG', 'production')  # 运行时唯一需要指定的变量

load_dotenv(dotenv_path=Path('.env'))
# load_dotenv(dotenv_path=Path('.') / 'env' / f'{APP_CONFIG}.env')

# app = create_app(APP_CONFIG, '../upload')
app = create_app(APP_CONFIG)
register_cli_commands(app)
