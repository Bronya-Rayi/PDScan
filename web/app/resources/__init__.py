from flask_restful import Api

from .auth import LoginResource, ChPasswdResource
from .task import TaskListResource, TaskDeleteResource, ShowCDuanResult, ShowIPResult, ShowSiteResult, ShowDomainResult, TaskStatusResource, ShowVulscanResult,ShowSitePathScanResult
from .settings import ToolsConfResource


def register_auth_api(api_bp):
    auth_api = Api(api_bp)
    auth_api.add_resource(LoginResource, '/auth/login')
    auth_api.add_resource(ChPasswdResource, '/auth/chpasswd')
    

def register_task_list_api(api_bp):
    task_list_api = Api(api_bp)
    task_list_api.add_resource(TaskListResource,'/task/list')
    task_list_api.add_resource(TaskDeleteResource,'/task/delete')
    task_list_api.add_resource(TaskStatusResource,'/task/status')

def register_task_detail_api(api_bp):
    task_detail_api = Api(api_bp)
    task_detail_api.add_resource(ShowSiteResult,'/site/list')
    task_detail_api.add_resource(ShowDomainResult,'/domain/list')   
    task_detail_api.add_resource(ShowCDuanResult,'/cduan/list')
    task_detail_api.add_resource(ShowIPResult,'/ip/list')
    task_detail_api.add_resource(ShowVulscanResult,'/vulscan/list')
    task_detail_api.add_resource(ShowSitePathScanResult,'/site_path_scan/list')

def register_settings_api(api_bp):
    settings_api = Api(api_bp)
    settings_api.add_resource(ToolsConfResource,'/settings/tools')