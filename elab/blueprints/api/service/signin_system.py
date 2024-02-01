from flask import Blueprint,request,send_from_directory,send_file,current_app
from elab.extensions import oidc
from elab.permission import check_permission
from elab.db.user import UserView
from elab.response import response_data,response_message
from datetime import datetime
from elab.service import sign_in_service
from elab.db.signin import SignIn as SU
signin_blueprint=Blueprint('signin',__name__)

# 查看签到详情
@signin_blueprint.route('',methods=['GET'])
@oidc.require_login
def get_details():
    sign_in_id=request.args.get('id')
    result=sign_in_service.find(int(sign_in_id))
    if result!=None:
        return response_data(result.return_to_dict())
    else:  
        return response_message('没有发现此签到') 


# 发起签到
@signin_blueprint.route('',methods=['POST'])
@check_permission('initiate_signin')
@oidc.require_login
def initiate_signin():
    # 获取参数
    form=request.get_json()
    # 创建签到
    try:
        sign_in_service.initate_sign_in(
            initiator_id=oidc.user_getfield('name'),
            initiator_name=oidc.user_getfield('displayName'),
            title=form['title'],
            start_time=datetime.strptime(form['start_time'], '%H:%M').time(),
            end_time=datetime.strptime(form['end_time'], '%H:%M').time(),
            sign_in_object_type=form['sign_in_object'],
            sign_in_method=form['sign_in_method'],
            result_import=form['sign_in_result'],
            sign_in_object=form['receivers_id'],
        )
        return response_message('添加成功','ok',code=200)
    except Exception as error:
        # 处理错误
        return response_message(str(error))


# 获取可签到对象
@signin_blueprint.route('/able-object',methods=['GET'])
@check_permission('initiate_signin')
@oidc.require_login
def get_able_object():
    users=UserView.query.all()
    result=[]
    for user in users:
        result.append({
            'id':user.id,
            'name':user.name,
            'avatar':user.avatar,
            'department':user.department,
            'grade':user.grade
        })
    return response_data(result)


# 签到
@signin_blueprint.route('/check-in',methods=['GET'])
@oidc.require_login
def check_in():
    # 获取信息
    user_id=oidc.user_getfield('name')
    sign_in_id=int(request.args.get('sign_in_id'))
    token=request.args.get('token')
    if sign_in_id is None:
        return response_message('缺少参数')
    # 验证是否可以签到
    try:
        # 签到成功d
        sign_in_service.check_in(sign_in_id,user_id,token=token)
        return response_message('成功','ok','200')
    except Exception as e:
        return response_message(str(e))



# 获取个人签到
@signin_blueprint.route('/personal',methods=['GET'])
@oidc.require_login
def get_personal_sign_in():
    user_id=oidc.user_getfield('name')
    return response_data(sign_in_service.get_personal_task(user_id))


# 获取签到大厅信息
@signin_blueprint.route('/hall',methods=['GET'])
@oidc.require_login
def get_hall_sign_in():
    return response_data(sign_in_service.get_hall())



# 获取签到二维码
@signin_blueprint.route('/QRcode',methods=['GET'])
@oidc.require_login
def get_QRcode():
    # # 判断是否正确
    user_id=oidc.user_getfield('name')
    sign_in_id=int(request.args.get('id'))
    sign_in=sign_in_service.find(sign_in_id)
    if sign_in==None:
        print(1)
        return response_message('id错误')
    if user_id!=sign_in.initiator_id:
        print(2)
        return response_message('没有权限')
    if sign_in.state!='doing':
        print(3)
        return response_message('不在时间范围内')
    # 返回二维码
    return send_file(current_app.root_path + f'/asset/QRcode/{sign_in_id}.png')


# 获取签到记录列表
@signin_blueprint.route('/records',methods=['GET'])
@check_permission('initiate_signin')
@oidc.require_login
def get_records():
    result=[]
    user_id=oidc.user_getfield('name')
    su=SU.query.filter_by(initiator_id=user_id).order_by(SU.initiate_time.desc()).all()
    for i in su:
        result.append({
            'id':i.id,
            'title':i.title,
            'initiate_time':i.initiate_time.timestamp() if i.initiate_time else None,
            'state':i.state
        })
    return response_data(result)


# 获取签到记录
@signin_blueprint.route('/record',methods=['GET'])
@check_permission('initiate_signin')
@oidc.require_login
def get_record():
    sign_in_id=request.args.get('id')
    if sign_in_id==None:
        return response_message('参数错误')
    sign_in_id=int(sign_in_id)
    su=SU.query.filter_by(id=sign_in_id).first()
    if su==None:
        return response_message('id错误')
    # 返回信息
    if su.state!='done':
        result=sign_in_service.find(sign_in_id).return_to_dict(is_get_details=True,user_info=True)
    else:
        result=su.return_to_dict()
    return response_data(result)
    



# 测试
@signin_blueprint.route('/test',methods=['GET'])
def test():
    hall={}
    custom={}

    for i in sign_in_service.pool['hall']:
        hall[i]=sign_in_service.pool['hall'][i].return_to_dict(is_get_details=True)
    for i in sign_in_service.pool['custom']:
        custom[i]=sign_in_service.pool['custom'][i].return_to_dict(is_get_details=True)
    
    return response_data({
        'hall':hall,
        'custom':custom,
        'personal_task':sign_in_service.personal_task
    })


def signin_init(service_blueprint):
    service_blueprint.register_blueprint(signin_blueprint,url_prefix='/signin')
    