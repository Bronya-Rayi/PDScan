from celery import Celery
from celery_tasks import task_worker
from celery_stop_tasks import stop_celery_worker

celery_app = Celery("pdscan_beat_celery",broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
#  python3 -m celery -A app.celery_task.celery_tasks worker --loglevel=WARNING  --logfile="/app/PDScan/log/system_status.log"
# 定义定时任务
# 限制task数量
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, task_worker.s(), name='发送任务',options={'queue': 'send_task'})
    sender.add_periodic_task(5.0, stop_celery_worker.s(), name='删除任务',options={'queue': 'stop_task'})





