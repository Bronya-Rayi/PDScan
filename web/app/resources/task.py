import hashlib
import json
import time
import uuid
import netaddr

from flask import request
from flask_restful import Resource
from sqlalchemy import and_, desc
from urllib.parse import urlparse

from app.models import DomainModels, IPModels, SiteModels, TaskModels, SitePathScanModels, ToolXrayModels
from app.utils import db, fail_api, success_api, logger
import traceback

from .auth import auth_required



def check_is_doamin_or_ip(target):
    '''
    检查任务的目标是域名还是ip
    支持格式：
    example.com
    127.0.0.1-127.0.0.9
    127.0.0.1/24
    '''
    target = target.strip()
    try:
        # 判断是否为127.0.0.1-127.0.0.3之类的模式
        target = target.replace(' ', '')
        if '-' in target and len(target.split('-')) == 3 and netaddr.IPAddress(target.split('-')[0]) and netaddr.IPAddress(target.split('-')[2]):
            return ["ip",target]
        elif netaddr.IPNetwork(target):
            return ["ip",target]
    except:
        try:
            url = urlparse(target)
            # 不加http的时候，netloc返回的是空
            if url.netloc:
                return ["domain",url.netloc]
            else:
                return ["domain",url.path]
        except Exception as e:
            print("checkIsDoaminOrIp error")
            print(str(e))
            return ["error",""]


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

        out_data = {
            "items": data,
            "total": task_list_total
        }

        return success_api(data=out_data)

    @auth_required
    def post(self):

        task_name = request.json.get(
                'task_name').strip().replace(' ', '_')

        task_targets = request.json.get('task_targets')
        task_module_list = request.json.get('task_module_list')
        # "task_module_list":[{"module":"oneforall"},{"module":"scaninfo"},{"module":"scaninfo"}]
        task_module_list = [module_dict['module'] for module_dict in task_module_list]
        # task_portscan_range
        input_portscan_range = request.json.get('input_portscan_range')
        if input_portscan_range != None and input_portscan_range != '':
            task_portscan_range = input_portscan_range.replace(' ','')
        else:
            task_portscan_range = request.json.get('select_portscan_range')

        task_target_list = task_targets.split('\n')
        for target in task_target_list:
            check_result = check_is_doamin_or_ip(target)
            if check_result[0] == "error":
                return fail_api(message="输入目标格式错误！")
        for target in task_target_list:
            task_id = hashlib.md5(str(uuid.uuid4()).encode('utf8')).hexdigest()[:10]
            check_result = check_is_doamin_or_ip(target)
            target = check_result[1]
            target_type = check_result[0]
            taskModel = TaskModels()
            taskModel.task_id = task_id
            taskModel.task_name = task_name
            taskModel.task_target = target
            taskModel.task_target_type = target_type
            taskModel.task_module_list = json.dumps(task_module_list)
            taskModel.task_running_module ='waiting'
            taskModel.task_portscan_range = task_portscan_range
            taskModel.task_status = 'waiting'
            taskModel.task_start_time = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime())
            taskModel.task_portscan_range = task_portscan_range

            try:
                db.session.add(taskModel)
                db.session.commit()
                db.session.close()
            except Exception as e:
                print(str(e))
                db.session.rollback()
                db.session.close()
                return fail_api(message='添加失败，数据库错误：' + str(e))

        return success_api(message='添加成功')


class TaskDeleteResource(Resource):

    @auth_required
    def get(self):
        # 先中断正在进行的任务，再对任务进行删除
        # 先把状态改为wait_for_kill，等待kill
        # 数据库中Task表由worker停止任务后自行删除
        task_id = request.args.get('task_id')

        task = TaskModels.query.filter_by(task_id=task_id).first()
        task.task_status = 'wait_for_delete'
        db.session.commit()

        try:
            domainModel = DomainModels.query.filter_by(task_id=task_id).delete()
            ipModel = IPModels.query.filter_by(task_id=task_id).delete()
            siteModel = SiteModels.query.filter_by(task_id=task_id).delete()
            SitePathScanModel = SitePathScanModels.query.filter_by(task_id=task_id).delete()
            ToolXrayModel = ToolXrayModels.query.filter_by(task_id=task_id).delete()

            db.session.commit()
            db.session.close()
            return success_api('删除成功，任务刷新可能延迟')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            db.session.close()
            return fail_api('删除失败，数据库错误：' + str(e))

'''
任务状态操作，包含启动、暂停
'''

class TaskStatusResource(Resource):

    @auth_required
    def get(self):
        try:
            if request.args.get('task_status') == 'stop':
                task = TaskModels.query.filter_by(task_id=request.args.get('task_id')).first()
                task.task_status = 'waiting'
                db.session.commit()
                logger.info("[+] 任务{}正在重启".format(request.args.get('task_id')))
                return success_api('正在重启任务，请稍等后刷新查看状态')
            
            elif request.args.get('task_status') == 'running':
                task = TaskModels.query.filter_by(task_id=request.args.get('task_id')).first()
                task.task_status = 'wait_for_stop'
                db.session.commit()
                logger.info("[+] 任务{}暂停成功".format(request.args.get('task_id')))
                return success_api('正在暂停任务，请稍等后刷新查看状态')
            
            elif request.args.get('task_status') == 'error':
                task = TaskModels.query.filter_by(task_id=request.args.get('task_id')).first()
                task.task_running_module = 'waiting'
                task.task_status = 'waiting'
                db.session.commit()
                logger.info("[+] 任务{}错误，正在重启".format(request.args.get('task_id')))
                return success_api('正在重启错误任务，请稍等后刷新查看状态')
            
            elif request.args.get('task_status') == 'finish':
                task = TaskModels.query.filter_by(task_id=request.args.get('task_id')).first()
                task.task_status = 'waiting'
                db.session.commit()
                logger.info("[+] 任务{}正在重启".format(request.args.get('task_id')))
                return success_api('正在重启任务，请稍等后刷新查看状态')
        except Exception as e:
            traceback.print_exc()
            db.session.rollback()
            return fail_api('操作失败')

'''
任务详情展示
'''


class ShowSiteResult(Resource):

    @auth_required
    def get(self):
        page = request.args.get('page', type=int)
        perPage = request.args.get('perPage', type=int)
        task_id = request.args.get('task_id')

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
    def get(self):
        task_id = request.args.get('task_id')
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


class ShowIPResult(Resource):

    @auth_required
    def get(self):
        task_id = request.args.get('task_id')
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

        ip_result = IPModels.query.filter(query_rule).paginate(
            page=page, per_page=perPage, error_out=False)
        ip_total = IPModels.query.filter(query_rule).count()

        data = [
            {
                'ip': item.ip,
                'port': item.port,
                'service': item.service,
                'banner': item.banner[0:50],
            } for item in ip_result.items
        ]

        out_data = {
            "items": data,
            "total": ip_total
        }
        return success_api(data=out_data)


class ShowCDuanResult(Resource):

    @auth_required
    def get(self):
        task_id = request.args.get('task_id')
        try:
            cduan_result = TaskModels.query.filter(TaskModels.task_id.like("%{}%".format(task_id))).first().task_c_duan
            result_list = json.loads(cduan_result)
        except:
            result_list = ["无C段"]
        result_html = ''
        for i in result_list:
            result_html += i + '\n'

        out_data = {"c_duan": result_html}
        return success_api(data=out_data)

class ShowVulscanResult(Resource):

    @auth_required
    def get(self):
        task_id = request.args.get('task_id')
        if task_id == 'all':
            task_id = ''

        vulscan_result_db = ToolXrayModels.query.filter(ToolXrayModels.task_id.like("%{}%".format(task_id))).all()
        vulscan_result = [ row.result_path for row in vulscan_result_db]

        if vulscan_result == []:
            return fail_api(message="未扫描到漏洞")
        data = [
            {
                'xray_result_url': item,
            } for item in vulscan_result
        ]
        out_data = {
            "items": data
        }
        return success_api(data=out_data)


class ShowSitePathScanResult(Resource):

    @auth_required
    def get(self):
        task_id = request.args.get('task_id')
        page = request.args.get('page', type=int)
        perPage = request.args.get('perPage', type=int)

        if task_id == 'all':
            task_id = ''

        query_rule = and_(
            SitePathScanModels.task_id.like("%{}%".format(task_id)),
            SitePathScanModels.url.like("%{}%".format(request.args.get('url', type=str)))
        )

        site_path_scan_result = SitePathScanModels.query.filter(query_rule).paginate(
            page=page, per_page=perPage, error_out=False)
        site_path_scan_total = SitePathScanModels.query.filter(query_rule).count()

        data = [
            {
                'id': item.id,
                'url': item.url
            } for item in site_path_scan_result.items
        ]

        out_data = {
            "items": data,
            "total": site_path_scan_total
        }
        return success_api(data=out_data)