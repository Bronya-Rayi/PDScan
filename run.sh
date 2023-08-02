#/bin/sh

nohup redis-server > /dev/null 2>&1 &
sleep 1
nohup python3 -m celery -A app.celery_task.celery_tasks worker --loglevel=WARNING  --logfile="/app/PDScan/log/system_status.log" &
sleep 2
nohup python3 -m celery -A app.celery_task.celery_beat_task beat --loglevel=WARNING > /dev/null 2>&1 &

rm -rf /app/PDScan/nginx/server.csr
rm -rf /app/PDScan/nginx/key.pem
rm -rf /app/PDScan/nginx/cert.pem

openssl req -new -newkey rsa:2048 -nodes -out /app/PDScan/nginx/server.csr -keyout /app/PDScan/nginx/key.pem -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=example.com"
openssl x509 -req -days 3650 -in /app/PDScan/nginx/server.csr -signkey /app/PDScan/nginx/key.pem -out /app/PDScan/nginx/cert.pem
service nginx start
python3 PDScan.py
