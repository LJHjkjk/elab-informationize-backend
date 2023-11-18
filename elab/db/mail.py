from db import mongodb as db
import datetime    


class UserGroup(db.Document):
    meta={
    'collection':'user_group',
    'allow_inheritance':True,
    'abstract': True,
    }



class MailCenter(db.Document):
    # 邮件id，由mongodb默认生成
    id = db.ObjectIdField(primary_key=True, default=None)
    title=db.StringField(required=True,max_length=200)
    # 邮件的类型
    type=db.StringField(required=True,
                        choices=['notify','reply','choice','judge'],
                        default='notify'
                        )
    # 发送者的名字
    sender_name=db.StringField(required=True,max_length=30,default='系统通知')
    # 发送者的id
    sender_id=db.IntField(required=True,default=0)
    pubdate=db.DateTimeField(required=True,default=datetime.datetime.utcnow)
    # 收件人的id列表
    receivers_id=db.ListField(db.IntField(),required=True)

    # 是否携带附件
    is_attachment=db.BooleanField(default=False)

    # 附件的信息，具体需要结合文件系统
    #attachment_id=db.File()

    # 邮件中心集合
    meta={
        'collection':'mail_center',
        'allow_inheritance':True,
        'abstract': True,
        }
    
    def return_dict(self,is_return_receiver:bool=False):
        '''
        返回符合可序列化的字典
        '''
        result= {
        'result':'ok',
        'message':{
            'id':id,
            'title':self.title,
            'type':self.type,
            'pubdate':self.pubdate.timestamp(),
            'sender_id':self.sender_id,
            'sender_name':self.sender_name,
            }
        }
        if is_return_receiver:
            pass
        return result


class UserMailbox(db.Document):
    # 用户收件箱集合
    id = db.ObjectIdField(primary_key=True, default=None)
    name=db.StringField(require=True,max_length=30)
    # 可发送对象的群组的文档
    sendable_id=db.ListField(db.IntField(),required=True,default=[])
    finished_mailbox=db.ListField(db.ReferenceField(MailCenter),required=True,default=[])
    unfinished_mailbox=db.ListField(db.ReferenceField(MailCenter),required=True,default=[])
    send_history=db.ListField(db.ReferenceField(MailCenter),required=True,default=[])

    meta={
    'collection':'user_mailbox',
    }



class NotifyMail(MailCenter):
    body=db.StringField(require=True)

    def return_dict(self, is_return_receiver):
        # 在父类的基础上增加自己的变量进入字典
        result=super().return_dict(is_return_receiver)
        result['message']['body']=self.body
        return result


class ReplyMail(MailCenter):
    body=db.StringField(require=True)
    reply_object_type=db.StringField(require=True,choices=['mail','apply','null'])
    reply_object=db.GenericReferenceField()





class ChoiceMail(MailCenter):
    body=db.StringField(require=True)
    is_multiple_choice=db.booleanField(require=True,default=False)
    options=db.ListField(db.StringField(max_length=20),min_items=2)
    results=db.ListField(db.StringField(max_length=20))
    
    def return_dict(self, is_return_receiver: bool = False):
        result=super().return_dict(is_return_receiver)
        result['message'['body']]=self.body
        result['message'['is_multiple_choice']]=self.is_multiple_choice
        result['message'['options']]=self.options
        result['message'['results']]=self.results

        return result
        


class JudgeMail(MailCenter):
    body=db.StringField(require=True)
    options = db.ListField(
        db.StringField(), 
        required=True, 
        min_items=2, 
        max_items=2,
        default=['是','否']
        )
    result=db.StringField(choices=options)

    def return_dict(self, is_return_receiver: bool = False):
        result=super().return_dict(is_return_receiver)
        result['message'['body']]=self.body
        result['message'['options']]=self.options
        result['message'['result']]=self.result
        return result


