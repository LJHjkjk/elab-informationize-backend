from elab.extensions import oidc
from flask import redirect,current_app,request,g
from flask import Blueprint
import json



auth_blueprint=Blueprint('auth',__name__)

 
@auth_blueprint.route('/validate-login')
def validate_login():
    '''
    验证token是否合法
    '''
    token=request.cookies.get('oidc_id_token')
    if not token:
        return {'result':'no','message':"don't have token"}
    

    if not oidc.user_loggedin:
        return {'result':'no','message':''}    
    return {
        'result': 'ok', 
        'message': 'had logined',
        'user_id':oidc.user_getfield('name')
        }




@auth_blueprint.route('/login')
@oidc.require_login
def login():
    return redirect(current_app.config['FRONT_INDEX_URL'])

 
def auth_init(api_blueprint):
    api_blueprint.register_blueprint(auth_blueprint,url_prefix='/auth')



