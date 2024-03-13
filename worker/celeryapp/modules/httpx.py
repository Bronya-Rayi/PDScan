from utils import db
from models import TaskModels, DomainModels, SiteModels, ToolConfModels
from modules.tools import out_file_cmd_exec
# import config
import json
import os
import tld


def httpx_module(task_id):
    print(f'[+] httpx_module正在运行，任务ID: {task_id}')
    httpx_conf = ToolConfModels.query.filter_by(tool_name='httpx').first()
    httpx_cmd = httpx_conf.tool_cmd
    httpx_log_path = httpx_conf.tool_log_path
    httpx_result_path = httpx_conf.tool_result_path
    httpx_update_sh = httpx_conf.tool_update_sh

    httpx_task = TaskModels.query.filter_by(task_id=task_id).first()

    # 开始httpx模块任务，注意任务一开始的域名和ip也要加进去，为了后期漏扫做准备
    subdomain_db = DomainModels.query.filter_by(task_id=httpx_task.task_id)

    site_list = []
    if subdomain_db.count() > 0:
        subdomain_db = subdomain_db.all()
        site_list = [subdomain.domain for subdomain in subdomain_db]

    site_list.append(httpx_task.task_target)

    site_list = list(set(site_list))

    target_file = httpx_result_path + httpx_task.task_id + '.txt'
    with open(target_file, 'w') as f:
        for site in site_list:
            f.write(site + '\n')

    result_file = httpx_result_path + httpx_task.task_id + '.json'
    # 清除站点扫描的日志
    os.system("echo '' > {}".format(httpx_log_path))
    cmd = httpx_cmd.format(target_file=target_file, result_file=result_file)
    cmd_result = out_file_cmd_exec(cmd, httpx_log_path)

    if cmd_result == 0:
        print(f"[+] 任务：{task_id} 开始读取httpx模块结果")
        httpx_result = []
        with open(result_file, 'r', encoding='utf-8') as f:
            for i in f.readlines():
                httpx_result.append(json.loads(i))
        # 将结果插入数据库
        if len(httpx_result) == 0:
            print("[!] 任务：{} 的httpx模块入库完成，但没有发现子域名或站点".format(task_id))
            return True

        for result in httpx_result:
            if 'title' not in result:
                result['title'] = ''
            if 'webserver' not in result:
                result['webserver'] = ''

            site_db = SiteModels(task_id=httpx_task.task_id,
                                 url=result['url'],
                                 ip=result['host'],
                                 status_code=result['status_code'],
                                 title=result['title'],
                                 finger=result['webserver'])
            db.add(site_db)
            db.commit()
        print("[+] 任务：{} httpx模块结果入库完成".format(task_id))
    else:
        print(
            "[!] 任务：{} 的httpx模块结果数据入库失败，运行httpx期间出现错误，subprocess返回值不为0".format(
                task_id))
