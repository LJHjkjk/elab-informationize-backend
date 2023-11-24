from flask import Blueprint,jsonify,request
from elab.extensions import oidc,sqlAlchemy as sql
from flask_cors import cross_origin
from elab.db.user import UserInfo,UserView



user_blueprint=Blueprint('/user',__name__)


@user_blueprint.route('',methods=['GET'])
@oidc.require_login
def get_user_info():
	id=request.args.get('user_id')
	print(id)
	# 检测是否为本人
	if id!=oidc.user_getfield('name'):
		return jsonify({
			'result':'no',
			'message':'不能获取其他用户信息'+str(id)+str(oidc.user_getfield('name')),			
		}),404

	# 获取用户信息
	user=UserView.query.filter(UserView.id==id).one()

	if user:
		# 返回用户信息
		return jsonify({
			'result':'ok',
			'message':{
				'id':user.id,
				'name':user.name,
				'email':user.email,
				'phone':user.phone,
				'award_winning_experience':user.award_winning_experience,
				'project_experience':user.project_experience,
				'position':user.position,
				'department':user.department,
				'avatar':user.avatar,
			},
			'permission':{

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
  api_blueprint.register_blueprint(user_blueprint,url_prefix='/user')

