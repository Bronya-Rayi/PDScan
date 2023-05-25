from app.utils import db
from app.modules.tools import out_file_cmd_exec, kill_xray, kill_crawlergo
from app.models import TaskModels, SiteModels
import config
import json
import os
import time
import threading


def xray_crawlergo_module(task_id):
    print(f'[+] xray_crawlergo_module正在运行，任务ID: {task_id}')

    xray_crawlergo_task = TaskModels.query.filter_by(task_id=task_id).first()

    # 启动xray
    # 用任务id和当前时间作为文件名
    result_file_name = xray_crawlergo_task.task_id + '_' + \
        time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.html'
    result_file_path = os.path.join(config.XRAY_RESULTS_PATH, result_file_name)

    cmd = config.XRAY_CMD.format(
        xray_proxy=config.XRAY_PROXY, result_file=result_file_path)
    
    xray_thread = threading.Thread(
        target=out_file_cmd_exec, args=(cmd, config.XRAY_LOG_PATH,))
    xray_thread.start()

    # 将xray的结果文件目录添加至数据库
    task_xray_result_now = "/xray_results/" + result_file_name
    # 查找以前数据库中记录的xray结果文件，将其与当前结果文件合并成列表
    task_xray_result = xray_crawlergo_task.task_xray_result
    if task_xray_result:
        task_xray_result = json.loads(task_xray_result)
        task_xray_result.append(task_xray_result_now)
    else:
        task_xray_result = [task_xray_result_now]

    TaskModels.query.filter_by(task_id=xray_crawlergo_task.task_id).update(
        {"task_xray_result": json.dumps(task_xray_result)})
    db.session.commit()

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

    # 先从数据库中将识别出的站点导出到漏洞扫描的目标文件中
    site_db = SiteModels.query.filter_by(
        task_id=xray_crawlergo_task.task_id).all()
    
    if len(site_db) == 0:
        xray_crawlergo_task.task_running_module = 'vulscan_error'
        xray_crawlergo_task.task_status = 'error'
        print("[!] 任务：{} 没有站点，无法进行漏洞扫描".format(task_id))
        db.session.commit()
        kill_xray()
        return False
    
    for site in site_db:

        print("[+] 正在爬取：{}".format(site.url))
        cmd = config.CRAWLERGO_CMD.format(
            xray_proxy=config.XRAY_PROXY, target=site.url)
        result = out_file_cmd_exec(cmd, config.CRAWLERGO_LOG_PATH)

        if result == 0:
            print("[+] 爬取成功：{}，开始漏扫".format(site.url))
            # 等待xray结束
            xray_wait_time = 0
            while not wait_xray_ok(config.XRAY_LOG_PATH, xray_wait_time):
                xray_wait_time += 1
        else:
            print("[!] 站点：{} 漏洞扫描失败,crawlergo运行期间出错".format(
                site.url))
            kill_crawlergo()

        print("[+] 站点{} 漏洞扫描完成，开始扫描下一个站点".format(site.url))
    # 漏扫结束
    print("[+] 任务：{} 漏扫完成，正在关闭xray和crawlergo".format(task_id))
    kill_crawlergo()
    kill_xray()
    time.sleep(5)
    kill_crawlergo()
    kill_xray()
    print("[+] 任务：{} 的漏洞扫描完成".format(task_id))

    return True
