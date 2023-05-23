from flask import current_app, redirect
from app import create_app,create_celery
from app.service.queue import TaskQueue
from flask_login import current_user
import config

app = create_app()

celery_app = create_celery(app)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/index.html')
    return redirect('/login.html')

@app.before_first_request
def init_background_task():
    current_app.TaskQueue= TaskQueue(app)
    current_app.TaskQueue.startTaskQueue()

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=8888,ssl_context=(config.CERT_PATH,config.CERT_KEY_PATH))
