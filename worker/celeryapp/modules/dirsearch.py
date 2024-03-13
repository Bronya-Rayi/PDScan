from models import TaskModels, SitePathScanModels,ToolConfModels, SiteModels
from utils import db
from modules.tools import out_file_cmd_exec
import requests
# import config
import json
import os


def dirsearch_module(task_id):
    print(f'[+] dirsearch_module正在运行，任务ID: {task_id}')
    dirsearch_conf = ToolConfModels.query.filter_by(
        tool_name='dirsearch').first()
    dirsearch_cmd = dirsearch_conf.tool_cmd
    dirsearch_log_path = dirsearch_conf.tool_log_path
    dirsearch_result_path = dirsearch_conf.tool_result_path
    dirsearch_update_sh = dirsearch_conf.tool_update_sh

    dirsearch_task = TaskModels.query.filter_by(task_id=task_id).first()

    db_site = SiteModels.query.filter_by(task_id=task_id).all()

    # dirsearch会同时查找任务设定的站点，以及通过其他方式查找到的站点
    site_dict = {}
    for row in db_site:
        site_dict[row.id] = row.url

    for id, site in site_dict.items():
        # 清除dirsearch的日志
        os.system("echo '' > {}".format(dirsearch_log_path))
        # 开始dirsearch的查询
        print("[+] 目标：{} 开始进行dirsearch模块".format(site))
        result_file = f'{task_id}_{id}.json'
        result_file = dirsearch_result_path + result_file
        cmd_result = out_file_cmd_exec(
            dirsearch_cmd.format(target=site, result_file=result_file),
            dirsearch_log_path)

        if cmd_result == 0:
            # dirsearch的输出固定为任务id，每次覆盖
            print("[+] 目标：{} 的dirsearch模块完成，开始读取结果".format(site))
            # 读过大的json可能会卡
            try:
                with open(result_file, 'r') as f:
                    result_file = json.load(f)
            except:
                print("[+] 目标：{} 的dirsearch结果为0".format(site))
                continue
            for result in result_file['results']:
                try:
                    site_path_scan = SitePathScanModels(
                        task_id=dirsearch_task.task_id,
                        url=result['url']
                    )
                    db.add(site_path_scan)
                    
                except Exception as e:
                    print("[!] 目标：{} 的dirsearch模块结果数据入库失败：{}".format(site, e))
                    raise
            db.commit()
        else:
            print(
                "[!] 目标：{} 的dirsearch模块结果数据入库失败，运行dirsearch期间出现错误，subprocess返回值不为0"
                .format(site))
            continue

        print("[+] 目标：{} 的dirsearch模块结果数据入库成功".format(site))
