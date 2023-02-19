from flask import current_app, redirect
from app import create_app
from app.service.queue import TaskQueue
from flask_login import current_user

app = create_app()

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
    app.run(host="0.0.0.0",debug=True,port=8888)
