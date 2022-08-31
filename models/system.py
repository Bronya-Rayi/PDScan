from datetime import datetime

from extensions import db


class LogModel(db.Model):
    __tablename__ = 'lg_logging'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10))
    uid = db.Column(db.Integer, default=None)
    url = db.Column(db.String(255))
    desc = db.Column(db.Text)
    ip = db.Column(db.String(255))
    success = db.Column(db.Boolean, default=True)
    user_agent = db.Column(db.Text)

    create_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
