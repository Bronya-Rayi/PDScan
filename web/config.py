import logging
import os

SECRET_KEY = os.urandom(24)

""" Sqlalchemy 配置 """
SQLALCHEMY_DATABASE_URI = 'sqlite:////app/PDScan/db/database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_RECYCLE = 8



LOG_LEVEL = logging.ERROR
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'log')
SYSTEM_STATUS_LOG_PATH = "/app/PDScan/web/log/system_status.log"
STATIC_FOLDER = "/app/PDScan/web/static"

