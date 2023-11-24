from elab.db import sqlAlchemy as db
from faker import Faker



# 用户详情表
class UserInfo(db.Model):
    __tablename__='user_info'
    # 用户的id，学号
    # id=db.Column(db.String(100),db.ForeignKey('user.name'),primary_key=True)
    id=db.Column(db.String(100),primary_key=True)
    # 用户的名字
    name=db.Column(db.String(30))
    # 获奖经历
    award_winning_experience=db.Column(db.Text)
    # 项目经历
    project_experience=db.Column(db.Text)
    # 职务
    # position=db.Column(db.String(30),db.ForeignKey('position.name'),nullable=False)
    position=db.Column(db.String(30))

    # 所在部门
    department=db.Column(db.String(30))

# casdoor的用户表
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

    email=db.Column(db.String(100))
    phone=db.Column(db.String(20))




# 结合了user表和user_info表的视图
class UserView(db.Model):
    #__abstract__ = True
    __tablename__='user_view'
    # 个人真实姓名
    name=db.Column(db.String(100))
    # 学号
    id=db.Column(db.Integer,primary_key=True)
    # 头像的url
    avatar=db.Column(db.String(100))
    # 密码
    password=db.Column(db.String(100))
    # 邮箱
    email=db.Column(db.String(100))
    # 手机号
    phone=db.Column(db.String(100))
    # 获奖经历
    award_winning_experience=db.Column(db.Text)
    # 项目经历
    project_experience=db.Column(db.Text)
    # 职务
    position=db.Column(db.String(30))
    # 所在部门
    department=db.Column(db.String(30))
    



def init_user():
    # 先创建所有的表
    db.create_all()
    # 刪除user_view
    db.session.execute(db.text('drop table if exists user_view'))
    db.session.commit()
    try:
        # 创建视图
        create_user_view_sql=db.text('''
        CREATE VIEW user_view AS
        SELECT 
        user_info.id,
        user_info.name,
        user_info.award_winning_experience,
        user_info.project_experience,
        user_info.position,
        user_info.department,
        user.avatar,
        user.password,
        user.email,
        user.phone

        FROM user
        JOIN user_info on user_info.id=user.name
        ;
        ''')

        db.session.execute(create_user_view_sql)
        db.session.commit()
    except Exception as e:
        print(e)

def drop_user():
    try:
        db.session.execute(db.text('drop tables if exists user_info,user_view'))
        db.session.commit()
    except Exception as e:
        print(e)
    try:
        User.query.filter(User.name!='admin').delete()
    except Exception as e:
        print(e)
    

def forge_user():
    try:
        new_user=User(
            name='20221071164',
            owner='built-in',
            avatar='https://img2.baidu.com/it/u=496494351,3684413482&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500',
            password='123123',
            id='1',
        )
        new_user_info=UserInfo(
            name='李佳浩',
            id='20221071164',
        )
        db.session.add(new_user)
        db.session.add(new_user_info)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()