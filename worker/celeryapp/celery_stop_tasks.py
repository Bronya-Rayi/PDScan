from celery import Celery,app
from sqlalchemy import and_, desc
from utils import db
from models import TaskModels
from modules.tools import kill_crawlergo,kill_dirsearch,kill_httpx,kill_oneforall,kill_scaninfo,kill_xray,kill_xray_crawlergo
from celery_tasks import validate_task_module
import signal


# 创建Celery应用
celery_app = Celery("pdscan_task_celery",
                    broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/1')
#  python3 -m celery -A celery_tasks worker -Q stop_task -c 1 --loglevel=WARNING


@celery_app.task(queue='stop_task')
def stop_celery_worker():
    # 从数据库中查找任务运行状态为wait_for_delete或wait_for_stop的任务，终止worker及其线程的执行
    waiting_task = TaskModels.query.filter(TaskModels.task_status.like("%wait_for%")).first()
    if waiting_task == None:
        print('[+] 没有任务需要暂停或删除')
        db.close()
        return

    if waiting_task.task_status == 'wait_for_stop':
        if waiting_task.celery_id == '':
            waiting_task.task_status ='stop'
            db.commit()
        else:
            celery_app.control.revoke(waiting_task.celery_id, terminate=True, signal=signal.SIGQUIT)
            waiting_task.task_status ='stop'
            db.commit()
        print(f'[+] 任务ID：{waiting_task.task_id}，停止执行')

    elif waiting_task.task_status == 'wait_for_delete':
        if waiting_task.celery_id == '':
            db.delete(waiting_task)
            db.commit()
        else:
            celery_app.control.revoke(waiting_task.celery_id, terminate=True, signal=signal.SIGQUIT)
            db.delete(waiting_task)
            db.commit()
        print(f'[+] 任务ID：{waiting_task.task_id}，删除任务')
    
        
    module_name = waiting_task.task_running_module
    if validate_task_module(module_name) == False:
        print(
            f'[-] 任务ID：{waiting_task.task_id}，任务状态错误，未找到模块{module_name}')
        waiting_task.task_running_module = 'error'
        waiting_task.task_status = 'error'
        db.commit()
        db.close()
        return
    # 执行模块终止函数
    # module_name已经写死，task_id也写死为自动生成的
    module_func = f"kill_{waiting_task.task_running_module}()"
    print(f'[+] module_func: {module_func}')
    eval(module_func)

    db.close()
    return
        
