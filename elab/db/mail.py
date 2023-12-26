from elab.db import sqlAlchemy as db
from datetime import datetime
import json
from faker import Faker

class MailCenter(db.Model):
    __tablename__='mail_center'
    # 邮件id
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    sender_id=db.Column(db.String(30),nullable=False,default=0)
    sender_name=db.Column(db.String(30),nullable=False,default='系统通知')
    pubdate=db.Column(db.DateTime, default=datetime.now())
    receivers_id=db.Column(db.JSON,nullable=False)
    body=db.Column(db.Text)
    is_attachment = db.Column(db.Boolean, default=False)
    
    def return_dict(self,is_receivers=False,is_body=True):
        '''
        返回符合可序列化的字典
        '''
        result= {
            'mail_id':self.id,
            'title':self.title,
            'pubdate':self.pubdate.timestamp() if self.pubdate else None,
            'sender_id':self.sender_id,
            'sender_name':self.sender_name,
        }
        if is_receivers:
            pass
        if is_body:
            result['body']=self.body

        return result


    @classmethod
    def send_system_mail(cls,title,receivers_id,body,**kwargs):
        '''
        发送一个系统邮件
        '''
        # 创建系统邮件
        sys_mail=cls(title=title,receivers_id=receivers_id,body=body,*kwargs)
        db.session.add(sys_mail)
        db.session.commit()

        # 添加到接收者中
        UserMailbox.add_mail_to_receivers(sys_mail.id,receivers_id)
    
    


class UserMailbox(db.Model):
    __tablename__='user_mailbox'
    id=db.Column(db.String(100),primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    finished_mailbox=db.Column(db.JSON,nullable=False,default='[]')
    unfinished_mailbox=db.Column(db.JSON,nullable=False,default='[]')
    send_history=db.Column(db.JSON,nullable=False,default='[]')


    def send_mail(self,title,body,receivers_id,**kwargs):
        # 创建邮件
        new_mail=MailCenter(
            title=title,
            body=body,
            receivers_id=json.dumps(receivers_id),
            sender_name=self.name,
            sender_id=self.id,
            **kwargs
            )
        db.session.add(new_mail)
        db.session.commit()
        # 将邮件添加到接收者中
        self.add_mail_to_receivers(new_mail.id,receivers_id)
        # 将邮件添加到自己的发送历史
        json_data=json.loads(self.send_history)
        json_data.append(new_mail.id)
        self.send_history=json.dumps(json_data)
        db.session.commit()
    
    
    @classmethod
    def add_mail_to_receivers(cls,mail_id,receivers_id):
        for receiver_id in receivers_id:
            userMailbox=cls.query.get(receiver_id)
            json_data=json.loads(userMailbox.unfinished_mailbox)
            json_data.append(mail_id)
            userMailbox.unfinished_mailbox=json.dumps(json_data)
            db.session.commit()
        



def init_mail():
    db.metadata.create_all(bind=db.engine, tables=[MailCenter.__table__,UserMailbox.__table__])
    # 获取user的信息
    from .user import UserView
    users=UserView.query.all()

    # 为每一个user创建一个用户收件箱
    for user in users:
        print(user)
        user_mailbox=UserMailbox(
            id=user.id,
            name=user.name,
        )
        db.session.add(user_mailbox)
        db.session.commit()



def drop_mail():
    # 删除两个表
    try:
        db.session.execute(db.text('drop tables if exists user_mailbox,mail_center'))
        db.session.commit()
    except Exception as e:
        print(e)




def forge_mail():
    # 获取user的信息
    from .user import UserView
    users=UserView.query.all()

    # 为每一个user创建一个用户收件箱
    for user in users:
        user_mailbox=UserMailbox(
            id=user.id,
            name=user.name,
        )
        db.session.add(user_mailbox)
        db.session.commit()


    # 获取user的信息
    from .user import UserView
    users=UserView.query.all()
    # 创建一些虚拟邮件
    fake=Faker('zh_CN')
    users=UserMailbox.query.all()
    for user in users:
        user.send_mail(
            title=fake.sentence(),
            body=fake.text(),
            receivers_id=['20221071164'],
            pubdate=fake.date_time()
        )
    
