from models import TaskModels, DomainModels, ToolConfModels
from utils import db
from modules.tools import out_file_cmd_exec
# import config
import json
import os
import tld


def oneforall_module(task_id):
    print(f'[+] oneforall_module正在运行，任务ID: {task_id}')
    oneforall_conf = ToolConfModels.query.filter_by(
        tool_name='oneforall').first()
    oneforall_cmd = oneforall_conf.tool_cmd
    oneforall_log_path = oneforall_conf.tool_log_path
    oneforall_result_path = oneforall_conf.tool_result_path
    oneforall_update_sh = oneforall_conf.tool_update_sh

    oneforall_task = TaskModels.query.filter_by(task_id=task_id).first()
    # OneForAll接受域名列表
    domain = oneforall_task.task_target

    # 清除OneForAll的日志
    os.system("echo '' > {}".format(oneforall_log_path))
    # 开始oneforall的查询
    print("[+] 域名：{} 开始进行oneforall模块".format(domain))
    cmd_result = out_file_cmd_exec(oneforall_cmd.format(target_domain=domain),
                                   oneforall_log_path)

    if cmd_result == 0:
        # OneForAll的输出是以域名为名称的
        print("[+] 域名：{} 的oneforall模块完成，开始读取结果".format(domain))
        result_path = os.path.join(
            oneforall_result_path,
            '{}.json'.format(tld.get_fld("http://" + domain)))
        # 读过大的json可能会卡
        with open(result_path, 'r') as f:
            results = json.load(f)
        for result in results:
            try:
                # 如果解析的是cname，则读取cname的域名
                if result['subdomain'] == result['cname']:
                    domain_db = DomainModels(task_id=oneforall_task.task_id,
                                             domain=result['subdomain'],
                                             domain_record=result['ip'])
                    db.add(domain_db)
                    db.commit()
                else:
                    domain_db = DomainModels(task_id=oneforall_task.task_id,
                                             domain=result['subdomain'],
                                             domain_record=result['cname'])
                    db.add(domain_db)
                    db.commit()
            except Exception as e:
                print("[!] 域名：{} 的oneforall模块结果数据入库失败：{}".format(domain, e))
                raise
    else:
        print(
            "[!] 域名：{} 的oneforall模块结果数据入库失败，运行OneForAll期间出现错误，subprocess返回值不为0"
            .format(domain))

    print("[+] 域名：{} 的oneforall模块结果数据入库成功".format(domain))
