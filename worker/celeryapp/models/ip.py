from utils import db,Base
from sqlalchemy import Column, Integer, String

class IPModels(Base):
    __tablename__ = 'pdscan_ip'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(255),nullable=False)
    ip = Column(String())
    port = Column(Integer())
    service = Column(String())
    banner = Column(String())