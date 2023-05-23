from PDScan import celery_app
from app.celery_task.celery_tasks import send_task

# 定义定时任务
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 每隔 10 秒执行一次任务
    sender.add_periodic_task(5.0, send_task.s(), name='发送任务')

