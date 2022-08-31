from flask_restful import Api

from .task_list import TaskListResource, TaskAddResource ,TaskStatusResource, TaskDeleteResource
from .task_manage import TaskLogResource, TaskRebootResource
from .show_result import ShowSubdomainResult, ShowPortScanResult, ShowCDuanResult, ShowSiteResult


def register_task_api(api_bp):
    task_api = Api(api_bp)
    task_api.add_resource(TaskListResource, '/task/list')
    task_api.add_resource(TaskAddResource, '/task/add')
    task_api.add_resource(TaskStatusResource, '/task/status')
    task_api.add_resource(TaskDeleteResource, '/task/delete')
    task_api.add_resource(TaskLogResource, '/task/log')
    task_api.add_resource(ShowSubdomainResult, '/task/show/subdomain/<task_id>')
    task_api.add_resource(ShowPortScanResult, '/task/show/portscan/<task_id>')
    task_api.add_resource(ShowCDuanResult, '/task/show/cduan/<task_id>')
    task_api.add_resource(ShowSiteResult, '/task/show/site/<task_id>')
    task_api.add_resource(TaskRebootResource, '/task/reboot')
    # sys_api.add_resource(FilePhotosResource, '/file/photos')
    # sys_api.add_resource(FilePhotoResource, '/file/photo/<int:photo_id>')
    # sys_api.add_resource(LoginResource, '/passport/login')
