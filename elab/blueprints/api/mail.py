from flask import Blueprint,jsonify,request

from elab.extensions import oidc
from elab.db.mail import MailCenter,UserMailbox
from elab.db.user import UserView
from elab.extensions import sqlAlchemy as db

import json

mail_blueprint=Blueprint('mail',__name__)

# 获取某个邮件信息
@mail_blueprint.route('',methods=['GET'])
@oidc.require_login
def get_mail_info():
    # 获取请求者id
    requester_id=oidc.user_getfield('name')
  
    # 找到邮件
    mail_id=int(request.args.get('mail_id'))
    mail=MailCenter.query.get(mail_id)


    if not mail:
        return jsonify({
            'result':'no',
            'message':'Mail not found'
        }),404
    # 判读请求者是否为邮件的可接受对象
    receivers_id=json.loads(mail.receivers_id)
    if requester_id in receivers_id:
        # 将邮件状态修改为已完成
        user=UserMailbox.query.get(requester_id)
        
        
        try:
            json_data=json.loads(user.unfinished_mailbox)
            json_data.remove(mail_id)
            user.unfinished_mailbox=json.dumps(json_data)

            json_data=json.loads(user.finished_mailbox)
            json_data.append(mail_id)
            user.finished_mailbox=json.dumps(json_data)
            db.session.commit()
        except Exception as e:
            ...

        

        return jsonify({
            'result':'ok',
            'data':mail.return_dict(is_body=True)
            })

    if requester_id==mail.sender_id:
        return jsonify({
            'result':'ok',
            'data':mail.return_dict(is_receivers=True,is_body=True)
            })
    
    return jsonify({
            'result':'no',
            'message':'没有权限'
        }),404
    


# 发布邮件
@mail_blueprint.route('',methods=['POST'])
@oidc.require_login
def send_mail():
    def error_message(message):
        error={
                'result':'no',
                'message':message
            }
        return jsonify(error),400
    
    # 获取表单
    form=request.get_json()
    if form==None:
        return error_message('请提交正确的格式')
    # 找到发布者
    sender_id=oidc.user_getfield('name')
    sender=UserMailbox.query.get(sender_id)

    # 表单验证
    required_fields = ['title', 'body', 'receivers']
    for field in required_fields:
        if field not in form:
            return error_message('表单字段不足')
    if 'attachment' not in form:
        form['attachment']=None

    if form['title']==None:
        return error_message('主题不能为空')

    receivers_id=form['receivers']
    if len(receivers_id)==0 or receivers_id==None:
        return error_message('必须选择收件人')
    if not set(receivers_id).issubset({i.id for i in UserMailbox.query.all()}):
        return error_message('接受对象不合法')
    
# 验证通过，开始添加邮件
    # 处理附件

    # 添加邮件 
    sender.send_mail(
        title=form['title'],
        body=form['body'],
        receivers_id=receivers_id
    )

    return jsonify({
        'result':'ok',
        'message':'发布成功',
    })


# 获取收件箱列表
@mail_blueprint.route('/mailbox',methods=['GET'])
@oidc.require_login
def get_mailbox():
    mails=[]
    # 查询用户
    user_id=oidc.user_getfield('name')
    user=UserMailbox.query.get(user_id)

    # 查询邮件

    json_data=json.loads(user.unfinished_mailbox)
    for i in json_data:
        mail=MailCenter.query.get(i)
        mails.append(mail.return_dict(is_body=False))
        mails[-1]['is_new']=True

    json_data=json.loads(user.finished_mailbox)
    for i in json_data:
        mail=MailCenter.query.get(i)
        mails.append(mail.return_dict(is_body=False))
        mails[-1]['is_new']=False


    # 返回排序结果

    return jsonify({
        'result':'ok',
        'data':sorted(mails,key=lambda x:x['pubdate'],reverse = True)
    })



# 获取可以发送邮件的对象
@mail_blueprint.route('/sendable-objects',methods=['GET'])
@oidc.require_login
def get_sendable_objects():
    # 将自己排除的所有人
    users=UserView.query.all()
    result=[]
    id=oidc.user_getfield('name')
    for user in users:
        if user.id!=id:
            result.append({
                'id':user.id,
                'name':user.name,
                'avatar':user.avatar,
                'department':user.department,
            })
    return jsonify(result)


def mail_init(api_blueprint):
    api_blueprint.register_blueprint(mail_blueprint,url_prefix='/mail')