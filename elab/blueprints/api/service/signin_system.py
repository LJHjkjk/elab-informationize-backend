from flask import Blueprint
from elab.extensions import oidc
from elab.permission import check_permission
from elab.db.user import UserView
from elab.response import response_data,response_message


signin_blueprint=Blueprint('signin',__name__)


# 发起签到
@signin_blueprint.route('',methods=['POST'])
@check_permission('initiate_signin')
@oidc.require_login
def initiate_signin():
    response_message('添加成功','ok',code=200)



# 获取可签到对象
@signin_blueprint.route('/able-object',methods=['GET'])
# @check_permission('initiate_signin')
@oidc.require_login
def get_able_object():
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
                'grade':user.grade
            })
    return response_data(result)



def signin_init(service_blueprint):
    service_blueprint.register_blueprint(signin_blueprint,url_prefix='/signin')
    