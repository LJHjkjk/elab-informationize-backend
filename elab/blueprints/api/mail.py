from flask import Blueprint,jsonify,request
from bson import ObjectId


from elab.extensions import oidc,mongodb as mg
from db.mail import MailCenter,UserMailbox,NotifyMail
from form.mail import SendNotifyMail

mail_blueprint=Blueprint('mail',__name__)


@mail_blueprint.route('/',methods=['GET'])
@oidc.require_login
def get_mail_info():
    # 获取请求者id
    requester_id=oidc.user_getfield('name')
  
    # 找到邮件
    mail_id=request.args.get('mail_id')
    mail=MailCenter.object.get(id=mail_id)

    if not mail:
        return jsonify({
            'result':'no',
            'message':'Mail not found'
        }),404
    # 判读是否为邮件接受对象
    if requester_id not in mail.receivers_id:
        return jsonify({
            'result':'no',
            'message':'没有权限'
        },404)

    # 返回邮件数据
    return jsonify(mail.return_dict())
    

@mail_blueprint.route('/',methods=['POST'])
@oidc.require_login
def send_mail():
    # 获取表单
    mail_type=request.args.get('mail_type')

    error_messge={
            'result':'no',
            'message':'fail to send'
        }
    
    mail_form=SendNotifyMail()

    if mail_type!='notify' or mail_type.validate_on_submit():
        return jsonify(error_messge)

    # 找到发布者
    sender_id=oidc.user_getfield('name')
    sender_id=ObjectId(sender_id)
    sender=UserMailbox.object.get(id=sender_id)

    # 检测接受者是否合法
    receivers_id=mail_form.receivers_id.data
    if not set(receivers_id).issubclass(set(sender.sendable_id)):
        return jsonify(error_messge)
    
# 验证通过，开始添加邮件
    
    # 处理附件 

    # 添加邮件到邮件中心
    new_mail=NotifyMail(
        title=mail_form.title.date,
        type=mail_form.type.date,
        sender_name=sender.name,
        sender_id=sender.id,
        receivers_id=receivers_id,
        is_attachment=mail_form.is_attachment.data
    )
    new_mail.save()
    # 添加邮件到发布者历史中
    sender.send_history.append(str(new_mail.id))
    # 添加邮件到接收者收件箱中
    for i in receivers_id:
        receiver_id=ObjectId(i)
        receiver=UserMailbox.object.get(id=receiver_id)
        receiver.unfinished_mailbox.append(str(new_mail.id))

    return jsonify({
        'result':'ok',
        'message':'发布成功',
    })


@mail_blueprint.route('/mailbox',methods=['GET'])
@oidc.require_login
def get_mailbox():
    mails={
        'unfinished':None,
        'finished':None
    }
    # 查询用户
    user_id=oidc.user_getfield('name')
    user=UserMailbox.object.get(id=ObjectId(user_id))

    # 查询邮件
    unfinished=[]
    finished=[]
    for i in user.unfinished:
        mail=MailCenter.object.get(ObjectId(i))
        unfinished.append(mail.return_dict())

    for i in user.finished:
        mail=MailCenter.object.get(ObjectId(i))
        finished.append(mail.return_dict())
    # 返回邮件
    mails['unfinished']=unfinished
    mails['finished']=finished

    return jsonify({
        'result':'ok',
        'messgae':mails
    })


@mail_blueprint.route('/sendable-objects',methods=['GET'])
@oidc.require_login
def get_sendable_objects():
    # 查询可发送对象

    # 返回列表
    pass


@mail_blueprint.route('/deal',methods=['POST'])
@oidc.require_login
def deal_mail():
    mail_id=request.args.get('mail_id')
    # 查看是否可以处理邮件

    # 进入处理

    # 返沪处理结果

    pass



def mail_init(api_blueprint):
    api_blueprint.register_blueprint(mail_blueprint)