from app.utils import db

class WebsiteAnalysisModels(db.Model):
    __tablename__ = 'pdscan_website_analysis'
    domain_or_ip = db.Column(db.String(),primary_key=True,nullable=False)
    title = db.Column(db.String())
    banner = db.Column(db.String(),nullable=False)
    finger = db.Column(db.String())
    url_scan = db.Column(db.String())
    task_id = db.Column(db.String())