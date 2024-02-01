from elab.db import sqlAlchemy as db
from datetime import datetime
import json

class SignIn(db.Model):
    __tablename__='sign_in'
    # id
    id=db.Column(db.Integer,primary_key=True)
    # 状态
    state=db.Column(db.Enum('doing','done','no'),default='no')
    # 名称 
    title=db.Column(db.String(200))
    # 发起人id
    initiator_id=db.Column(db.String(100))
    # 发起人名字
    initiator_name=db.Column(db.String(100))
    # 发起时间
    initiate_time=db.Column(db.DateTime)
    # 开始时间
    start_time=db.Column(db.Time)
    # 结束时间
    end_time=db.Column(db.Time)
    # 签到对象类型
    sign_in_object_type=db.Column(db.Enum('custom','hall'))
    # 签到对象数组
    sign_in_object=db.Column(db.JSON)
    # 签到方式
    sign_in_method=db.Column(db.Enum('QRcode','common'))
    # 结果导入
    result_import=db.Column(db.String(100))
    # 签到结果
    result=db.Column(db.JSON)
    
    def return_to_dict(self):
        return {
            'id':self.id,
            'state':self.state,
            'initiator_name':self.initiator_name,
            'title':self.title,
            'initiate_time':self.initiate_time.timestamp(),
            'start_time':self.start_time.strftime("%H:%M:%S"),
            'end_time':self.end_time.strftime("%H:%M:%S"),
            'sign_in_object':self.result,
            'sign_in_method':{
                'type':self.sign_in_method,
                },
            'result_import':self.result_import,
        }


def init_signup():
    db.metadata.create_all(db.engine,tables=[SignIn.__table__])

def drop_signup():
    db.session.execute(db.text('drop table if exists sign_in'))
    db.session.commit()

def forge_signup():
    pass