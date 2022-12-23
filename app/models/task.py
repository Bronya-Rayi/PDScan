from app.utils import db

class TaskModels(db.Model):
    __tablename__ = 'pdscan_task'
    task_id = db.Column(db.String(255),primary_key=True,nullable=False)
    task_name = db.Column(db.String(255),nullable=False)
    task_target = db.Column(db.String(),nullable=False)
    task_target_domain = db.Column(db.String())
    task_target_ip = db.Column(db.String())
    task_result_count = db.Column(db.Integer)
    task_running_module = db.Column(db.String(255),nullable=False)
    task_status = db.Column(db.String(255),nullable=False)
    task_start_time = db.Column(db.String(255),nullable=False)
    task_end_time = db.Column(db.String(255))
    task_c_duan = db.Column(db.String())
    task_port_limit = db.Column(db.String())
    task_vulscan = db.Column(db.String())
    task_xray_result = db.Column(db.String())
