import hashlib
import json
import time
import uuid
import netaddr

from flask import request
from flask_restful import Resource
from sqlalchemy import and_, desc
from urllib.parse import urlparse

from app.models import DomainModels, IPModels, SiteModels, TaskModels
from app.modules.tools import *
from app.utils import db, fail_api, success_api, logger
from config import worker_task_list
import traceback

from .auth import auth_required

'''
展示任务列表，不包含改删操作
'''

# 停止指定celery任务
def stop_task(task_id):
    # 查询任务
    task = TaskModels.query.filter_by(task_id=task_id).first()
    # 先把任务状态改为pause
    task.task_status = 'paused'
    db.session.commit()

    # 查看当前任务在运行什么模块，通过模块名在worker_task_list中查找对应的任务，并revoke
    if task.task_running_module != 'finish' or task.task_running_module != 'error':
        msg = success_api(f'任务ID：{task_id}，不需要停止任务，直接重启')
        return msg

    if task.task_running_module not in worker_task_list.keys():
        task.task_status = 'error'
        db.session.commit()
        msg = fail_api(f'任务ID：{task_id}，任务状态错误，未找到模块{task.task_running_module}')
    
    for module_name in worker_task_list.keys():
        if task.task_running_module == module_name:
            try:
                try:
                    worker_task_list[module_name].revoke(terminate=True)
                except:
                    pass
                # 动态调用kill函数
                kill_func = f"kill_{module_name}()"
                eval(kill_func)
                msg = success_api(f'任务ID：{task_id}，停止{module_name}任务成功')
            except Exception as e:
                msg = fail_api(f'任务ID：{task_id}，停止{module_name}任务失败，错误信息：{str(e)}')
    return msg
    
def check_is_doamin_or_ip(task_target_list):
        '''
        检查任务的目标是域名还是ip，并分类
        支持格式：
        example.com
        127.0.0.1-127.0.0.9
        127.0.0.1/24
        '''
        task_ip = []
        task_domain = []

        for target in task_target_list:
            target = target.strip()
            try:
                # 判断是否为127.0.0.1-127.0.0.3之类的模式
                target = target.replace(' ', '')
                if '-' in target and len(target.split('-')) == 3 and netaddr.IPAddress(target.split('-')[0]) and netaddr.IPAddress(target.split('-')[2]):
                    task_ip.append(target)
                elif netaddr.IPNetwork(target):
                    task_ip.append(target)
            except:
                try:
                    url = urlparse(target)
                    # 不加http的时候，netloc返回的是空
                    if url.netloc:
                        task_domain.append(url.netloc)
                    else:
                        task_domain.append(url.path)
                except Exception as e:
                    print("checkIsDoaminOrIp error")
                    print(str(e))
        # 去重
        task_domain = list(set(task_domain))
        task_ip = list(set(task_ip))
        return task_domain, task_ip

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
                'task_module_list': item.task_module_list,
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
        task_target_domain, task_target_ip = check_is_doamin_or_ip(task_target.split('\n'))



        task_target = json.dumps(task_target.split('\n'))
        task_module_list = request.json.get('task_module_list')
        # "task_module_list":[{"module":"oneforall"},{"module":"scaninfo"},{"module":"scaninfo"}]
        task_module_list = [module_dict['module'] for module_dict in task_module_list]

        # 如果input_port_limit不为空，则将其赋值给task_port_limit
        input_port_limit = request.json.get('input_port_limit')
        if input_port_limit != None and input_port_limit != '':
            task_port_limit = input_port_limit.replace(' ','')
        else:
            task_port_limit = request.json.get('select_port_limit')

        # 设置task_next_module为task_module_list的第一项
        task_next_module = task_module_list[0]
        
        taskModel.task_id = task_id
        taskModel.task_name = request.json.get(
            'task_name').strip().replace(' ', '_')
        taskModel.task_target = str(task_target)
        taskModel.task_target_domain = json.dumps(task_target_domain)
        taskModel.task_target_ip = json.dumps(task_target_ip)
        taskModel.task_module_list = json.dumps(task_module_list)
        taskModel.task_running_module ='waiting'
        taskModel.task_next_module = task_next_module
        taskModel.task_status = 'waiting'
        taskModel.task_start_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        taskModel.task_port_limit = task_port_limit

        try:
            db.session.add(taskModel)
            db.session.commit()
            return success_api(message='添加成功')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return fail_api(message='添加失败')


class TaskDeleteResource(Resource):

    @auth_required
    def get(self, task_id):
        # 先中断正在进行的任务，再对任务进行删除
        msg = stop_task(task_id)
        if msg['status'] == 400:
            return msg
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
            return fail_api('删除失败，数据库错误')

'''
任务状态操作，包含启动、暂停
'''

class TaskStatusResource(Resource):

    @auth_required
    def get(self):
        try:
            if request.args.get('task_status') == 'paused':
                TaskModels.query.filter_by(task_id=request.args.get('task_id')).update({'task_status': 'waiting'})
                db.session.commit()
                logger.info("[+] 任务{}启动成功".format(request.args.get('task_id')))
                return success_api('启动成功')
            elif request.args.get('task_status') == 'running': 
                msg = stop_task(request.args.get('task_id'))
                if msg['status'] == 400:
                    return msg
                logger.info("[+] 任务{}暂停成功".format(request.args.get('task_id')))
                return success_api('暂停成功')
            else:
                msg = stop_task(request.args.get('task_id'))
                if msg['status'] == 400:
                    return msg
                # 更新数据库中的任务状态
                time.sleep(2)
                task = TaskModels.query.filter_by(task_id=request.args.get('task_id')).first()
                task_module_list = json.loads(task.task_module_list)
                task.task_running_module = 'waiting'
                task.task_next_module = task_module_list[0]
                task.task_status = 'waiting'
                db.session.commit()
                logger.info("[+] 任务{}重启成功".format(request.args.get('task_id')))
                return success_api('重启成功')
        except Exception as e:
            traceback.print_exc()
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
