from app.utils import db

class SitePathScanModels(db.Model):
    __tablename__ = 'pdscan_site_path_scan'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255),nullable=False)
    url = db.Column(db.String(),nullable=False)