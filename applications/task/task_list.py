from flask import request,current_app
from flask_restful import Resource
from sqlalchemy import desc
from flask_login import current_user
from service.task_manager import TaskManager
from common.utils.http import fail_api, success_api, table_api
from extensions import db
from models import TaskModels, SiteModels, DomainModels, IPModels
import time
import hashlib
import json
import uuid 
from common.utils.log import logger

class TaskListResource(Resource):

    def get(self):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        page = request.args.get('page', type=int)
        limit = request.args.get('limit', type=int)
        task_list_paginate = TaskModels.query.order_by(desc(TaskModels.task_start_time)
                                                    ).paginate(page=page,
                                                             per_page=limit,
                                                             error_out=False)
        task_list_total = TaskModels.query.count()
        data = [
            {
                'task_id': item.task_id,
                'task_name': item.task_name,
                'task_target': item.task_target,
                'task_result_count': item.task_result_count,
                'task_running_module': item.task_running_module,
                'task_status': item.task_status,
                'task_start_time': item.task_start_time,
                'task_end_time': item.task_end_time,
            } for item in task_list_paginate.items
        ]

        # 转换成可以在前端显示的html
        target_html = ''
        for task in data:
            for target in json.loads(task['task_target']):
                target_html += '<li>' + target + '</li>'
            task['task_target'] = target_html
            target_html = ''

        return table_api(result={'items': data,
                                 'total': task_list_total, },
                         code=0)

class TaskAddResource(Resource):

    def post(self):
        # print(request.json)
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        taskModel = TaskModels()
        task_id = hashlib.md5(str(uuid.uuid4()).encode('utf8')).hexdigest()[:8]

        task_target = request.json.get('task_target')
        task_target = json.dumps(task_target.split('\n'))

        taskModel.task_id = task_id
        taskModel.task_name = request.json.get('task_name').strip().replace(' ','_')
        taskModel.task_target = str(task_target)
        taskModel.task_running_module = 'Waiting'
        taskModel.task_status = 'Waiting'
        taskModel.task_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        taskModel.task_port_limit = request.json.get('port_limit')
        taskModel.task_vulscan = request.json.get('vulscan')
        try:
            db.session.add(taskModel)
            db.session.commit()
            TaskManager(task_id, taskModel.task_name, task_target)
            return success_api('添加成功')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return fail_api('添加失败')

class TaskDeleteResource(Resource):

    def post(self):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        task_id = request.json.get('task_id')
        # 先中断正在进行的任务，再对任务进行删除
        TaskManager.stopTask(request.json.get('task_id'))
        try:
            taskModel = TaskModels.query.filter_by(task_id=task_id).delete()
            db.session.commit()
            domainModel = DomainModels.query.filter_by(task_id=task_id).delete()
            db.session.commit()
            ipModel = IPModels.query.filter_by(task_id=task_id).delete()
            db.session.commit()
            siteModel = SiteModels.query.filter_by(task_id=task_id).delete()
            db.session.commit()
            return success_api('删除成功')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return fail_api('删除失败')

class TaskStatusResource(Resource):

    def post(self):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        try:
            if request.json.get('task_status') == 'Paused':
                TaskModels.query.filter_by(task_id=request.json.get('task_id')).update({'task_status': 'Running'})
                db.session.commit()
                logger.info("任务{}启动成功".format(request.json.get('task_id')))
                return success_api('启动成功')
            elif request.json.get('task_status') == 'Running': 
                task_running_module = TaskManager.stopTask(request.json.get('task_id'))
                # 任务中断时会造成任务记录为error，这里需要再更新下为Paused
                time.sleep(2)
                TaskModels.query.filter_by(task_id=request.json.get('task_id')).update({'task_status': 'Paused', 'task_running_module': task_running_module})
                db.session.commit()
                logger.info("任务{}暂停成功".format(request.json.get('task_id')))
                return success_api('暂停成功')
            else:
                task_running_module = TaskManager.stopTask(request.json.get('task_id'))
                # 更新数据库中的任务状态
                time.sleep(2)
                TaskModels.query.filter_by(task_id=request.json.get('task_id')).update({'task_status': 'Waiting', 'task_running_module': task_running_module})
                db.session.commit()
                logger.info("任务{}重启成功".format(request.json.get('task_id')))
                return success_api('重启成功')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return fail_api('操作失败')