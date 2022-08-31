from flask import request
from flask_restful import Resource
from sqlalchemy import desc
from flask_login import current_user
from service.task_manager import TaskManager
from common.utils.http import fail_api, success_api, table_api
from extensions import db
from models import DomainModels, IPModels, SiteModels ,TaskModels
import html
import json

class ShowSiteResult(Resource):

    def get(self,task_id):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        page = request.args.get('page', type=int)
        limit = request.args.get('limit', type=int)
        site_result = SiteModels.query.filter(SiteModels.task_id.like("%{}%".format(task_id))).paginate(page=page,per_page=limit,error_out=False)
        data = [
            {
                'task_id': item.task_id,
                'url': item.url,
                'ip': item.ip,
                'status_code': item.status_code,
                'title': item.title,
                'finger': item.finger,
            } for item in site_result.items
        ]
        site_total = SiteModels.query.filter(SiteModels.task_id.like("%{}%".format(task_id))).count()
        return table_api(result={'items': data,
                                 'total': site_total, },
                         code=0)

class ShowSubdomainResult(Resource):

    def get(self,task_id):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        page = request.args.get('page', type=int)
        limit = request.args.get('limit', type=int)
        domain_result = DomainModels.query.filter(DomainModels.task_id.like("%{}%".format(task_id))).paginate(page=page,per_page=limit,error_out=False)
        data = [
            {
                'domain': item.domain,
                'domain_record': item.domain_record,
                'task_id': task_id,
            } for item in domain_result.items
        ]
        domain_total = DomainModels.query.filter(DomainModels.task_id.like("%{}%".format(task_id))).count()
        return table_api(result={'items': data,
                                 'total': domain_total, },
                         code=0)


class ShowPortScanResult(Resource):

    def get(self,task_id):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        page = request.args.get('page', type=int)
        limit = request.args.get('limit', type=int)
        portscan_result = IPModels.query.filter(IPModels.task_id.like("%{}%".format(task_id))).order_by(IPModels.ip).paginate(page=page,per_page=limit,error_out=False)
        data = [
            {
                'ip': item.ip,
                'port': item.port,
                'service': item.service,
                'banner': "<pre> " + html.escape(item.banner[0:50]) + "</pre>",
            } for item in portscan_result.items
        ]
        portscan_total = IPModels.query.filter(IPModels.task_id.like("%{}%".format(task_id))).count()
        return table_api(result={'items': data,
                                 'total': portscan_total, },
                         code=0)



class ShowCDuanResult(Resource):

    def get(self,task_id):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        page = request.args.get('page', type=int)
        limit = request.args.get('limit', type=int)
        cduan_result = TaskModels.query.filter(TaskModels.task_id.like("%{}%".format(task_id))).order_by(TaskModels.task_id).paginate(page=page,per_page=limit,error_out=False)
        data = [
            {
                'task_id': item.task_id,
                'task_name': item.task_name,
                'task_c_duan': item.task_c_duan,
            } for item in cduan_result.items
        ]
        cduan_total = TaskModels.query.filter(TaskModels.task_id.like("%{}%".format(task_id))).count()

        # 转换成可以在前端显示的html
        target_html = ''
        for task in data:
            for target in json.loads(task['task_c_duan']):
                target_html += '<li>' + target + '</li>'
            task['task_c_duan'] = target_html
            target_html = ''

        return table_api(result={'items': data,
                                 'total': cduan_total, },
                         code=0)