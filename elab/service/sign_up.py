from typing import Any
import schedule
from datetime import datetime
from elab.db.signin import SignIn as SU,db
import time
import qrcode
from flask import current_app
import os
import threading
import secrets
from elab.db.user import UserView

# 签到基类
class SignIn:
    def __init__(self,id,initiator_id,initiator_name,title,start_time,end_time,
                 sign_in_object,sign_in_method,start_job,end_job,result_import=None,
                 initiate_time=None):
        self.id=id
        # 发起人
        self.initiator_id=initiator_id
        self.initiator_name=initiator_name
        # 签到主题
        self.title=title
        # 发起时间
        self.initiate_time=initiate_time if initiate_time!=None  else datetime.now() 
        # 签到时间
        self.start_time=start_time
        self.end_time=end_time
        # 签到对象
        self.sign_in_object=sign_in_object
        # 签到方式
        self.sign_in_method=sign_in_method
        # 签到结果
        self.result_import=result_import

        # 任务调度
        self.start_job=start_job
        self.end_job=end_job

        self.state='no'
    
    # 签到
    def check_in(self,user_id,**kwargs):
        # 判断签到状态
        if self.state!='doing':
            raise Exception('不在签到时间')
        # 签到方式检验
        self.sign_in_method.check_in(**kwargs)
        # 签到对象检验
        self.sign_in_object.record(user_id)
        # 签到成功

             

    
    def return_to_dict(self,is_get_details=False,user_info=False):
        result={
            'id':self.id,
            'state':self.state,
            'title':self.title,
            'initiator_name':self.initiator_name,
            'initiate_time':self.initiate_time.timestamp(),
            'start_time':self.start_time.strftime("%H:%M:%S"),
            'end_time':self.end_time.strftime("%H:%M:%S"),
            'sign_in_method':self.sign_in_method.type,
        }
        if is_get_details:
            result.update({
            'sign_in_object':self.sign_in_object.return_to_dict(user_info),
            'sign_in_method':self.sign_in_method.return_to_dict(),
            'result_import':self.result_import,
        })
        return result

    def __str__(self) -> str:
        return str(self.return_to_dict())


# 签到方式
class SignInMethod:
    '''
    签到方式基类
    '''
    def __init__(self):
        pass
    # 签到
    def check_in(self,**kwargs):
        pass
    
    def return_to_dict(self):
        return {
            'type':self.type
        }
 

class CommonSignIn(SignInMethod):
    '''
    普通签到
    '''
    type='common'
    def __init__(self):
        super().__init__()
        
    def check_in(self,**kwargs):
        return super().check_in(**kwargs)

    def return_to_dict(self):
        return super().return_to_dict()
    
    

class QRcodeSignIn(SignInMethod):
    '''
    二维码签到
    '''
    type='QRcode'
    def __init__(self,id,position):
        super().__init__()
        # 生成token
        self.token=secrets.token_hex(16)
        # 生成二维码
        self.QRcode_address,self.get_QRcode_url=self.generate_qrcode(id,position,self.token)


    
    def return_to_dict(self):
        result=super().return_to_dict()
        # 添加二维码获取链接
        result['get_QRcode_url']=self.get_QRcode_url
        return result
    
    def check_in(self,token,**kwargs):
        super().check_in(**kwargs)
        # 验证token
        if token!=self.token:
            raise Exception('token不正确')


    @classmethod
    def generate_qrcode(cls,id,position,token):
        img = qrcode.make(current_app.config['ROOT_URL']+f'/api/service/signup/check-id?sign_in_id={id}&token={token}')
        address=f"{position}/{id}.png"
        img.save(address)
        url=current_app.config['ROOT_URL']+f'/api/service/signin/QRcode?id={id}'
        return address,url
        


# 签到对象
class SignInObject:
    '''
    签到对象基类
    '''
    def __init__(self,sign_in_object):
        self.member=sign_in_object
        self.result=[]
    def record(self,user_id):
        '''
        记录签到人员
        '''
        # 如果已经签到，则返回错误
        if user_id in self.result:
            raise Exception('已经完成签到，不可重复签到')
        # 添加到签到人员中
        self.result.append(user_id)
 
    def return_to_dict(self,user_info):
        finished_sign_in=[]
        if user_info:
            for i in self.result:
                user=UserView.query.get(i)
                finished_sign_in.append({
                    'id':i,
                    'name':user.name,
                })
        else:
            finished_sign_in=self.result
        return {
            'type':self.type,
            'finished':finished_sign_in,
        }


class CustomSignIn(SignInObject):
    '''
    自定义签到
    '''    
    type='custom'

    def __init__(self,sign_in_object:list):
        super().__init__(sign_in_object)
        self.undone=sign_in_object.copy()

    def record(self, user_id):
        super().record(user_id)
        # 从未签到中删除
        self.undone.remove(user_id)

    
    def return_to_dict(self,user_info):
        result=super().return_to_dict(user_info)
        unfunished_sign_in=[]
        if user_info:
            for i in self.undone:
                user=UserView.query.get(i)
                unfunished_sign_in.append({
                    'id':i,
                    'name':user.name,
                })
        else:
            unfunished_sign_in=self.undone
        result['unfinished']=unfunished_sign_in
        return result


class HallSignIn(SignInObject):
    '''
    大厅签到
    '''
    type='hall'

    def __init__(self,sign_in_object:None):
        super().__init__(sign_in_object)
    def record(self, user_id):
        return super().record(user_id)
    def return_to_dict(self,user_info):
        return super().return_to_dict(user_info)


'''
设计：
签到管理类：可以添加签到，定时执行签到，定时删除签到，将签到持久化储存，成员签到
分为
'''
class SignInManager:
    def __init__(self,interval=10,QRcode_folder='asset/QRcode'):
        '''
        interval为任务调度检测时间间隔
        process成员为子进程，专门执行任务调度
        '''
        # 签到池
        self.pool={
            'hall':{},
            'custom':{}
        }
        # 成员的个人签到表
        self.personal_task={}
        # 任务调度进程
        self.thread = threading.Thread(target=self.run)
        self.interval=interval

        # 创建二维码文件夹
        self.QRcode_folder=QRcode_folder
        if not os.path.exists(QRcode_folder):
            os.makedirs(QRcode_folder)


    def set_app(self,app):
        self.app=app

    # 任务调度线程运行
    def start(self):
        self.thread.start()

    def run(self):        
        while True:
            with self.app.app_context():
                schedule.run_pending()
                time.sleep(self.interval)


    # 发起签到
    def initate_sign_in(self,initiator_id,initiator_name,title,start_time,end_time,sign_in_object_type,
                        sign_in_method,result_import,sign_in_object=None):
        # 设置签到对象
        if sign_in_object_type=='hall':
            sign_in_object=HallSignIn(sign_in_object)
        elif sign_in_object_type=='custom':
            sign_in_object=CustomSignIn(sign_in_object)
        else:
            raise Exception('签到对象错误')
        
        # 将签到添加到数据库中
        initiate_time=datetime.now()
        su=SU(initiator_id=initiator_id,
              initiator_name=initiator_name,
              title=title,
              start_time=start_time,
              end_time=end_time,
              sign_in_object_type=sign_in_object_type,
              sign_in_method=sign_in_method,
              result_import=result_import,
              initiate_time=initiate_time)
        
        db.session.add(su)
        db.session.commit()
        id=su.id
        # 设置签到方式
        if sign_in_method=='common':
            sign_in_method=CommonSignIn()
        elif sign_in_method=='QRcode':
            sign_in_method=QRcodeSignIn(id,self.QRcode_folder)
        else:
            raise Exception('签到方式错误')
        # 设置调度任务
        start_job=schedule.every().day.at(start_time.strftime("%H:%M:%S")).do(self.start_sign_in,
                        sign_in_id=id,sign_in_object_type=sign_in_object_type,sign_in_object=sign_in_object)
        end_job=schedule.every().day.at(end_time.strftime("%H:%M:%S")).do(self.end_sign_in,
                sign_in_id=id,sign_in_object_type=sign_in_object_type)
        

        # 创建签到
        sign_in=SignIn(id,initiator_id,initiator_name,title,start_time,end_time,
                       sign_in_object,sign_in_method,start_job,end_job,result_import,initiate_time=initiate_time)
        # 添加到签到池中
        self.pool[sign_in_object_type][id]=sign_in

    # 开始签到
    def start_sign_in(self,sign_in_id,sign_in_object,sign_in_object_type):
        print(f'{sign_in_id}开始签到')
        # 将用户的签到添加到个人签到
        if sign_in_object_type=='custom':
            self.add_personal_tasks(sign_in_id,sign_in_object)
        sign_in=self.find(sign_in_id)
        sign_in.state='doing'
        # 修改状态为正在签到
        su=SU.query.get(sign_in_id)
        su.state='doing'
        db.session.commit()
        return schedule.CancelJob
    
    # 获取详细信息
    def get_sign_in_details(self,sign_in_id,is_get_QRcode=True):
        return self.return_to_dict(sign_in_id,is_get_QRcode)

    # 获取个人签到任务
    def get_personal_task(self,user_id):
        sign_in_list=self.personal_task.get(user_id,[])
        return self.return_to_dict(sign_in_list)
    
    # 获取签到大厅的签到任务
    def get_hall(self):
        result=[]
        for i in self.pool['hall']:
            result.append(self.pool['hall'][i].return_to_dict()) 
        return result
    
    
    # 结束签到
    def end_sign_in(self,sign_in_id,sign_in_object_type):
        print(f'{sign_in_id}结束签到')
        # 将签到从字典中删除
        sign_in=self.pool[sign_in_object_type].pop(sign_in_id)
        # 将信息添加入数据库中
        su=SU.query.get(sign_in_id)
        su.state='done'
        su.initiate_time=sign_in.initiate_time
        su.sign_in_object=sign_in.sign_in_object.member
        su.result=sign_in.sign_in_object.return_to_dict(user_info=True)
        db.session.commit()

        # 删除二维码
        if sign_in.sign_in_method.type=='QRcode':
            try:
                os.remove(sign_in.sign_in_method.QRcode_address)
            except FileNotFoundError:
                print(f"File '{sign_in.sign_in_method.QRcode_address}' not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        # 将用户的签到从个人签到中删除
        if sign_in.sign_in_object.type=='custom':
            self.delete_personal_tasks(sign_in_id,sign_in.sign_in_object.undone)

        return schedule.CancelJob


    # 成员签到
    def check_in(self,sign_in_id,user_id,**kwargs):
        # 找到签到
        sign_in=self.find(sign_in_id)
        if sign_in==None:
            return '没有此签到'
        sign_in.check_in(user_id,**kwargs)
        # 如果成功，删除个人的签到任务
        if sign_in.sign_in_object.type=='custom':
            self.delete_personal_task(sign_in_id=sign_in_id,user_id=user_id)


    
    # 找到签到
    def find(self,sign_in_id):
        for i in self.pool:
            sign_in=self.pool[i].get(sign_in_id)
            if sign_in!=None:
                return sign_in
        return None

    def return_to_dict(self,objects,is_get_details=False):
        if type(objects)==list:
            result=[]
            for i in objects:
                result.append(self.find(i).return_to_dict(is_get_details))
            return result
        else:
            return self.find(objects).return_to_dict(is_get_details)


    def add_personal_tasks(self,sign_in_id,sign_in_object):
        if sign_in_object.member == None:
            return
        for i in sign_in_object.member:
            if self.personal_task.get(i)==None:
                self.personal_task[i]=[sign_in_id]
            else:
                self.personal_task[i].append(sign_in_id)

    def delete_personal_tasks(self,sign_in_id,sign_in_object):
        if sign_in_object == None:
            return
        for user_id in sign_in_object:
                self.personal_task[user_id].remove(sign_in_id)


    def delete_personal_task(self,sign_in_id,user_id):
        self.personal_task[user_id].remove(sign_in_id)