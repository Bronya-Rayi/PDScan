import json
from urllib.parse import urlparse

import netaddr
from app.utils.log import logger
from flask import current_app
from app.models import TaskModels

from app.utils import db


class TaskManager(object):
    def __init__(self, task_id, task_name, task_target,task_running_module=''):
        self.task_id = task_id
        self.task_name = task_name
        self.task_target_list = json.loads(task_target)
        self.task_running_module = task_running_module
        self.task_domain = []
        self.task_ip = []
        self.c_duan = ''
        self.checkIsDoaminOrIp()
        self.startTask()

    def startTask(self):
        '''
        任务开始的入口点暂定就两个
        如果输入的是域名，就进行子域名的任务
        如果输入的是ip，就进行端口扫描的任务
        如果指定了入口点任务，就按照指定的开始运行
        '''
        logger.info("[+] 任务：%s 开始执行" % self.task_name)
        # 先进行子域名的任务
        if self.task_running_module == 'subdomain' or (self.task_running_module == 'waitting' and self.task_domain):
            self.task_running_module = 'subdomain'
            # 开始子域名任务
            self.startSubdomainTask()
        elif self.task_running_module == 'portscan' or (self.task_running_module == 'waitting' and self.task_ip):
            self.task_running_module = 'portscan'
            # 开始端口扫描任务
            self.startPortScanTask()
        elif self.task_running_module == 'webfind':
            self.task_running_module = 'webfind'
            # 开始web网站查找任务
            self.startWebfindTask()
        else:
            logger.info("[-] 任务：%s 未发现ip或域名，无法执行" % self.task_name)
            TaskModels.query.filter_by(task_id=self.task_id).update(
                {'task_running_module': 'input_error', 'task_status': 'Error'})
            db.session.commit()

    def stopTask(task_id):
        task = TaskModels.query.filter_by(task_id=task_id).first()
        task_running_module = task.task_running_module.split('_')[0]
        # 根据不同的任务类型，调用不同的中断方法
        if task_running_module == 'subdomain':
            current_app.TaskQueue.stopSubdomain()
        elif task_running_module == 'portscan':
            current_app.TaskQueue.stopPortscan()
        elif task_running_module == 'webfind':
            current_app.TaskQueue.stopWebfind()
        elif task_running_module == 'vulscan':
            current_app.TaskQueue.stopVulscan()
        return task_running_module

    def checkIsDoaminOrIp(self):
        '''
        检查任务的目标是域名还是ip，并分类
        支持格式：
        example.com
        127.0.0.1-127.0.0.9
        127.0.0.1/24
        '''
        for target in self.task_target_list:
            target = target.strip()
            try:
                # 判断是否为127.0.0.1-127.0.0.3之类的模式
                target = target.replace(' ', '')
                if '-' in target and len(target.split('-')) == 3 and netaddr.IPAddress(target.split('-')[0]) and netaddr.IPAddress(target.split('-')[2]):
                    self.task_ip.append(target)
                elif netaddr.IPNetwork(target):
                    self.task_ip.append(target)
            except:
                try:
                    url = urlparse(target)
                    # 不加http的时候，netloc返回的是空
                    if url.netloc:
                        self.task_domain.append(url.netloc)
                    else:
                        self.task_domain.append(url.path)
                except Exception as e:
                    print("checkIsDoaminOrIp Error")
                    print(str(e))
        # 去重
        self.task_domain = list(set(self.task_domain))
        TaskModels.query.filter_by(task_id=self.task_id).update({'task_target_domain': json.dumps(
            self.task_domain), 'task_target_ip': json.dumps(self.task_ip)})
        db.session.commit()

    def startSubdomainTask(self):
        '''
        开始子域名任务
        '''
        # 先查询是否有子域名任务正在运行
        task_info = TaskModels.query.filter_by(
            task_running_module='subdomain', task_status='Running').first()
        if task_info:
            logger.info("任务：%s 进入子域名查询队列" % self.task_name)
            # 先更新任务模组为子域名查询，然后任务状态为等待
            TaskModels.query.filter_by(task_id=self.task_id).update(
                {'task_running_module': 'subdomain', 'task_status': 'Waiting'})
        else:
            # 更新任务模组为自域名查询，状态为运行中
            logger.info("任务：%s 开始进行子域名查询" % self.task_name)
            TaskModels.query.filter_by(task_id=self.task_id).update(
                {'task_running_module': 'subdomain', 'task_status': 'Running'})
        db.session.commit()

    def startPortScanTask(self):
        '''
        开始端口扫描任务
        '''
        # 先查询是否有端口扫描任务正在运行
        task_info = TaskModels.query.filter_by(
            task_running_module='portscan', task_status='Running').first()
        if task_info:
            logger.info("任务：%s 进入端口扫描队列" % self.task_name)
            # 先更新任务模组为端口扫描，然后任务状态为等待
            TaskModels.query.filter_by(task_id=self.task_id).update(
                {'task_running_module': 'portscan', 'task_status': 'Waiting'})
        else:
            # 更新任务模组为端口扫描，状态为运行中
            logger.info("任务：%s 开始进行端口扫描" % self.task_name)
            TaskModels.query.filter_by(task_id=self.task_id).update(
                {'task_running_module': 'portscan', 'task_status': 'Running'})
        db.session.commit()

    def startWebfindTask(self):
        '''
        开始web网站查找任务
        '''
        # 先查询是否有web网站查找任务正在运行
        task_info = TaskModels.query.filter_by(
            task_running_module='webfind', task_status='Running').first()
        if task_info:
            logger.info("任务：%s 进入web网站查找队列" % self.task_name)
            # 先更新任务模组为web网站查找，然后任务状态为等待
            TaskModels.query.filter_by(task_id=self.task_id).update(
                {'task_running_module': 'webfind', 'task_status': 'Waiting'})
        else:
            # 更新任务模组为web网站查找，状态为运行中
            logger.info("任务：%s 开始进行web网站查找" % self.task_name)
            TaskModels.query.filter_by(task_id=self.task_id).update(
                {'task_running_module': 'webfind', 'task_status': 'Running'})
        db.session.commit()
