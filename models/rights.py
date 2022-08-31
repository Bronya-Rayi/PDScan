from extensions import db

# 创建中间表
user_role = db.Table(
    "rt_user_role",  # 中间表名称
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    db.Column("user_id", db.Integer, db.ForeignKey("cp_user.id"), comment='用户编号'),  # 属性 外键
    db.Column("role_id", db.Integer, db.ForeignKey("rt_role.id"), comment='角色编号'),  # 属性 外键
)

# 创建中间表
role_power = db.Table(
    "rt_role_power",  # 中间表名称
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    db.Column("power_id", db.Integer, db.ForeignKey("rt_power.id"), comment='用户编号'),  # 属性 外键
    db.Column("role_id", db.Integer, db.ForeignKey("rt_role.id"), comment='角色编号'),  # 属性 外键
)


class RightModels(db.Model):
    __tablename__ = 'rt_power'
    id = db.Column(db.Integer, primary_key=True, comment='权限编号')
    name = db.Column(db.String(255), comment='权限名称')
    type = db.Column(db.SMALLINT, comment='权限类型')
    code = db.Column(db.String(30), comment='权限标识')
    url = db.Column(db.String(255), comment='权限路径')
    open_type = db.Column(db.String(10), comment='打开方式')
    parent_id = db.Column(db.Integer, db.ForeignKey("rt_power.id"), comment='父类编号')
    icon = db.Column(db.String(128), comment='图标')
    sort = db.Column(db.Integer, comment='排序')
    enable = db.Column(db.Boolean, comment='是否开启')

    parent = db.relationship("RightModels", remote_side=[id])  # 自关联


class RoleModels(db.Model):
    __tablename__ = 'rt_role'
    id = db.Column(db.Integer, primary_key=True, comment='角色ID')
    name = db.Column(db.String(255), comment='角色名称')
    code = db.Column(db.String(255), comment='角色标识')
    enable = db.Column(db.Boolean, comment='是否启用')
    comment = db.Column(db.String(255), comment='备注')
    details = db.Column(db.String(255), comment='详情')
    sort = db.Column(db.Integer, comment='排序')

    power = db.relationship('RightModels', secondary="rt_role_power", backref=db.backref('role'))
