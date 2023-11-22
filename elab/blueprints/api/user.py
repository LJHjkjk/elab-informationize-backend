from flask import Blueprint,jsonify,request
from elab.extensions import oidc,sqlAlchemy as sql

from db.user import UserInfo,UserView



user_blueprint=Blueprint('user',__name__)


@user_blueprint.route('',methods=['GET'])
@oidc.require_login
def get_user_info():
	id=request.args.get('user_id')
	# 检测是否为本人
	if id!=oidc.user_getfield('name'):
		return jsonify({
			'result':'no',
			'message':'不能获取其他用户信息',			
		},404)


	# 获取用户信息
	user=UserView.query.filter_by(id=id).one()

	if user:
		# 返回用户信息
		return jsonify({
			'result':'ok',
			'message':{
				'id':user.id,
				'name':user.name,
				'avatar':user.avatar,
			}
		})
	else :
		return jsonify({
				'result':'no',
				'message':'User not found'
		}),404

	

@user_blueprint.route('/<int:id>',methods=['PATCH'])
@oidc.require_login
def post_user_info(id):
	# 检测是否为本人

	# 可以修改用户信息
	pass



def user_init(api_blueprint):
  api_blueprint.register_blueprint(user_blueprint)

