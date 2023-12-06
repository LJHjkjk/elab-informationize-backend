from flask import Blueprint,jsonify,request
from elab.extensions import oidc,sqlAlchemy as db
from flask_cors import cross_origin
from elab.db.user import UserInfo,User,UserView
from datetime import datetime
from flask_uploads import UploadSet, configure_uploads, IMAGES

user_blueprint=Blueprint('/user',__name__)

# 获取用户信息
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
			'message':user.return_to_dict(),
			'permission':{}
		})
	else :
		return jsonify({
				'result':'no',
				'message':'User not found'
		}),404


# 修改用户信息
@user_blueprint.route('',methods=['POST'])
@oidc.require_login
def modify_user_info():
	def response_json(message,result='no',code=400):
		return jsonify({
			'result':result,
			'message':message,
		}),code
	
	# 查询用户
	id=oidc.user_getfield('name')
	user_info=UserInfo.query.get(id)
	user=User.query.filter_by(name=id)
	if user==None or user_init==None:
		return response_json('没有这个用户')
	
	# 验证信息
	form=request.get_json()
	if form==None:
		return response_json('请提交格式正确的数据')

	# 修改用户信息
	try:
		user_info.gender=form.get('gender')
		user_info.college=form.get('college')
		user_info.major=form.get('major')
		user_info.classname=form.get('classname')
		user_info.native_place=form.get('native_place')
		user_info.reason_for_application=form.get('reason_for_application')
		user_info.join_date=datetime.strptime(form.get('join_date'), "%Y-%m-%d").date()\
				if 'join_date' in form else None, 
		user_info.time_of_enrollment=datetime.strptime(form.get('time_of_enrollment'), "%Y-%m-%d").date()\
				if 'time_of_enrollment' in form else None, 	

		user.email=form.get('email')
		user.phone=form.get('phone')
		db.session.commit()
		return response_json('修改成功','ok',200)
	except Exception as e:
		return response_json(e)
	

# 上传头像
@user_blueprint.route('/avatar',methods=['POST'])
@oidc.require_login
def upload_avatar():
	pass


# 上传个人照片
@user_blueprint.route('/photograph',methods=['POST'])
@oidc.require_login
def upload_photograph():
	pass



def user_init(api_blueprint):
  api_blueprint.register_blueprint(user_blueprint,url_prefix='/user')

