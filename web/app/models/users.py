from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.utils import db

class UserModels(db.Model, UserMixin):
    __tablename__ = 'pdscan_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(20), comment='用户名')
    password_hash = db.Column(db.String(128), comment='哈希密码')

    def set_password(self, password):
        """设置密码，对密码进行加密存储"""
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        """校验密码方法"""
        return check_password_hash(self.password_hash, password)

