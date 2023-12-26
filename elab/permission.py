from elab.db.permission import Positon,Duty,PositonDutyMap,MemberDutyMap,db
from elab.response import response_message
from elab.extensions import oidc



def check_permission(duty,response=response_message('权限不足')):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
                # 找到请求人
                user_id=oidc.user_getfield('name')
                # 验证是否有权限
                check=MemberDutyMap.query.filter_by(member_id=user_id,duty=duty).first
                if check is None:
                    return response
                else:                   
                    return func(*args, **kwargs)
        return wrapper
    return my_decorator
