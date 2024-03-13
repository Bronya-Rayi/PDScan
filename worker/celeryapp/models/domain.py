from utils import db,Base
from sqlalchemy import Column, Integer, String

class DomainModels(Base):
    __tablename__ = 'pdscan_domain'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(255),nullable=False)
    domain = Column(String(),nullable=False)
    domain_record = Column(String())