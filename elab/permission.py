from elab.db.permission import Positon,Duty,PositonDutyMap,MemberDutyMap,db
from elab.response import response_message
from elab.extensions import oidc
from functools import wraps



def check_permission(duty, resp=None):
    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal resp
            if resp is None:
                resp = response_message('权限不足')

            # 找到请求人
            user_id = oidc.user_getfield('name')
            # 验证是否有权限
            check = MemberDutyMap.query.filter_by(member_id=user_id, duty=duty).one()
            if check is None:
                return resp
            else:
                return func(*args, **kwargs)
        return wrapper
    return my_decorator
