from app.utils import db

class ToolConfModels(db.Model):
    __tablename__ = 'pdscan_tool_conf'
    id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String())
    tool_cmd = db.Column(db.String())
    tool_log_path = db.Column(db.String())
    tool_result_path = db.Column(db.String())
    tool_update_sh = db.Column(db.String())
    tool_others = db.Column(db.String())