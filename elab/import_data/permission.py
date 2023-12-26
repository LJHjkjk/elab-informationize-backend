import pandas as pd
from .index import open_file
from elab.db.permission import Duty,Positon,db
import json
from elab.db.user import UserInfo

# 导入职责
def import_duty_info(path):
    df=open_file(path)

    for _,row in df.iterrows():
        new_duty=Duty(
            name=row['name'],
            type=row['type'],
            displayname=row['display_name'],
            describe=row['describe'],
        )

        db.session.add(new_duty)
    db.session.commit()

# 导入职务，还有其对应的职责,使用json
def import_positon_info(path):
    '''
    json格式:
    {
        position1:{
            duty:[duty1,duty2....],
            include:['*'],
            display_name:display_name1,
            describe:...,
        },
        position2:{
            duty:[duty1,duty2....],
            include:[type1,type2...],
            display_name:display_name2,
            describe:...,
        },
    }
    '''
    with open(path, 'r') as file:
        # 从文件中加载 JSON 数据
        data = json.load(file)
    for position in data:
        # 添加职务
        new_position=Positon(
            name=position,
            display_name=data[position]['display_name'],
            describe=data[position]['describe']
        )
        db.session.add(new_position)
        db.session.commit()
        # 添加对应的职责
        if 'include' in data[position]:
            if len(data[position]['include'])==1 and data[position]['include'][0]=='*':
                new_position.add_duty_typied('*')
            else:
                for i in data[position]['include']:
                    new_position.add_duty_typied(i)
        new_position.add_dutys(data[position].get('duty'))
    db.session.commit()



# 导入用户的职务
def import_user_position(path,defalut_position='member'):
    df=open_file(path)
    for _,row in df.iterrows():
        user_info=UserInfo.query.get(row['id'])
        user_info.add_position(row['positon'])
    # 添加默认职务
    user_info_list=UserInfo.query.all()
    for i in user_info_list:
        if i.position is None:
            i.add_position(defalut_position)
