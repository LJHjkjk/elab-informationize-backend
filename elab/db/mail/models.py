from mail import db
import datetime    


class UserGroup(db.Document):
    meta={
    'collection':'user_group',
    'allow_inheritance':True,
    'abstract': True,
    }


class MailCenter(db.Document):
    # 邮件中心集合
    title=db.StringField(required=True,max_length=200)
    sender_name=db.StringField(required=True,max_length=30,default='系统通知')
    sender_id=db.IntField(required=True,default=0)
    pubdate=db.DateTimeField(required=True,default=datetime.datetime.utcnow)
    receiver_id=db.ListField(db.IntField(),required=True)

    meta={
        'collection':'mail_center',
        'allow_inheritance':True,
        'abstract': True,
        }



class UserMailbox(db.Document):
    # 用户收件箱集合
    id=db.IntField(require=True)
    name=db.StringField(require=True,max_length=30)
    sendable_group=db.ListField(db.ReferenceField(UserGroup),required=True,default=[])
    finished_mailbox=db.ListField(db.ReferenceField(MailCenter),required=True,default=[])
    unfinished_mailbox=db.ListField(db.ReferenceField(MailCenter),required=True,default=[])
    send_history=db.ListField(db.ReferenceField(MailCenter),required=True,default=[])

    meta={
    'collection':'user_mailbox',
    }



class NotifyMail(MailCenter):
    body=db.StringField(require=True)


class ReplyMail(MailCenter):
    body=db.StringField(require=True)
    reply_object_type=db.StringField(require=True,choices=['mail','apply','null'])
    reply_object=db.GenericReferenceField()



class ChoiceMail(MailCenter):
    body=db.StringField(require=True)
    is_multiple_choice=db.booleanField(require=True,default=False)
    options=db.ListField(db.StringField(max_length=20),min_items=2)
    results=db.ListField(db.StringField(max_length=20))


class JudgeMail(MailCenter):
    body=db.StringField(require=True)
    options = db.ListField(
        db.StringField(), 
        required=True, 
        min_items=2, 
        max_items=2,
        default=['是','否']
        )

class AttachmentMail(MailCenter):
    body=db.StringField(require=True)
    
    



