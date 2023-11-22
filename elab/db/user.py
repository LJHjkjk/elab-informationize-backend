from db import sqlAlchemy as db



class UserInfo(db.Model):
    __tablename__='user_info'
    id=db.Column(db.Integer,db.ForeignKey('user.name'),primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    award_winning_experience=db.Column(db.String)
    project_experience=db.Column(db.String)
    position=db.Column(db.String(30),db.ForeignKey('position.name'),nullable=False)
    department=db.Column(db.Enum())


class User(db.Model):
    __tablename__='user'
    # 所属组织
    owner=db.Column(db.String(100),primary_key=True)
    # 名字唯一标识（使用学号）
    name=db.Column(db.String(100),primary_key=True)
    # 每个人有一个id
    id=db.Column(db.String(100),nullable=False)
    # 头像的url
    avatar=db.Column(db.String(100))
    # 密码
    password=db.Column(db.String(100),nullable=False)
    # 显示名称
    displayName=db.Column(db.String(100))
    email=db.Column(db.String)
    phone=db.Column(db.String)


class UserView(db.Model):
    __tablename__='user_view'
    # 个人真实姓名
    name=db.Column(db.String(100))
    # 学号
    id=db.Column(db.Integer)
    # 头像的url
    avatar=db.Column(db.String(100))
    # 密码
    password=db.Column(db.String(100))
    # 显示名称
    displayName=db.Column(db.String(100))
