from flask import Flask

from .sqlalchemy import db,init_databases
from .http import success_api,fail_api
from .init_login import init_login_manager
from .log import logger

def init_utils(app: Flask) -> None:
    init_databases(app)
    init_login_manager(app)
