from flask import request
from flask_login import current_user
from flask_restful import Resource, reqparse
from sqlalchemy import desc

from common.utils.http import fail_api, success_api, table_api
from extensions import db
from models import UserModels, RoleModels, DepartmentModels
from models import LogModel


def get_current_user_logs():
    """ 获取当前用户日志 """
    log = LogModel.query.filter_by(url='/passport/login').filter_by(uid=current_user.id).order_by(
        desc(LogModel.create_at)).limit(10)
    return log


def is_user_exists(username):
    """ 判断用户是否存在 """
    res = UserModels.query.filter_by(username=username).count()
    return bool(res)


def delete_by_id(_id):
    """ 删除用户 """
    user = UserModels.query.filter_by(id=_id).first()
    roles_id = []
    for role in user.role:
        roles_id.append(role.id)
    roles = RoleModels.query.filter(RoleModels.id.in_(roles_id)).all()
    for r in roles:
        user.role.remove(r)
    res = UserModels.query.filter_by(id=_id).delete()
    db.session.commit()
    return res


def batch_remove(ids):
    """ 批量删除 """
    for _id in ids:
        delete_by_id(_id)


def update_user_role(_id, roles_list):
    user = UserModels.query.filter_by(id=_id).first()
    roles_id = []
    for role in user.role:
        roles_id.append(role.id)
    roles = RoleModels.query.filter(RoleModels.id.in_(roles_id)).all()
    for r in roles:
        user.role.remove(r)
    roles = RoleModels.query.filter(RoleModels.id.in_(roles_list)).all()
    for r in roles:
        user.role.append(r)
    db.session.commit()


class UserUsersResource(Resource):
    """用户列表数据操作"""

    def get(self):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('limit', type=int, default=10)
        parser.add_argument('realName', type=str, dest='real_name')
        parser.add_argument('username', type=str)
        parser.add_argument('deptId', type=int, dest='dept_id', default=0)

        res = parser.parse_args()

        filters = []

        if res.real_name:
            filters.append(UserModels.realname.like('%' + res.real_name + '%'))
        if res.username:
            filters.append(UserModels.username.like('%' + res.username + '%'))
        if res.dept_id:
            filters.append(UserModels.dept_id == res.dept_id)

        paginate = UserModels.query.filter(*filters).paginate(page=res.page,
                                                              per_page=res.limit,
                                                              error_out=False)

        dept_name = lambda dept_id: DepartmentModels.query.filter_by(id=dept_id).first().dept_name if dept_id else ""
        user_data = [{
            'id': item.id,
            'username': item.username,
            'realname': item.realname,
            'enable': item.enable,
            'create_at': str(item.create_at),
            'update_at': str(item.update_at),
            'dept': dept_name(item.dept_id),
        } for item in paginate.items]
        return table_api(result={'items': user_data,
                                 'total': paginate.total}
                         , code=0)

    def post(self):
        """新建单个用户"""
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        parser = reqparse.RequestParser()
        parser.add_argument("roleIds", type=str, dest='role_ids')
        parser.add_argument("username", type=str, required=True, help="用户名不能为空")
        parser.add_argument("realName", type=str, required=True, help="真实姓名不能为空", dest='real_name')
        parser.add_argument("password", type=str, required=True, help="密码不得为空")

        res = parser.parse_args()

        role_ids = res.role_ids.split(',')

        if is_user_exists(res.username):
            return fail_api(message="用户已经存在")

        user = UserModels()
        user.username = res.username
        user.realname = res.real_name
        user.set_password(res.password)
        db.session.add(user)
        db.session.commit()

        """ 增加用户角色 """
        user = UserModels.query.filter_by(id=user.id).first()
        roles = RoleModels.query.filter(RoleModels.id.in_(role_ids)).all()
        for r in roles:
            user.role.append(r)
        db.session.commit()

        return success_api(message="增加成功", code=0)

    def delete(self):
        """批量删除"""
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        ids = request.form.getlist('ids[]')
        batch_remove(ids)
        return success_api(message="批量删除成功")


class UserUserResource(Resource):
    """修改用户数据"""

    def post(self, user_id):
        """新建单个用户"""
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        parser = reqparse.RequestParser()
        parser.add_argument("roleIds", type=str, dest='role_ids')
        parser.add_argument("username", type=str, required=True, help="用户名不能为空")
        parser.add_argument("realName", type=str, required=True, help="真实姓名不能为空", dest='real_name')
        parser.add_argument("password", type=str, required=True, help="密码不得为空")

        res = parser.parse_args()

        role_ids = res.role_ids.split(',')

        if is_user_exists(res.username):
            return fail_api(message="用户已经存在")

        user = UserModels()
        user.username = res.username
        user.realname = res.real_name
        user.set_password(res.password)
        db.session.add(user)
        db.session.commit()

        """ 增加用户角色 """
        user = UserModels.query.filter_by(id=user.id).first()
        roles = RoleModels.query.filter(RoleModels.id.in_(role_ids)).all()
        for r in roles:
            user.role.append(r)
        db.session.commit()

        return success_api(message="增加成功", code=0)

    def delete(self, user_id):
        # 删除用户
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        res = delete_by_id(user_id)
        if not res:
            return fail_api(message="删除失败")
        return success_api(message="删除成功")


class UserRoleResource(Resource):
    def put(self, user_id):
        if current_user.is_authenticated != True:
            return fail_api(message="请登录")
        parser = reqparse.RequestParser()
        parser.add_argument('roleIds', type=str, dest='role_ids')
        parser.add_argument('userId', type=str, dest='user_id')
        parser.add_argument('username', type=str)
        parser.add_argument('realName', type=str, dest='real_name')
        parser.add_argument('deptId', type=str, dest='dept_id')

        res = parser.parse_args()
        role_ids = res.role_ids.split(',')

        # 更新用户数据
        UserModels.query.filter_by(id=user_id).update({'username': res.username,
                                                        'realname': res.real_name,
                                                        'dept_id': res.dept_id})
        db.session.commit()

        update_user_role(user_id, role_ids)

        return success_api(message="更新成功")
