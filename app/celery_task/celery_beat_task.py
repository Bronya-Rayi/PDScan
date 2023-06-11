from PDScan import celery_app
from app.celery_task.celery_tasks import send_task,stop_task

# 定义定时任务
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(5.0, send_task.s(), name='发送任务')
    sender.add_periodic_task(5.0, stop_task.s(), name='停止任务')




