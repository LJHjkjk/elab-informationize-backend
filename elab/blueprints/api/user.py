from flask import Blueprint
from elab.extensions import oidc


user_blueprint=Blueprint('user',__name__)


@user_blueprint.route('/user/<int:id>')
@oidc.require_login
def get(id):
    # 获取用户信息
    

    # 返回用户信息

    return 

def user_init(api_blueprint):
    api_blueprint.register_blueprint(user_blueprint,)

    
