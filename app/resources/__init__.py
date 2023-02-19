from flask_restful import Api

from .auth import LoginResource, ChPasswdResource
from .show_log import ShowLogResource
from .task import TaskListResource, TaskDeleteResource, ShowCDuanResult, ShowPortScanResult, ShowSiteResult, ShowDomainResult, TaskStatusResource, ShowVulscanResult


def register_auth_api(api_bp):
    auth_api = Api(api_bp)
    auth_api.add_resource(LoginResource, '/auth/login')
    auth_api.add_resource(ChPasswdResource, '/auth/chpasswd')
    

def register_show_log_api(api_bp):
    show_log_api = Api(api_bp)
    show_log_api.add_resource(ShowLogResource, '/show_log')

def register_task_list_api(api_bp):
    task_list_api = Api(api_bp)
    task_list_api.add_resource(TaskListResource,'/task/list')
    task_list_api.add_resource(TaskDeleteResource,'/task/delete/<task_id>')
    task_list_api.add_resource(TaskStatusResource,'/task/status')

def register_task_detail_api(api_bp):
    task_detail_api = Api(api_bp)
    task_detail_api.add_resource(ShowSiteResult,'/site/list/<task_id>/')
    task_detail_api.add_resource(ShowDomainResult,'/domain/list/<task_id>/')   
    task_detail_api.add_resource(ShowCDuanResult,'/cduan/list/<task_id>/')
    task_detail_api.add_resource(ShowPortScanResult,'/port/list/<task_id>/')
    task_detail_api.add_resource(ShowVulscanResult,'/vulscan/list/<task_id>/')