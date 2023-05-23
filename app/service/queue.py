import json
import os
import shlex
import subprocess
import threading
import time
from re import A

import IPy
import tld
from app.models import DomainModels, IPModels, SiteModels, TaskModels

import config
from app.utils import db
from app.utils.log import logger



def out_file_cmd_exec(cmd, file_path='log/tool.log'):
    '''执行命令并输出到文件
    :param cmd: 命令
    :param file_path: 文件路径
    :return: 返回执行结果
    '''
    with open(file_path, 'w') as f:
        if os.name == 'nt':
            pass
        else:
            cmd = shlex.split(cmd)
        p = subprocess.Popen(cmd, stdout=f, stderr=f).wait()
        return p


def tail(filepath, n):
    return os.popen("tail -n {} {}".format(n, filepath)).read()


def clear_oneforall_results():
    '''清除oneforall结果'''
    try:
        if os.name == 'nt':
            os.system('del /s /q /a ' + config.ONEFORALL_RESULTS_PATH)
        else:
            os.system('rm -rf ' + config.ONEFORALL_RESULTS_PATH)
    except Exception as e:
        print(e)
        return False

class TaskQueue(object):

    def __init__(self,app):
        # 这个是分配任务用的子线程的标志位
        self.app = app
        self.queue_thread_flag = False
        self.queue_thread = None

        self.subdomain_thread_flag = False
        self.portscan_thread_flag = False
        self.webfind_thread_flag = False

        self.vulscan = False
        self.vulscan_thread_flag = False
        
    '''
    后台开启子线程，分配任务
    '''
    def startTaskQueue(self):
        # 判断是否已经开启了分配任务的子线程
        if self.queue_thread_flag and self.queue_thread.is_alive():
            logger.info('[+] 后台任务已经开始')
        else:
            logger.info("[+] 后台任务正在启动")
            self.queue_thread_flag = True
            self.queue_thread = threading.Thread(target=self.assignModule)
            self.queue_thread.start()

    def stopTaskQueue(self):
        self.queue_thread_flag = False
        self.stopSubdomain()
        self.stopPortscan()
        self.stopWebfind()
        self.stopVulscan()
        self.queue_thread.join(5)
        logger.info("[-] 后台任务已经停止")
        return True

    def stopSubdomain(self):
        self.subdomain_thread_flag = False
        try:
            self.subdomain_thread.join(3)
            self.killSubdomain()
        except:
            pass
        logger.info("[-] 子域名线程已经停止")
        return True
    
    def stopPortscan(self):
        self.portscan_thread_flag = False
        try:
            self.portscan_thread.join(3)
            self.killPortscan()
        except:
            pass
        logger.info("[-] 端口扫描线程已经停止")
        return True

    def stopWebfind(self):
        self.webfind_thread_flag = False
        try:
            self.webfind_thread.join(3)
            self.killWebfind()
        except:
            pass
        logger.info("[-] 网站查找线程已经停止")
        return True

    def stopVulscan(self):
        self.vulscan_thread_flag = False
        try:
            self.vulscan_thread.join(5)
            self.killVulscan()
            self.killCrawlergo()
        except:
            pass
        logger.info("[-] 漏洞扫描线程已经停止")
        return True

    def killSubdomain(self):
        os.system(r"ps -ef |grep oneforall |grep -v grep |awk '{print $2}'|xargs kill -9")

    def killPortscan(self):
        os.system(r"ps -ef |grep scaninfo |grep -v grep |awk '{print $2}'|xargs kill -9")

    def killWebfind(self):
        os.system(r"ps -ef |grep httpx |grep -v grep |awk '{print $2}'|xargs kill -9")

    def killVulscan(self):
        os.system(r"ps -ef |grep xray |grep -v grep |awk '{print $2}'|xargs kill -9")

    def killCrawlergo(self):
        os.system(r"ps -ef |grep crawlergo |grep -v grep |awk '{print $2}'|xargs kill -9")
        os.system(r"ps -ef |grep chrome |grep -v grep |awk '{print $2}'|xargs kill -9")

    '''
    根据任务类型分配模块
    '''
    def assignModule(self):
        logger.info("[+] 后台任务启动成功")
        while self.queue_thread_flag == True:
            # 准备子域名任务
            if self.subdomain_thread_flag and self.subdomain_thread.is_alive():
                logger.info("[*] 子域名线程正在进行，队列任务排队中")
            else:
                self.subdomain_thread_flag = True
                self.subdomain_thread = threading.Thread(target=self.prepareSubdomain)
                self.subdomain_thread.start()

            # 准备端口扫描任务
            if self.portscan_thread_flag == True and self.portscan_thread.is_alive():
                logger.info("[*] 端口扫描线程正在进行，队列任务排队中")
            else:
                self.portscan_thread_flag = True
                self.portscan_thread = threading.Thread(target=self.preparePortscan)
                self.portscan_thread.start()

            # 准备网站查找任务
            if self.webfind_thread_flag == True and self.webfind_thread.is_alive():
                logger.info("[*] 网站查找线程正在进行，队列任务排队中")
            else:
                self.webfind_thread_flag = True
                self.webfind_thread = threading.Thread(target=self.prepareWebFind)
                self.webfind_thread.start()

            # 准备漏洞扫描任务
            if self.vulscan_thread_flag == True and self.vulscan_thread.is_alive():
                logger.info("[*] 漏洞扫描线程正在进行，队列任务排队中")
            else:
                self.vulscan_thread_flag = True
                self.vulscan_thread = threading.Thread(target=self.prepareVulscan)
                self.vulscan_thread.start()
            
            time.sleep(5)
        
                
    
    def prepareSubdomain(self):
        # 查询出需要进行子域名任务的任务
        # time.sleep(10)
        with self.app.app_context():
            # logger.info("子域名线程启动成功")
            domain_task = TaskModels.query.filter_by(task_status='running',task_running_module='subdomain')
            doamin_task_waiting = TaskModels.query.filter_by(task_status='waiting',task_running_module='subdomain')
            # print(domain_task.count())
            if domain_task.count() == 1:
                domain_task = domain_task.first()
                logger.info("[+] 队列读取完成，开始任务：{} 的子域名查询".format(domain_task.task_name))
                self.startSubdomain(domain_task)
            elif domain_task.count() > 1:
                logger.error("[!] 有两个子域名查询任务在运行，请检查！")
            elif doamin_task_waiting.count() > 0:
                # 读取等待中的任务，并且更新任务状态
                doamin_task_waiting = doamin_task_waiting.first()
                doamin_task_waiting.task_status = 'running'
                db.session.commit()
                logger.info("[+] 队列任务：{} 排队结束，更新状态为正在运行".format(doamin_task_waiting.task_name))
                domain_task = doamin_task_waiting
                logger.info("[+] 队列读取完成，开始任务：{} 的子域名查询".format(domain_task.task_name))
                self.startSubdomain(domain_task)

            # logger.info("子域名线程结束")
        self.subdomain_thread_flag = False

    def preparePortscan(self):
        # 查询出需要进行端口扫描任务的任务
        with self.app.app_context():
            # logger.info("端口扫描线程启动成功")
            portscanTask = TaskModels.query.filter_by(task_status='running',task_running_module='portscan')
            portscanTask_waiting = TaskModels.query.filter_by(task_status='waiting',task_running_module='portscan')
            if portscanTask.count() == 1:
                portscanTask = portscanTask.first()
                logger.info("[+] 队列读取完成，开始任务：{} 的端口扫描".format(portscanTask.task_name))
                self.startPortscan(portscanTask)
            elif portscanTask.count() > 1:
                logger.error("[!] 有两个端口扫描任务在运行，请检查！")
            elif portscanTask_waiting.count() > 0:
                # 读取等待中的任务，并且更新任务状态
                portscanTask_waiting = portscanTask_waiting.first()
                portscanTask_waiting.task_status = 'running'
                db.session.commit()
                portscan_task = portscanTask_waiting
                logger.info("[+] 队列读取完成，开始任务：{} 的端口扫描".format(portscan_task.task_name))
                self.startPortscan(portscan_task)
            
            # logger.info("端口扫描线程结束")
        self.portscan_thread_flag = False


    def prepareWebFind(self):
        # 查询出需要进行网站查找任务的任务
        with self.app.app_context():
            # logger.info("网站查找线程启动成功")
            webfindTask = TaskModels.query.filter_by(task_status='running',task_running_module='webfind')
            webfindTask_waiting = TaskModels.query.filter_by(task_status='waiting',task_running_module='webfind')
            if webfindTask.count() == 1:
                webfindTask = webfindTask.first()
                logger.info("[+] 队列读取完成，开始任务：{} 的网站查找".format(webfindTask.task_name))
                self.startWebFind(webfindTask)
            elif webfindTask.count() > 1:
                logger.error("[!] 有两个网站查找任务在运行，请检查！")
            elif webfindTask_waiting.count() > 0:
                # 读取等待中的任务，并且更新任务状态
                webfindTask_waiting = webfindTask_waiting.first()
                webfindTask_waiting.task_status = 'running'
                db.session.commit()
                webfind_task = webfindTask_waiting
                logger.info("[+] 队列读取完成，开始任务：{} 的网站查找".format(webfind_task.task_name))
                self.startWebFind(webfind_task)
            
        self.webfind_thread_flag = False

    def prepareVulscan(self):
        # 查询出需要进行漏洞扫描任务的任务
        with self.app.app_context():
            # logger.info("漏洞扫描线程启动成功")
            vulscanTask = TaskModels.query.filter_by(task_status='running',task_running_module='vulscan')
            vulscanTask_waiting = TaskModels.query.filter_by(task_status='waiting',task_running_module='vulscan')
            if vulscanTask.count() == 1:
                vulscanTask = vulscanTask.first()
                logger.info("[+] 队列读取完成，开始任务：{} 的漏洞扫描".format(vulscanTask.task_name))
                self.startVulscan(vulscanTask)
            elif vulscanTask.count() > 1:
                logger.error("[!] 有两个漏洞扫描任务在运行，请检查！")
            elif vulscanTask_waiting.count() > 0:
                # 读取等待中的任务，并且更新任务状态
                vulscanTask_waiting = vulscanTask_waiting.first()
                vulscanTask_waiting.task_status = 'running'
                db.session.commit()
                vulscan_task = vulscanTask_waiting
                logger.info("[+] 队列读取完成，开始任务：{} 的漏洞扫描".format(vulscan_task.task_name))
                self.startVulscan(vulscan_task)
        
        self.vulscan_thread_flag = False

    def startSubdomain(self,domain_task):
        try:
            # OneForAll接受域名列表
            domain_list = json.loads(domain_task.task_target_domain)
            for domain in domain_list:
                # 清除OneForAll的日志
                os.system("echo '' > {}".format(config.ONEFORALL_LOG_PATH))
                # 开始oneforall的查询
                logger.info("[+] 域名：{} 开始进行子域名查询".format(domain))
                cmd_result = out_file_cmd_exec(config.ONEFORALL_CMD.format(target_domain=domain), config.ONEFORALL_LOG_PATH)
                if cmd_result == 0:
                    # OneForAll的输出是以域名为名称的
                    logger.info("[+] 域名：{} 的子域名查询完成，开始读取结果".format(domain))
                    result_path = os.path.join(config.ONEFORALL_RESULTS_PATH, '{}.json'.format(tld.get_fld("http://"+domain)))
                    # 读过大的json可能会卡
                    with open(result_path,'r') as f:
                        results = json.load(f)
                    for result in results:
                        try:
                            # 如果解析的是cname，则读取cname的域名
                            if result['subdomain'] == result['cname']:
                                domain_db = DomainModels(task_id = domain_task.task_id,domain = result['subdomain'],domain_record = result['ip'])
                                db.session.add(domain_db)
                                db.session.commit()
                            else:
                                domain_db = DomainModels(domain = result['subdomain'],domain_record = result['cname'],task_id = domain_task.task_id)
                                db.session.add(domain_db)
                                db.session.commit()
                        except Exception as e:
                            logger.error("[!] 域名：{} 的子域名查询数据库入库失败：{}".format(domain,e))
                else:
                    logger.error("[!] 域名：{} 的子域名查询入库失败，运行OneForAll期间出现错误".format(domain))
                    continue
                logger.info("[+] 域名：{} 的子域名查询入库成功".format(domain))
            # 子域名任务完成后，更新任务状态
            domain_task.task_running_module = 'portscan'
            domain_task.task_status = 'waiting'
            db.session.commit()
            logger.info("[+] 任务：{} 的子域名查询入库完成".format(domain_task.task_name))
            logger.info("[+] 任务：{} 进入端口扫描队列".format(domain_task.task_name))
            return True
        except Exception as e:
            domain_task.task_running_module = 'subdomain_error'
            domain_task.task_status = 'Error'
            db.session.commit()
            logger.error("[!] 任务：{} 的子域名查询入库失败，后台任务调度出现错误:{}".format(domain_task.task_name,e))
        
    def startPortscan(self,portscan_task):
        scan_ports = config.SCAN_PORTS[portscan_task.task_port_limit]
        try:
            logger.info("[+] 任务：{} 开始进行C段整理".format(portscan_task.task_name))
            ip_list = json.loads(portscan_task.task_target_ip)
            c_duan = []
            # 将目标ip加入c段列表
            for ip in ip_list:
                # print(ip)
                if '-' in ip:
                    c_duan.append(str(IPy.IP(ip.split('-')[0]).make_net('255.255.255.0')))
                elif '/' in ip:
                    c_duan.append(ip)
                else:
                    c_duan.append(str(IPy.IP(ip).make_net('255.255.255.0')))
            
            # 查一查有无子域名扫描结果的ip，也加入c段和ip列表
            subdomain_ips = DomainModels.query.filter(DomainModels.task_id.like("%{}%".format(portscan_task.task_id)))
            # print(subdomain_ip.count())
            # 输入目标的c段计数，如果c段过多的话，在下面的端口扫描就需要分段进行，及时保存结果
            # count_target_c_duan = 0
            if subdomain_ips.count() > 0:
                subdomain_ips = subdomain_ips.all()
                for subdomain_ip in subdomain_ips:
                    try:
                        ip = subdomain_ip.domain_record
                        # print(ip)
                        if '-' in ip:
                            c_duan.append(str(IPy.IP(ip.split('-')[0]).make_net('255.255.255.0')))
                            ip_list.append(ip)
                        elif '/' in ip:
                            c_duan.append(ip)
                            ip_list.append(ip)
                            # count_target_c_duan += 1
                        else:
                            c_duan.append(str(IPy.IP(ip).make_net('255.255.255.0')))
                            ip_list.append(ip)
                    except Exception as e:
                        # CNAME不管了
                        continue
            
            # 列表去重
            c_duan = list(set(c_duan))
            ip_list = list(set(ip_list))
            # c段数据入库
            try:
                task_db = TaskModels.query.filter_by(task_id=portscan_task.task_id)
                task_db.update({"task_c_duan":json.dumps(c_duan)})
                db.session.commit()
            except Exception as e:
                logger.error(e)
                logger.info("[!] 任务：{} 的c段入库失败".format(portscan_task.task_name))
                portscan_task.task_running_module = 'portscan_error'
                portscan_task.task_status = 'Error'
                db.session.commit()
                logger.info("[!] 任务：{} 的端口扫描入库失败".format(portscan_task.task_name))
                return False

            # print(ip_list)
            logger.info("[+] 任务：{} 的C段整理和ip去重工作完成，开始端口扫描".format(portscan_task.task_name))

            # 端口扫描的日志和结果文件是一个
            result_file = os.path.join(config.SCANINFO_RESULTS_PATH, "portscan_result")
            os.system("echo '' > {}.txt".format(result_file))
            for ip in ip_list:
                # 开始端口扫描任务
                # 清空结果文件
                os.system("echo '' > {}.txt".format(result_file))
                logger.info("[+] IP：{} 开始端口扫描".format(ip))
                cmd = config.SCANINFO_CMD.format(target_ip = ip, ports = scan_ports, result_file = result_file)
                # print(config.SCANINFO_LOG_PATH)
                # print(cmd)
                cmd_result = out_file_cmd_exec(cmd, '/dev/null')
                # cmd_result = 0
                if cmd_result == 0:
                    logger.info("[+] IP:{} 端口扫描完成，开始读取结果".format(ip))
                    scaninfo_result = []
                    with open(result_file+".txt", 'r', encoding='utf-8') as f:
                        for i in f.readlines():
                            scaninfo_result.append(json.loads(i))
                    # 将结果插入数据库
                    if len(scaninfo_result) == 0:
                        logger.info("[!] IP：{} 的端口扫描完成，但没有发现开放端口".format(ip))
                        continue

                    for result in scaninfo_result:
                        if 'ip' in result:
                            try:
                                target_db = IPModels(
                                    task_id = portscan_task.task_id,
                                    ip = result['ip'],
                                    port = result['port'],
                                    service = result['service'],
                                    banner = result['Banner'],
                                    )
                                db.session.add(target_db)
                                db.session.commit()
                            except Exception as e:
                                logger.error(e)
                                logger.error("[!] IP:{} 的端口扫描入库失败".format(ip))
                        elif 'url' in result:
                            try:
                                target_db = SiteModels(
                                    task_id = portscan_task.task_id,
                                    url = result['url'],
                                    ip = result['url'].replace("http://","").replace("https://","").split("/")[0],
                                    status_code = result['StatusCode'],
                                    title = result['Title'],
                                    finger = result['HeaderDigest'] + "\n" + result['KeywordFinger'] + "\n" + result['HashFinger'],
                                    )
                                db.session.add(target_db)
                                db.session.commit()
                            except Exception as e:
                                logger.error(e)
                                logger.error("[!] IP：{} 的端口扫描入库失败".format(ip))
                    logger.info("[+] IP：{} 端口扫描结果入库完成".format(ip))
                else:
                    logger.error("[!] IP：{} 的端口扫描失败，端口扫描期间出现错误".format(ip))
                    continue
            # 端口扫描任务完成后，更新任务状态
            portscan_task.task_running_module = 'webfind'
            portscan_task.task_status = 'waiting'
            db.session.commit()
            logger.info("[+] 任务：{} 的端口扫描入库完成".format(portscan_task.task_name))
            logger.info("[+] 任务：{} 进入网站查询模块".format(portscan_task.task_name))
            return True
        except Exception as e:
            portscan_task.task_running_module = 'portscan_error'
            portscan_task.task_status = 'Error'
            db.session.commit()
            logger.error("[!] 任务：{} 的端口扫描入库失败".format(portscan_task.task_name))
            logger.error(str(e))
            return False
    
    def startWebFind(self, webfind_task):
        # 在这里检查当前任务是否有漏扫的步骤，关系到最后的状态更新
        if webfind_task.task_vulscan == '1':
            self.vulscan = True
        else:
            self.vulscan = False
            
        try:
            # 开始网站查找任务，注意任务一开始的域名和ip也要加进去，为了后期漏扫做准备
            subdomain_db = DomainModels.query.filter_by(task_id = webfind_task.task_id)
            task_target_domain_list = json.loads(webfind_task.task_target_domain)
            task_target_ip_list = json.loads(webfind_task.task_target_ip)
            subdomain_list = []
            if subdomain_db.count() > 0:
                subdomain_db = subdomain_db.all()
                subdomain_list = [subdomain.domain for subdomain in subdomain_db]
            
            site_list = subdomain_list + task_target_domain_list + task_target_ip_list
            site_list = list(set(site_list))

            target_file = os.path.join(config.HTTPX_PATH, webfind_task.task_id + '.txt')
            with open(target_file,'w') as f:
                for site in site_list:
                    f.write(site + '\n')

            result_file = os.path.join(config.HTTPX_RESULTS_PATH, webfind_task.task_id + '.json')
            # 清除站点扫描的日志
            os.system("echo '' > {}".format(config.HTTPX_LOG_PATH))
            cmd = config.HTTPX_CMD.format(target_file = target_file, result_file = result_file)
            cmd_result = out_file_cmd_exec(cmd, config.HTTPX_LOG_PATH)
            if cmd_result == 0:
                logger.info("开始读取网站查找结果")
                webfind_result = []
                with open(result_file, 'r', encoding='utf-8') as f:
                    for i in f.readlines():
                        webfind_result.append(json.loads(i))
                # 将结果插入数据库
                if len(webfind_result) == 0:
                    # 根据下一步是否有漏扫任务，更新任务状态
                    if self.vulscan:
                        webfind_task.task_running_module = 'vulscan'
                        webfind_task.task_status = 'waiting'
                        db.session.commit()
                        logger.info("[+] 任务：{} 的网站查找入库完成，但没有发现子域名或站点，开始漏洞扫描".format(webfind_task.task_name))
                        return True
                    else:
                        webfind_task.task_running_module = 'webfind_finish'
                        webfind_task.task_status = 'finish'
                        db.session.commit()
                        logger.error("[!] 任务：{} 的网站查找入库完成，但没有发现子域名或站点".format(webfind_task.task_name))
                        return True

                for result in webfind_result:
                    if 'title' not in result:
                        result['title'] = ''
                    if 'webserver' not in result:
                        result['webserver'] = ''
                    
                    site_db = SiteModels(
                        task_id = webfind_task.task_id,
                        url = result['url'],
                        ip = result['host'],
                        status_code = result['status_code'],
                        title = result['title'],
                        finger = result['webserver']
                    )
                    db.session.add(site_db)
                    db.session.commit()
                # 根据下一步是否有漏扫任务，更新任务状态
                if self.vulscan:
                    webfind_task.task_running_module = 'vulscan'
                    webfind_task.task_status = 'waiting'
                    db.session.commit()
                    logger.info("[+] 任务：{} 的网站查找入库完成，开始漏洞扫描".format(webfind_task.task_name))
                    return True
                else:
                    webfind_task.task_running_module = 'webfind_finish'
                    webfind_task.task_status = 'finish'
                    db.session.commit()
                    logger.info("[+] 任务：{} 的网站查找完成".format(webfind_task.task_name))
                    return True
            else:
                webfind_task.task_running_module = 'webfind_error'
                webfind_task.task_status = 'Error'
                db.session.commit()
                logger.error("[!] 任务：{} 的网站查找入库失败，运行httpx期间报错".format(webfind_task.task_name))
                return False


        except Exception as e:
            webfind_task.task_running_module = 'webfind_error'
            webfind_task.task_status = 'Error'
            db.session.commit()
            logger.error("[!] 任务：{} 的网站查找入库失败".format(webfind_task.task_name))
            logger.error(str(e))
            return False

    def startVulscan(self, vulscan_task):
        # 启动xray
        # 用任务id和当前时间作为文件名
        result_file_name = vulscan_task.task_id + '_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.html'
        result_file_path = os.path.join(config.XRAY_RESULTS_PATH, result_file_name)
        cmd = config.XRAY_CMD.format(xray_proxy = config.XRAY_PROXY, result_file = result_file_path)
        xray_thread = threading.Thread(target=out_file_cmd_exec, args=(cmd, config.XRAY_LOG_PATH,))
        xray_thread.start()
        # 将xray的结果文件目录添加至数据库
        task_xray_result_now = "/xray_results/" + result_file_name

        # 查找以前数据库中记录的xray结果文件，将其与当前结果文件合并成列表
        task_xray_result = vulscan_task.task_xray_result
        if task_xray_result:
            task_xray_result = json.loads(task_xray_result)
            task_xray_result.append(task_xray_result_now)
        else:
            task_xray_result = [task_xray_result_now]


        TaskModels.query.filter_by(task_id = vulscan_task.task_id).update({"task_xray_result": json.dumps(task_xray_result)})
        db.session.commit()
        

        def wait_xray_ok(xray_log_path,xray_wait_time):
            cmd = '''
                wc {0} | awk '{{print $1}}';
                sleep 5;
                wc {0} | awk '{{print $1}}';
            '''.format(xray_log_path)
            result = os.popen(cmd).read()

            if result.split('\n')[0] == result.split('\n')[1]:
                cmd = "tail -n 10 {}".format(xray_log_path)
                s = os.popen(cmd).read()

                if "All pending requests have been scanned" in s:
                    os.system('echo "" > {}'.format(xray_log_path))
                    return True
                if xray_wait_time == 2:
                    return True

            return False

        try:
            # 先从数据库中将识别出的站点导出到漏洞扫描的目标文件中
            site_db = SiteModels.query.filter_by(task_id = vulscan_task.task_id).all()
            if len(site_db) == 0:
                vulscan_task.task_running_module = 'vulscan_error'
                vulscan_task.task_status = 'Error'
                logger.error("[!] 任务：{} 没有站点，无法进行漏洞扫描".format(vulscan_task.task_name))
                db.session.commit()
                self.killVulscan()
                return False
            for site in site_db:
                logger.info("[+] 正在爬取：{}".format(site.url))
                cmd = config.CRAWLERGO_CMD.format(xray_proxy = config.XRAY_PROXY, target = site.url)
                result = out_file_cmd_exec(cmd, config.CRAWLERGO_LOG_PATH)
                if result == 0:
                    logger.info("[+] 爬取成功：{}，开始漏扫".format(site.url))
                    # 等待xray结束
                    xray_wait_time = 0
                    while not wait_xray_ok(config.XRAY_LOG_PATH,xray_wait_time):
                        xray_wait_time += 1
                else:
                    vulscan_task.task_running_module = 'vulscan_error'
                    vulscan_task.task_status = 'Error'
                    logger.error("[!] 任务：{} 漏洞扫描失败,crawlergo运行期间出错".format(vulscan_task.task_name))
                    db.session.commit()
                    self.killVulscan()
                    return False
                logger.info("[+] 漏洞扫描完成：{} ，开始进行下一项漏扫".format(site.url))
            # 漏扫结束
            logger.info("[+] 任务：{} 漏扫完成，正在关闭xray和crawlergo".format(vulscan_task.task_name))
            self.killVulscan()
            self.killCrawlergo()
            vulscan_task.task_running_module = 'vulscan_finish'
            vulscan_task.task_status = 'finish'
            db.session.commit()
            logger.info("[+] 任务：{} 的漏洞扫描完成".format(vulscan_task.task_name))
            self.killVulscan()
            return True
                
        except Exception as e:
            vulscan_task.task_running_module = 'vulscan_error'
            vulscan_task.task_status = 'Error'
            db.session.commit()
            logger.error(e)
            logger.error("[!] 任务：{} 的漏洞扫描出现错误".format(vulscan_task.task_name))
            self.killVulscan()
            return False
            
