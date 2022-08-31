import os

from flask import Flask, Blueprint
from common.flask_uploads import configure_uploads

from common.utils.upload import photos
from extensions import init_plugs
from applications.view import init_view
import config


api_bp: Blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

from .rights import register_rights_api
from .system import register_system_api
from .users import register_users_api
from .task import register_task_api

register_rights_api(api_bp)
register_users_api(api_bp)
register_system_api(api_bp)
register_task_api(api_bp)


def init_api(app: Flask) -> None:
    app.register_blueprint(api_bp)


def create_app() -> Flask:
    app = Flask('pear-admin-flask')

    # 引入数据库配置
    app.config.from_object(config)

    # 注册各种插件
    init_plugs(app)

    # 注册路由
    init_view(app)

    # 注册接口（restful api）
    init_api(app)

    # 文件上传
    configure_uploads(app, photos)

    # 初始化目录
    if not os.path.exists(config.HTTPX_RESULTS_PATH):
        os.makedirs(config.HTTPX_RESULTS_PATH)
    if not os.path.exists(config.ONEFORALL_RESULTS_PATH):
        os.makedirs(config.ONEFORALL_RESULTS_PATH)
    if not os.path.exists(config.XRAY_RESULTS_PATH):
        os.makedirs(config.XRAY_RESULTS_PATH)
    if not os.path.exists(config.SCANINFO_RESULTS_PATH):
        os.makedirs(config.SCANINFO_RESULTS_PATH)


    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        logo()

    return app


def logo():
    print('''


    ____  ____  _____                
   / __ \/ __ \/ ___/_________ _____ 
  / /_/ / / / /\__ \/ ___/ __ `/ __ \
 / ____/ /_/ /___/ / /__/ /_/ / / / /
/_/   /_____//____/\___/\__,_/_/ /_/ 
                                     



    ''')
