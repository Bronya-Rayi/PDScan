from utils import db
from modules.tools import out_file_cmd_exec, kill_xray, kill_crawlergo
from models import TaskModels, SiteModels, ToolConfModels, ToolXrayModels, SitePathScanModels
# import config
import json
import os
import time
import threading


def xray_crawlergo_module(task_id):
    print(f'[+] xray_crawlergo_module正在运行，任务ID: {task_id}')

    xray_conf = ToolConfModels.query.filter_by(tool_name='xray').first()
    xray_cmd = xray_conf.tool_cmd
    xray_log_path = xray_conf.tool_log_path
    xray_result_path = xray_conf.tool_result_path
    xray_update_sh = xray_conf.tool_update_sh

    crawlergo_conf = ToolConfModels.query.filter_by(
        tool_name='crawlergo').first()
    crawlergo_cmd = crawlergo_conf.tool_cmd
    crawlergo_log_path = crawlergo_conf.tool_log_path
    crawlergo_result_path = crawlergo_conf.tool_result_path
    crawlergo_update_sh = crawlergo_conf.tool_update_sh

    xray_crawlergo_task = TaskModels.query.filter_by(task_id=task_id).first()

    # 启动xray
    # 用任务id和当前时间作为文件名
    result_file_name = xray_crawlergo_task.task_id + '_' + \
        time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.html'
    result_file_path = os.path.join(xray_result_path, result_file_name)

    # 将xray的结果文件目录添加至数据库
    task_xray_result_web = "/xray_results/" + result_file_name
    add_result_path = ToolXrayModels(task_id = xray_crawlergo_task.task_id,result_path = task_xray_result_web)
    db.add(add_result_path)
    db.commit()

    cmd = xray_cmd.format(result_file=result_file_path)

    xray_thread = threading.Thread(target=out_file_cmd_exec,
                                   args=(
                                       cmd,
                                       xray_log_path,
                                   ))
    xray_thread.start()

    def wait_xray_ok(xray_log_path, xray_wait_time):
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
    site_path_scan_db = SitePathScanModels.query.filter_by(task_id=task_id).all()
    site_path_scan_list = [row.url for row in site_path_scan_db]

    # 先从数据库中将识别出的站点导出到漏洞扫描的目标文件中
    site_db = SiteModels.query.filter_by(
        task_id=xray_crawlergo_task.task_id).all()
    site_list = [row.url for row in site_db]

    target_list = site_path_scan_list + site_list

    if len(target_list) == 0:
        xray_crawlergo_task.task_status = 'error'
        print("[!] 任务：{} 没有站点，无法进行漏洞扫描".format(task_id))
        db.commit()

        kill_xray()
        return False

    for target in target_list:

        print("[+] 正在爬取：{}".format(target))
        cmd = crawlergo_cmd.format(target=target)
        result = out_file_cmd_exec(cmd, crawlergo_log_path)

        if result == 0:
            print("[+] 爬取成功：{}，开始漏扫".format(target))
            # 等待xray结束
            xray_wait_time = 0
            while not wait_xray_ok(xray_log_path, xray_wait_time):
                xray_wait_time += 1
        else:
            print("[!] 站点：{} 漏洞扫描失败,crawlergo运行期间出错".format(target))
            kill_crawlergo()
        print("[+] 站点{} 漏洞扫描完成，开始扫描下一个站点".format(target))

    if os.path.isfile(result_file_path) != True:
        # 无扫描结果
        task_xray_result_web = "/xray_results/" + result_file_name + "(空文件，本次扫描无结果)"
        result_db = ToolXrayModels.query.filter_by(task_id = xray_crawlergo_task.task_id).first()
        result_db.result_path = task_xray_result_web
        db.commit()


    # 漏扫结束
    print("[+] 任务：{} 漏扫完成，正在关闭xray和crawlergo".format(task_id))
    kill_crawlergo()
    kill_xray()
    time.sleep(5)
    kill_crawlergo()
    kill_xray()
    print("[+] 任务：{} 的漏洞扫描完成".format(task_id))

    return True
