from flask_restful import Resource
from flask_login import current_user
from flask import current_app
from common.utils.task_manage import tail
from common.utils.http import fail_api, success_api
import config
import os
import time



class TaskLogResource(Resource):

    def log_format(self,log_List):
        log = ''
        for item in log_List:
            log += '<p>' + item + '</p>'
        return log

    def getToolsLog(self):
        oneforall_log_list = tail(config.ONEFORALL_LOG_PATH, 10).split('\n')
        oneforall_log = '<p> <span class="layui-badge layui-bg-blue">oneforall_log</span> </p>' + '<code>' + self.log_format(oneforall_log_list) + '</code>'

        httpx_log_list = tail(config.HTTPX_LOG_PATH,10).split('\n')
        httpx_log = '<p> <span class="layui-badge layui-bg-blue">httpx_log</span> </p>' + '<code>' + self.log_format(httpx_log_list) + '</code>'

        crawlergo_log_list = tail(config.CRAWLERGO_LOG_PATH,10).split('\n')
        crawlergo_log = '<p> <span class="layui-badge layui-bg-blue">crawlergo_log</span> </p>' + '<code>' + self.log_format(crawlergo_log_list) + '</code>'

        xray_log_list = tail(config.XRAY_LOG_PATH,10).split('\n')
        xray_log = '<p> <span class="layui-badge layui-bg-blue">xray_log</span> </p>' + '<code>' + self.log_format(xray_log_list) + '</code>'
        return [oneforall_log,httpx_log,crawlergo_log,xray_log]

    def getSystemProcessLog(self):
        system_process_list = os.popen('ps -axo user,%cpu,%mem,command').read().split('\n')
        system_process = '<p> <span class="layui-badge layui-bg-blue">系统进程</span> </p>' + '<code>' + self.log_format(system_process_list) + '</code>'
        return system_process

    def getTaskProgressLog(self):
        process_log_path = config.ASSIGN_TASKS_LOG_PATH
        log_list = tail(process_log_path, 15).split('\n')
        log_details = ''
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_details = '<p> <span class="layui-badge layui-bg-blue">Time</span> <b>' + now + '</b> </p>' + '<code>'
        for i in log_list:
            log_details += '<p>' + i.strip() + '</p>'
        return log_details + '</code>'

    def get(self):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        oneforall_log,httpx_log,crawlergo_log,xray_log = self.getToolsLog()
        system_process = self.getSystemProcessLog()
        task_progress = self.getTaskProgressLog()
        
        return {"code":1,"subdomain_log": oneforall_log, "webfind_log": httpx_log, "crawlergo_log": crawlergo_log, "xray_log": xray_log, "system_process": system_process, "task_progress": task_progress}


class TaskRebootResource(Resource):

    def get(self):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        current_app.BackgroundTask.stopBackgroundTask()
        time.sleep(1)
        current_app.BackgroundTask.startBackgroundTask()

        return success_api(message="重启成功，重启后之前运行的任务会显示error，再重新运行任务即可")
