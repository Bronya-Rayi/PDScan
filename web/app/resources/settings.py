from flask import request
from flask_restful import Resource
from sqlalchemy import and_, desc

from app.models import ToolConfModels
from app.utils import db, fail_api, success_api

from .auth import auth_required

class ToolsConfResource(Resource):

    @auth_required
    def get(self):
        tool_name = request.args.get('tool_name')
        tools_conf_list = ToolConfModels.query.filter_by(tool_name=tool_name).first()
        data = {
                'tool_cmd': tools_conf_list.tool_cmd,
                'tool_log_path': tools_conf_list.tool_log_path,
                'tool_result_path': tools_conf_list.tool_result_path,
                'tool_update_sh': tools_conf_list.tool_update_sh,
                'tool_others': tools_conf_list.tool_others
        }

        return success_api(data=data)

    @auth_required
    def post(self):

        tool_name = request.args.get('tool_name')
        tool_cmd = request.json.get('tool_cmd')
        tool_log_path = request.json.get('tool_log_path')
        tool_result_path = request.json.get('tool_result_path')
        tool_update_sh = request.json.get('tool_update_sh')
        tool_others = request.json.get('tool_others')

        ToolConfModel = ToolConfModels.query.filter_by(tool_name=tool_name).first()
        ToolConfModel.tool_cmd = tool_cmd
        ToolConfModel.tool_log_path = tool_log_path
        ToolConfModel.tool_result_path = tool_result_path
        ToolConfModel.tool_update_sh = tool_update_sh
        ToolConfModel.tool_others = tool_others

        try:
            db.session.commit()
            db.session.close()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            db.session.close()
            return fail_api(message='更新失败，数据库错误：' + str(e))
            
        return success_api(message='更新成功')

