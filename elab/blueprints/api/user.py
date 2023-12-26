from flask import Blueprint,jsonify,request,current_app,send_file
from elab.extensions import oidc,sqlAlchemy as db
from elab.db.user import UserInfo,User,UserView
from elab.db.file import File,FileType
from datetime import datetime
from elab.response import response_data,response_message
from elab.file_manage import avatars,photographs

user_blueprint=Blueprint('user',__name__)

# 获取用户信息
@user_blueprint.route('',methods=['GET'])
@oidc.require_login
def get_user_info():
	id=request.args.get('user_id')
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
				if 'join_date' in form and form.get('join_date')!=None else None, 
		user_info.grade=form.get('grade')
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
	# 检查
	if 'avatar' not in request.files:
		return response_message('没有头像')
	avatar_file = request.files['avatar']

	user_id=oidc.user_getfield('name')
	user_view=UserView.query.get(user_id)
	# 将头像图片保存
	filename = avatars.save(avatar_file)
	
	url=avatars.url(filename)
	path=avatars.path(filename)

	try:
		# 删除之前的头像图片
		old_avatar=File.query.filter_by(owner_id=user_view.id,type=FileType.AVATAR).first()
		if old_avatar:
			avatars.delete(old_avatar.name)
			db.session.delete(old_avatar)
			db.session.commit()


		# 将头像保存到数据库文件表中
		new_avatar=File(
			name=filename,
			type=FileType.AVATAR,
			path=path,
			owner_id=user_view.id,
			owner_name=user_view.name,
			url=url,
			upload_datatime=datetime.now()
		)
		db.session.add(new_avatar)
		db.session.commit()
		# 修改用户头像url
		user=User.query.filter_by(name=user_id).one()
		user.avatar=url
		db.session.commit()
		return response_message('上传成功','ok',200)
	

	except Exception as e:
		print(e)
		return response_message('服务器错误')



# 上传个人照片
@user_blueprint.route('/photograph',methods=['POST'])
@oidc.require_login
def upload_photograph():
	# 检查
	if 'photograph' not in request.files:
		return response_message('没有照片')
	photograph_file = request.files['photograph']

	user_id=oidc.user_getfield('name')
	user_view=UserView.query.get(user_id)
	# 将照片保存
	filename = photographs.save(photograph_file)
	
	url=photographs.url(filename)
	path=photographs.path(filename)

	try:
		# 删除之前的照片
		old_photograph=File.query.filter_by(owner_id=user_view.id,type=FileType.PHOTOGRAPH).first()
		if old_photograph:
			photographs.delete(old_photograph.name)
			db.session.delete(old_photograph)
			db.session.commit()


		# 将头像保存到数据库文件表中
		new_photograph=File(
			name=filename,
			type=FileType.PHOTOGRAPH,
			path=path,
			owner_id=user_view.id,
			owner_name=user_view.name,
			url=url,
			upload_datatime=datetime.now()
		)
		db.session.add(new_photograph)
		db.session.commit()
		# 修改用户照片url
		user_info=UserInfo.query.filter_by(id=user_id).one()
		user_info.photograph=url
		db.session.commit()
		return response_message('上传成功','ok',200)
	

	except Exception as e:
		print(e)
		return response_message('服务器错误')


# 获取个人照片
@user_blueprint.route('/photograph/<filename>',methods=['GET'])
@oidc.require_login
def get_photograph(filename):
	# 找到这个文件
	photograph_file=File.query.filter_by(name=filename,type=FileType.PHOTOGRAPH).first()
	if not photograph_file:
		return response_message('获取错误')
	
	# 检查权限
	if not photograph_file.owner_id==oidc.user_getfield('name'):
		return response_message('获取错误')
	
	# 返回文件
	return send_file(photographs.path(filename,True))


# 获取所有成员数据
@user_blueprint.route('/members',methods=['GET'])
@oidc.require_login
def get_members():
	# 验证身份
	user_id=oidc.user_getfield('name')
	# 返回数据
	return response_data([i.return_to_dict() for i in UserView.query.all()])


def user_init(api_blueprint):
  api_blueprint.register_blueprint(user_blueprint,url_prefix='/user')

