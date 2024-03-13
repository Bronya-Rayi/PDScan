from utils import db,Base
from sqlalchemy import Column, Integer, String

class TaskModels(Base):
    __tablename__ = 'pdscan_task'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(255),nullable=False)
    task_name = Column(String(255),nullable=False)
    task_target = Column(String(),nullable=False)
    task_target_type = Column(String())
    task_module_list = Column(String(),nullable=False)
    task_running_module = Column(String(255),nullable=False)
    task_portscan_range = Column(String())
    task_status = Column(String(255),nullable=False)
    task_start_time = Column(String(255),nullable=False)
    task_end_time = Column(String(255))
    celery_id = Column(String())
    task_c_duan = Column(String())
