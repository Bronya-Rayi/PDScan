from flask_login import current_user, login_user
from flask_restful import Resource, reqparse
from flask import request
from app.utils import success_api, fail_api, db
from app.models import UserModels
from functools import wraps

def auth_required(func):
    """
    登陆验证
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated != True:
            return fail_api(message="No Auth!")
        else:
            return func(*args, **kwargs)

    return wrapper

class LoginResource(Resource):

    def post(self):
        login_req = reqparse.RequestParser(bundle_errors=True)
        login_req.add_argument('username', type=str, help='请输入用户名', required=True)
        login_req.add_argument('password', type=str, help='请输入密码', required=True)
        req = login_req.parse_args()

        user = UserModels.query.filter_by(username='admin').first()

        if user is None:
            return fail_api(message="用户名或密码错误")

        if user.validate_password(req.password):
            # 登录
            login_user(user)
            return success_api(message="登录成功")
        return fail_api(message="用户名或密码错误")


class ChPasswdResource(Resource):

    @auth_required
    def post(self):
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')
        new_password_2 = request.json.get('new_password_2')

        if new_password != new_password_2:
            return fail_api(message="两次密码不一致")

        # 新密码长度必须大于8
        if len(new_password) < 8:
            return fail_api(message="密码长度必须大于8")

        # 验证旧密码
        if current_user.validate_password(old_password):
            user = UserModels.query.filter_by(username='admin').first()
            user.set_password(new_password)
            db.session.add(user)
            db.session.commit()
            return success_api(message="修改成功")
        else:
            return fail_api(message="旧密码错误")
