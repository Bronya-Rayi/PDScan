from app.utils import db

class SiteModels(db.Model):
    __tablename__ = 'pdscan_site'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255),nullable=False)
    url = db.Column(db.String(),nullable=False)
    ip = db.Column(db.String())
    status_code = db.Column(db.String())
    title = db.Column(db.String())
    finger = db.Column(db.String())
    xray_crawlergo_finish = db.Column(db.Integer)