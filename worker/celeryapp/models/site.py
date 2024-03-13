from utils import db,Base
from sqlalchemy import Column, Integer, String

class SiteModels(Base):
    __tablename__ = 'pdscan_site'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(255),nullable=False)
    url = Column(String(),nullable=False)
    ip = Column(String())
    status_code = Column(String())
    title = Column(String())
    finger = Column(String())