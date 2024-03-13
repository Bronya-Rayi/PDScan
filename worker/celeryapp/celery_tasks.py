from celery import Celery
from models import TaskModels
from sqlalchemy import and_, desc
from utils import db
from modules.tools import kill_xray_crawlergo, kill_httpx, kill_scaninfo, kill_oneforall, kill_dirsearch
from modules import oneforall_module, httpx_module, scaninfo_module, xray_crawlergo_module, dirsearch_module
import re
import traceback
import json
import time
import os

# python3 -m celery -A celery_tasks worker -c 1 --loglevel=WARNING > /dev/null 2>&1 &
# 创建Celery应用
celery_app = Celery("pdscan_task_celery",
                    broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/1')

# 可执行的模块
worker_task_list = ["oneforall", "httpx", "scaninfo", "xray_crawlergo", "dirsearch"]

def validate_task_id(string):
    pattern = r'^[a-fA-F0-9]{10}$'
    return re.match(pattern, string) is not None

def validate_task_module(module_name):
    # 判断模块是否在worker_task_list中
    return module_name in worker_task_list

def check_for_waiting_task():
    # 查询所有task_status为waiting的任务
    waiting_task = TaskModels.query.filter_by(task_status='waiting').order_by(
        desc(TaskModels.task_start_time)).first()
    # 如果为空，则输出提示信息
    if not waiting_task:
        # print('[-] 定时任务：没有任务需要发送')
        return False
    else:
        return waiting_task
    
def run_module(waiting_task):
    print(f'[+] 任务ID：{waiting_task.task_id}，开始执行{waiting_task.task_running_module}任务')
    
    task_module_list = json.loads(waiting_task.task_module_list)
    unfinished_module_list = task_module_list[task_module_list.index(waiting_task.task_running_module):]
    
    try:
        for module_name in unfinished_module_list:
            # 校验模块名
            if validate_task_module(module_name) == False:
                print(
                    f'[-] 任务ID：{waiting_task.task_id}，任务状态错误，未找到模块{module_name}')
                waiting_task.task_running_module = 'error'
                waiting_task.task_status = 'error'
                db.commit()
                db.close()
                return
            
            waiting_task.task_running_module = module_name
            db.commit()
            # 任务执行
            # module_name已经写死，task_id也写死为自动生成的
            module_func = f"{waiting_task.task_running_module}_module('{waiting_task.task_id}')"
            print(f'[+] module_func: {module_func}')
            eval(module_func)

            print(
                f'[+] 任务ID：{waiting_task.task_id}，{module_name}任务执行完成'
            )
                
        waiting_task.task_status = 'finish'
        waiting_task.task_running_module = 'finish'
        waiting_task.task_end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.localtime())
        db.commit()
        print(f'[+] 任务ID：{waiting_task.task_id}，全部任务完成')
        return
                
    except Exception as e:
        waiting_task.task_status = 'error'
        db.commit()

        print(f'[-] 任务ID：{waiting_task.task_id}，任务执行失败，错误信息:')
        print(traceback.format_exc())
        return
        
    
# 限制task数量
#  python3 -m celery -A celery_tasks worker -Q send_task -c 1 --loglevel=WARNING

@celery_app.task(queue='send_task')
def task_worker():
    celery_task_id = task_worker.request.id
    waiting_task = check_for_waiting_task()
    
    # 判断当前数据库中是否有等待执行的任务
    if waiting_task == False:
        print(f'[-] Worker {celery_task_id}：没有任务需要处理')
        db.close()
        return 
    
    waiting_task.celery_id = celery_task_id
    db.commit()
    # 校验任务ID
    if not validate_task_id(waiting_task.task_id):
        print(f'[-] 任务ID：{waiting_task.task_id}，任务ID错误，含有非法字符')
        waiting_task.task_running_module = 'error'
        waiting_task.task_status = 'error'
        db.commit()
        db.close()
        return
    
    task_module_list = json.loads(waiting_task.task_module_list)

    if waiting_task.task_running_module == 'waiting' or waiting_task.task_running_module == 'error' or waiting_task.task_running_module == 'finish':
        waiting_task.task_running_module = task_module_list[0]
        waiting_task.task_status = 'running'
        db.commit()
    
    else:
        waiting_task.task_status = 'running'
        db.commit()
    
    # 开始执行当前任务的模块
    run_module(waiting_task)
    print(f'[+] 任务ID：{waiting_task.task_id}，执行完成')
    db.close()
    return
    



