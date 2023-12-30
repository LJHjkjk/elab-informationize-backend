from elab.extensions import oidc
from flask import redirect,current_app,request,g,url_for
from flask import Blueprint,make_response
import json
from elab.response import response_message


auth_blueprint=Blueprint('auth',__name__)

 
@auth_blueprint.route('/validate-login')
def validate_login():
    '''
    验证token是否合法
    '''

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


@auth_blueprint.route('/logout')
@oidc.require_login
def logout():
    resp=make_response(redirect(current_app.config['FRONT_INDEX_URL']))
    resp.delete_cookie('oidc_id_token')
    return resp

 
def auth_init(api_blueprint):
    api_blueprint.register_blueprint(auth_blueprint,url_prefix='/auth')
