import os

from flask import Flask, Blueprint
from app.utils import init_utils
import config


api_bp: Blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

# from .resources.rights import register_rights_api
# from .system import register_system_api
# from .users import register_users_api
# from .task import register_task_api
from .resources import register_auth_api, register_show_log_api, register_task_list_api, register_task_detail_api


register_auth_api(api_bp)
register_show_log_api(api_bp)
register_task_list_api(api_bp)
register_task_detail_api(api_bp)
# register_users_api(api_bp)
# register_system_api(api_bp)
# register_task_api(api_bp)

def create_app() -> Flask:
    app = Flask('pdscan-flask',static_url_path='/',static_folder='static')

    # 引入配置
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_ECHO'] = config.SQLALCHEMY_ECHO

    app.config['LOG_PATH'] = config.LOG_PATH
    app.config['LOG_LEVEL'] = config.LOG_LEVEL 
    


    # 初始化工具
    init_utils(app)

    # 注册接口（restful api）
    app.register_blueprint(api_bp)

    # 初始化目录
    if not os.path.exists(config.HTTPX_RESULTS_PATH):
        os.makedirs(config.HTTPX_RESULTS_PATH)
    if not os.path.exists(config.ONEFORALL_RESULTS_PATH):
        os.makedirs(config.ONEFORALL_RESULTS_PATH)
    if not os.path.exists(config.XRAY_RESULTS_PATH):
        os.makedirs(config.XRAY_RESULTS_PATH)
    if not os.path.exists(config.SCANINFO_RESULTS_PATH):
        os.makedirs(config.SCANINFO_RESULTS_PATH)

    # 初始化日志文件
    if not os.path.exists(config.LOG_PATH):
        os.makedirs(config.LOG_PATH)
    open(config.SYSTEM_STATUS_LOG_PATH, 'w').close()
    open(config.ONEFORALL_LOG_PATH, 'w').close()
    open(config.HTTPX_LOG_PATH, 'w').close()
    open(config.SCANINFO_LOG_PATH, 'w').close()
    open(config.XRAY_LOG_PATH, 'w').close()
    open(config.CRAWLERGO_LOG_PATH, 'w').close()
    

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
