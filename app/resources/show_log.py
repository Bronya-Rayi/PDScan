from flask_restful import Resource
from app.utils import success_api, fail_api
from .auth import auth_required
from app.modules.tools import tail
import config
import os

class ShowLogResource(Resource):

    def getToolsLog(self):
        oneforall_log= tail(config.ONEFORALL_LOG_PATH, 10)

        scaninfo_log = tail(config.SCANINFO_LOG_PATH,10)

        crawlergo_log = tail(config.CRAWLERGO_LOG_PATH,10)

        xray_log = tail(config.XRAY_LOG_PATH,10)
        return [oneforall_log,scaninfo_log,crawlergo_log,xray_log]

    def getSystemProcessLog(self):
        system_process = os.popen('ps -axo user,%cpu,%mem,command').read()
        return system_process

    def getSystemStatusLog(self):
        process_log_path = config.SYSTEM_STATUS_LOG_PATH
        log = tail(process_log_path, 15)

        return log

    @auth_required    
    def get(self):
        tools_log = self.getToolsLog()
        system_process = self.getSystemProcessLog()
        system_status_log = self.getSystemStatusLog()
        data ={
            'oneforall_log':tools_log[0],
            'scaninfo_log':tools_log[1],
            'crawlergo_log':tools_log[2],
            'xray_log':tools_log[3],
            'system_process':system_process,
            'system_status_log':system_status_log

        }
        return success_api(data=data)


