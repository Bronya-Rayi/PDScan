from utils import db,Base
from sqlalchemy import Column, Integer, String

class ToolXrayModels(Base):
    __tablename__ = 'pdscan_tool_xray'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(255),nullable=False)
    result_path = Column(String(),nullable=False)
