from app.utils import db

class DomainModels(db.Model):
    __tablename__ = 'pdscan_domain'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255),nullable=False)
    domain = db.Column(db.String(),nullable=False)
    domain_record = db.Column(db.String())