from utils import db,Base
from sqlalchemy import Column, Integer, String

class ToolConfModels(Base):
    __tablename__ = 'pdscan_tool_conf'
    id = Column(Integer, primary_key=True)
    tool_name = Column(String())
    tool_cmd = Column(String())
    tool_log_path = Column(String())
    tool_result_path = Column(String())
    tool_update_sh = Column(String())
    tool_others = Column(String())