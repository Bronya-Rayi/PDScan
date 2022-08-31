from flask import render_template
from applications.view import index_bp
from flask_login import login_required
from models import TaskModels

# 任务列表展示
@index_bp.get('/task/list')
@login_required
def task_index():
    return render_template('task/task_list.html')

# 添加任务
@index_bp.get('/task/add')
@login_required
def task_add():
    return render_template('task/task_add.html')

# 获取任务详情
@index_bp.get('/task/detail/<task_id>')
@login_required
def task_detail(task_id):
    vulscan_result = TaskModels.query.filter_by(task_id=task_id).first().task_xray_result
    if not vulscan_result:
        vulscan_result = ''
    return render_template('task/task_detail.html',task_id=task_id,vulscan_result_path=vulscan_result)