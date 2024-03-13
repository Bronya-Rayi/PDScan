from app.utils import db

class ToolXrayModels(db.Model):
    __tablename__ = 'pdscan_tool_xray'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255),nullable=False)
    result_path = db.Column(db.String(255),nullable=False)
