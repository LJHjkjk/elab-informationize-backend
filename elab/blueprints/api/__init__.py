from flask_restful import Api
from flask import Blueprint,request,current_app
from elab.extensions import oidc
import requests


api_blueprint=Blueprint('api',__name__)

from .auth import auth_init
from .user import user_init
from .mail import mail_init



auth_init(api_blueprint)
user_init(api_blueprint)
mail_init(api_blueprint)




from urllib.parse import urlencode
import json

@oidc.require_login
@api_blueprint.route('/sso')
def sso_login():
    code=request.args.get('code')
    state=request.args.get('state')


	# 使用code向授权服务器发送请求换取token
    headers = {
    	"Accept": "*/*",
    	"Content-Type": "application/x-www-form-urlencoded"
    }

    payload = urlencode({
    	"client_id": oidc.flow.client_id,
    	"client_secret": oidc.flow.client_secret,
    	"grant_type": "authorization_code",
    	"redirect_uri": current_app.config['OVERWRITE_REDIRECT_URI'],
    	"code": code
    })

	# 获取授权token
    token_response = json.loads(requests.request("POST", oidc.flow.token_uri, headers=headers, data=payload).text)

	# 登录
    oidc.set_cookie_id_token(token_response['id_token'])