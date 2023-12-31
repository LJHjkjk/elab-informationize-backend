from elab.db import sqlAlchemy as db
from .permission import *
from faker import Faker

# casdoor的用户表
class User(db.Model):
    __tablename__='user'
    # 所属组织
    owner=db.Column(db.String(100),primary_key=True)
    # 名字
    display_name=db.Column(db.String(100))
    # 名字唯一标识（使用学号）
    name=db.Column(db.String(100),primary_key=True,nullable=False)
    # 每个人有一个id
    id=db.Column(db.String(100),nullable=False)
    # 头像的url
    avatar=db.Column(db.String(100))
    # 密码
    password=db.Column(db.String(100),nullable=False)

    email=db.Column(db.String(100))
    phone=db.Column(db.String(20))

# 用户详情表
class UserInfo(db.Model):
    __tablename__='user_info'
    # 用户的id，学号
    id=db.Column(db.String(100),primary_key=True)
    # 用户的名字
    name=db.Column(db.String(100))
    # 获奖经历
    award_winning_experience=db.Column(db.Text)
    # 项目经历
    project_experience=db.Column(db.Text)
    # 职务
    position=db.Column(db.String(100))
    # 所在部门
    department=db.Column(db.String(100),default='无')

    # 性别
    gender=db.Column(db.Enum('女','男'))
    # 学院
    college=db.Column(db.String(100))
    # 专业
    major=db.Column(db.String(100))
    # 班级
    classname=db.Column(db.String(100))
    # 入学年份
    grade=db.Column(db.Integer)
    # 加入时间
    join_date=db.Column(db.Date)
    # 籍贯
    native_place=db.Column(db.String(100))
    # 照片
    photograph=db.Column(db.String(100))
    reason_for_application=db.Column(db.Text)

    
    # 为用户添加一个职位
    def add_position(self,position):
        from .permission import Positon,PositonDutyMap,MemberDutyMap
        position=Positon.query.get(position)
        positon_duty_map=PositonDutyMap.query.filter_by(position_name=position).all()
        member_duty_map=[]
        for i in positon_duty_map:
            member_duty_map.append(MemberDutyMap(member_id=self.id,duty=i.duty_name))
        db.session.add_all(member_duty_map)
        self.position=position
        db.session.commit()



class UserView(db.Model):
    #__abstract__ = True
    __tablename__='user_view'
    # 个人真实姓名
    name=db.Column(db.String(100))
    # id,学号
    id=db.Column(db.String(100),primary_key=True)
    # 头像的url
    avatar=db.Column(db.String(100))
    # 密码
    password=db.Column(db.String(100))
    # 邮箱
    email=db.Column(db.String(100))
    # 手机号
    phone=db.Column(db.String(20))
    # 获奖经历
    award_winning_experience=db.Column(db.Text)
    # 项目经历
    project_experience=db.Column(db.Text)
    # 职务
    position=db.Column(db.String(30),default='成员')
    # 所在部门
    department=db.Column(db.Enum('硬件组','极创组','无'),default='硬件组')

    # 性别
    gender=db.Column(db.Enum('女','男'))
    # 学院
    college=db.Column(db.String(100))
    # 专业
    major=db.Column(db.String(100))
    # 班级
    classname=db.Column(db.String(100))
    # 入学年份
    grade=db.Column(db.Integer)
    # 加入时间
    join_date=db.Column(db.Date)
    # 籍贯
    native_place=db.Column(db.String(100))
    # 照片
    photograph=db.Column(db.String(100))
    # 申请理由
    reason_for_application=db.Column(db.Text)
    def return_to_dict(self):
        result={
            'id':self.id,
            'name':self.name,
            'avatar':self.avatar,
            'email':self.email,
            'phone':self.phone,
            'award_winning_experience':self.award_winning_experience,
            'project_experience':self.project_experience,
            'position':self.position,
            'department':self.department,
            'gender':self.gender,
            'college':self.college,
            'major':self.major,
            'classname':self.classname,
            'grade':self.grade,
            'join_date':self.join_date.strftime("%Y-%m-%d")
                if self.join_date else None,
            'native_place':self.native_place,
            'photograph':self.photograph,
            'reason_for_application':self.reason_for_application,
        }
        return result



def init_user():
    try:
        db.metadata.create_all(bind=db.engine, tables=[UserInfo.__table__])
        # 创建视图
        create_user_view_sql='''
        CREATE VIEW user_view AS
        SELECT 
        user_info.id,
        user_info.name,
        user_info.award_winning_experience,
        user_info.project_experience,
        user_info.position,
        user_info.gender,
        user_info.college,
        user_info.major,
        user_info.classname,
        user_info.grade,
        user_info.join_date,
        user_info.native_place,
        user_info.department,
        user_info.photograph,
        user_info.reason_for_application,
        user.avatar,
        user.password,
        user.email,
        user.phone

        FROM user
        JOIN user_info on user_info.id=user.name
        ;
        '''
        db.session.execute(db.text(create_user_view_sql))

        # 创建admin账户
        admin=User.query.filter_by(name='admin').one()
        admin_user=UserInfo(
            name=admin.id,
            id=admin.name,
            position='admin',
        )
        db.session.add(admin_user)
        db.session.commit()
        
    except Exception as e:
        print(e)


def drop_user():
    try:
        db.session.execute(db.text('drop tables if exists user_view,user_info'))
        db.session.execute(db.text('drop view if exists user_view'))
        db.session.commit()
    except Exception as e:
        print(e)
    try:
        User.query.filter(User.name!='admin').delete()
    except Exception as e:
        print(e)
    

def forge_user():
    fake = Faker('zh_CN')
    try:
        new_user=User(
            name='20221071164',
            owner='built-in',
            avatar='https://img2.baidu.com/it/u=496494351,3684413482&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500',
            password='123123',
            id='1',
            email=fake.email(),
            phone=fake.phone_number(),
            display_name='李佳浩'
        )
        new_user_info=UserInfo(
            name='李佳浩',
            id='20221071164',
            position='成员',
            project_experience=fake.text(),
            award_winning_experience=fake.text(),
            grade=fake.random_int(min=2000, max=2023)
        )
        db.session.add(new_user)
        db.session.add(new_user_info)
        db.session.commit()

        # 生成其他的虚拟数据
        
        for i in range(0,20):
            name=fake.name()
            new_user=User(
                name=str(fake.ssn(min_age=11, max_age=11)),
                owner='built-in',
                avatar='https://img2.baidu.com/it/u=496494351,3684413482&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500',
                password='123123',
                id=str(i+2),
                email=fake.email(),
                phone=fake.phone_number(),
                display_name=name
            )
            new_user_info=UserInfo(
                name=name,
                id=new_user.name,
                position='成员',
                project_experience=fake.text(),
                award_winning_experience=fake.text(),
                grade=fake.random_int(min=2000, max=2023)

            )
            db.session.add(new_user)
            db.session.add(new_user_info)
        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()