from utils import db,Base
from sqlalchemy import Column, Integer, String

class SitePathScanModels(Base):
    __tablename__ = 'pdscan_site_path_scan'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(255),nullable=False)
    url = Column(String(),nullable=False)