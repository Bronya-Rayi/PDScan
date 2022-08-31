from applications import create_app
from common.utils.log import logger
from service.background_task_manager import BackgroundTaskManager
from flask import current_app
import config

app = create_app()

@app.before_first_request
def init_background_task():
    current_app.BackgroundTask= BackgroundTaskManager(app)
    current_app.BackgroundTask.startBackgroundTask()

if __name__ == '__main__':
    logger.info('Flask 正在启动')
    app.run(host="0.0.0.0",debug=True,port=8888)
