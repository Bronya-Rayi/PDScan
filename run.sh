#/bin/sh

nohup redis-server > /dev/null 2>&1 &
sleep 1
nohup python3 -m celery -A app.celery_task.celery_tasks worker --loglevel=WARNING > ./log/system_status.log &
sleep 2
nohup python3 -m celery -A app.celery_task.celery_beat_task beat --loglevel=WARNING > /dev/null 2>&1 &
python3 PDScan.py
