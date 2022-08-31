from flask import Flask
import re
from datetime import datetime

date_str = re.compile('\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d$')


def add_data(data_list, obj):
    from extensions import db

    for _data in data_list:
        dept = obj()
        for key, value in _data.items():

            if isinstance(value, str) and date_str.match(value):
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

            setattr(dept, key, value)
        db.session.add(dept)
    db.session.commit()


def register_script(app: Flask):
    @app.cli.command()
    def init_db():
        import json
        import os

        path = os.path.dirname(os.path.abspath(__name__))
        path = os.path.join(path, 'static', 'data')
        cp_dept_data_list = json.loads(open(os.path.join(path, 'cp_dept.json'), encoding='utf-8').read())
        cp_user_data_list = json.loads(open(os.path.join(path, 'cp_user.json'), encoding='utf-8').read())
        file_photo_data_list = json.loads(open(os.path.join(path, 'file_photo.json'), encoding='utf-8').read())
        rt_power_data_list = json.loads(open(os.path.join(path, 'rt_power.json'), encoding='utf-8').read())
        rt_role_data_list = json.loads(open(os.path.join(path, 'rt_role.json'), encoding='utf-8').read())
        rt_role_power_data_list = json.loads(open(os.path.join(path, 'rt_role_power.json'), encoding='utf-8').read())
        rt_user_role_data_list = json.loads(open(os.path.join(path, 'rt_user_role.json'), encoding='utf-8').read())

        """数据库初始化"""

        # 创建化部门数据
        from models import DepartmentModels
        add_data(cp_dept_data_list, DepartmentModels)

        # 图片数据
        from models import PhotoModels

        add_data(file_photo_data_list, PhotoModels)

        # 初始化权限表数据
        from models import RightModels

        add_data(rt_power_data_list, RightModels)
        # 初始化角色表
        from models import RoleModels

        # 角色权限关系表
        from extensions import db
        for data in rt_role_power_data_list:
            db.session.execute('insert into rt_role_power VALUES (%s, %s, %s);' % tuple(data))
        db.session.commit()

        add_data(rt_role_data_list, RoleModels)

        # 管理员用户
        from models import UserModels

        add_data(cp_user_data_list, UserModels)

        # 用户角色表
        from extensions import db

        for data in rt_user_role_data_list:
            db.session.execute('insert into rt_user_role VALUES (%s, %s, %s);' % tuple(data))
        db.session.commit()

    @app.cli.command()
    def turn():
        """清空数据库"""
        from extensions import db
        db.drop_all()
        db.create_all()
