from app.utils import db

class IPModels(db.Model):
    __tablename__ = 'pdscan_ip'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255),nullable=False)
    ip = db.Column(db.String())
    port = db.Column(db.Integer())
    service = db.Column(db.String())
    banner = db.Column(db.String())