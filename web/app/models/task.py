from app.utils import db

class TaskModels(db.Model):
    __tablename__ = 'pdscan_task'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255),nullable=False)
    task_name = db.Column(db.String(255),nullable=False)
    task_target = db.Column(db.String(),nullable=False)
    task_target_type = db.Column(db.String())
    task_module_list = db.Column(db.String(),nullable=False)
    task_running_module = db.Column(db.String(255),nullable=False)
    task_portscan_range = db.Column(db.String())
    task_status = db.Column(db.String(255),nullable=False)
    task_start_time = db.Column(db.String(255),nullable=False)
    task_end_time = db.Column(db.String(255))
    celery_id = db.Column(db.String())
    task_c_duan = db.Column(db.String())
