import hashlib
import json
import time
import uuid

from flask import request
from flask_restful import Resource
from sqlalchemy import and_, desc

from app.models import DomainModels, IPModels, SiteModels, TaskModels
from app.utils import db, fail_api, success_api, logger
from app.service.task_manager import TaskManager

from .auth import auth_required

'''
展示任务列表，不包含改删操作
'''


class TaskListResource(Resource):

    @auth_required
    def get(self):
        page = request.args.get('page', type=int)
        perPage = request.args.get('perPage', type=int)
        task_list_paginate = TaskModels.query.order_by(desc(TaskModels.task_start_time)
                                                       ).paginate(page=page,
                                                                  per_page=perPage,
                                                                  error_out=False)
        task_list_total = TaskModels.query.count()
        data = [
            {
                'task_id': item.task_id,
                'task_name': item.task_name,
                'task_target': item.task_target,
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
                target_html += target + ' | '
            task['task_target'] = target_html
            target_html = ''

        return success_api(data=data)

    @auth_required
    def post(self):
        taskModel = TaskModels()
        task_id = hashlib.md5(str(uuid.uuid4()).encode('utf8')).hexdigest()[:8]

        task_target = request.json.get('task_target')
        task_target = json.dumps(task_target.split('\n'))

        taskModel.task_id = task_id
        taskModel.task_name = request.json.get(
            'task_name').strip().replace(' ', '_')
        taskModel.task_target = str(task_target)
        taskModel.task_running_module = request.json.get('task_running_module')
        taskModel.task_status = 'Waiting'
        taskModel.task_start_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        taskModel.task_port_limit = request.json.get('port_limit')
        taskModel.task_vulscan = request.json.get('vulscan')
        try:
            db.session.add(taskModel)
            db.session.commit()
            TaskManager(task_id, taskModel.task_name, task_target,taskModel.task_running_module)
            return success_api(message='添加成功')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return fail_api(message='添加失败')


class TaskDeleteResource(Resource):

    @auth_required
    def get(self, task_id):
        # 先中断正在进行的任务，再对任务进行删除
        TaskManager.stopTask(task_id)
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

'''
任务状态操作，包含启动、暂停
'''

class TaskStatusResource(Resource):

    @auth_required
    def get(self):
        try:
            if request.args.get('task_status') == 'Paused':
                TaskModels.query.filter_by(task_id=request.args.get('task_id')).update({'task_status': 'Running'})
                db.session.commit()
                logger.info("[+] 任务{}启动成功".format(request.args.get('task_id')))
                return success_api('启动成功')
            elif request.args.get('task_status') == 'Running': 
                task_running_module = TaskManager.stopTask(request.args.get('task_id'))
                # 任务中断时会造成任务记录为error，这里需要再更新下为Paused
                time.sleep(2)
                TaskModels.query.filter_by(task_id=request.args.get('task_id')).update({'task_status': 'Paused', 'task_running_module': task_running_module})
                db.session.commit()
                logger.info("[+] 任务{}暂停成功".format(request.args.get('task_id')))
                return success_api('暂停成功')
            else:
                task_running_module = TaskManager.stopTask(request.args.get('task_id'))
                # 更新数据库中的任务状态
                time.sleep(2)
                TaskModels.query.filter_by(task_id=request.args.get('task_id')).update({'task_status': 'Waiting', 'task_running_module': task_running_module})
                db.session.commit()
                logger.info("[+] 任务{}重启成功".format(request.args.get('task_id')))
                return success_api('重启成功')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return fail_api('[!] 操作失败')

'''
任务详情展示
'''


class ShowSiteResult(Resource):

    @auth_required
    def get(self, task_id):
        page = request.args.get('page', type=int)
        perPage = request.args.get('perPage', type=int)

        # 当task_id为all时查询所有站点
        if task_id == 'all':
            task_id = ''
        query_rule = and_(
            SiteModels.task_id.like("%{}%".format(task_id)),
            SiteModels.url.like("%{}%".format(
                request.args.get('url', type=str))),
            SiteModels.ip.like("%{}%".format(
                request.args.get('ip', type=str))),
            SiteModels.status_code.like("%{}%".format(
                request.args.get('status_code', type=str))),
            SiteModels.title.like("%{}%".format(
                request.args.get('title', type=str))),
            SiteModels.finger.like("%{}%".format(
                request.args.get('finger', type=str))),
        )

        site_result = SiteModels.query.filter(query_rule).paginate(
            page=page, per_page=perPage, error_out=False)
        site_total = SiteModels.query.filter(query_rule).count()

        data = [
            {
                'id': item.id,
                'task_id': item.task_id,
                'url': item.url,
                'ip': item.ip,
                'status_code': item.status_code,
                'title': item.title,
                'finger': item.finger,
            } for item in site_result.items
        ]
        out_data = {
            "items": data,
            "total": site_total
        }
        return success_api(data=out_data)


class ShowDomainResult(Resource):

    @auth_required
    def get(self, task_id):
        page = request.args.get('page', type=int)
        perPage = request.args.get('perPage', type=int)

        if task_id == 'all':
            task_id = ''

        query_rule = and_(
            DomainModels.task_id.like("%{}%".format(task_id)),
            DomainModels.domain.like("%{}%".format(
                request.args.get('domain', type=str))),
            DomainModels.domain_record.like("%{}%".format(
                request.args.get('domain_record', type=str))),
        )

        domain_result = DomainModels.query.filter(query_rule).paginate(
            page=page, per_page=perPage, error_out=False)
        domain_total = DomainModels.query.filter(query_rule).count()

        data = [
            {
                'domain': item.domain,
                'domain_record': item.domain_record,
                'task_id': task_id,
            } for item in domain_result.items
        ]

        out_data = {
            "items": data,
            "total": domain_total
        }
        return success_api(data=out_data)


class ShowPortScanResult(Resource):

    @auth_required
    def get(self, task_id):
        page = request.args.get('page', type=int)
        perPage = request.args.get('perPage', type=int)

        if task_id == 'all':
            task_id = ''

        query_rule = and_(
            IPModels.task_id.like("%{}%".format(task_id)),
            IPModels.ip.like("%{}%".format(request.args.get('ip', type=str))),
            IPModels.port.like("%{}%".format(
                request.args.get('port', type=str))),
            IPModels.service.like("%{}%".format(
                request.args.get('service', type=str))),
            IPModels.banner.like("%{}%".format(
                request.args.get('banner', type=str))),
        )

        portscan_result = IPModels.query.filter(query_rule).paginate(
            page=page, per_page=perPage, error_out=False)
        portscan_total = IPModels.query.filter(query_rule).count()

        data = [
            {
                'ip': item.ip,
                'port': item.port,
                'service': item.service,
                'banner': item.banner[0:50],
            } for item in portscan_result.items
        ]

        out_data = {
            "items": data,
            "total": portscan_total
        }
        return success_api(data=out_data)


class ShowCDuanResult(Resource):

    @auth_required
    def get(self, task_id):

        cduan_result = TaskModels.query.filter(TaskModels.task_id.like("%{}%".format(task_id))).first().task_c_duan

        result_list = json.loads(cduan_result)
        result_html = ''
        for i in result_list:
            result_html += i + '\n'

        out_data = {
            "c_duan": result_html
        }
        return success_api(data=out_data)

class ShowVulscanResult(Resource):

    @auth_required
    def get(self, task_id):
        if task_id == 'all':
            return fail_api(message="需要指定任务id")
        else:
            vulscan_result = TaskModels.query.filter_by(task_id=task_id).first().task_xray_result
            if vulscan_result == None:
                return fail_api(message="未扫描到漏洞")
            vulscan_result = json.loads(vulscan_result)
            data = [
                {
                    'xray_result_url': item,
                } for item in vulscan_result
            ]
            out_data = {
                "items": data
            }
            return success_api(data=out_data)
