#/bin/sh

nohup redis-server > /dev/null 2>&1 &
sleep 1
cd /app/PDScan/worker/celeryapp ; nohup python3 -m celery -A celery_tasks worker -Q send_task -c 1 --loglevel=WARNING  --logfile="/app/PDScan/web/log/system_status.log" &
sleep 2
cd /app/PDScan/worker/celeryapp ; nohup python3 -m celery -A celery_stop_tasks worker -Q stop_task -c 1 --loglevel=WARNING  --logfile="/app/PDScan/web/log/stop_worker_log.log" &
sleep 2
cd /app/PDScan/worker/celeryapp ; nohup python3 -m celery -A celery_beat_task beat --loglevel=WARNING > /dev/null 2>&1 &

rm -rf /app/PDScan/web/nginx/server.csr
rm -rf /app/PDScan/web/nginx/key.pem
rm -rf /app/PDScan/web/nginx/cert.pem

echo '' > /app/PDScan/web/log/system_status.log

openssl req -new -newkey rsa:2048 -nodes -out /app/PDScan/web/nginx/server.csr -keyout /app/PDScan/web/nginx/key.pem -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=example.com"
openssl x509 -req -days 3650 -in /app/PDScan/web/nginx/server.csr -signkey /app/PDScan/web/nginx/key.pem -out /app/PDScan/web/nginx/cert.pem
service nginx start
python3 /app/PDScan/web/PDScan.py