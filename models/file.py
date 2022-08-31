from datetime import datetime

from extensions import db


class PhotoModels(db.Model):
    __tablename__ = 'file_photo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    href = db.Column(db.String(255))
    mime = db.Column(db.CHAR(50), nullable=False)
    size = db.Column(db.CHAR(30), nullable=False)

    create_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
