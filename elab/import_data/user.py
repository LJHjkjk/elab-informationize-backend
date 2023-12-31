from elab.db.user import User,UserInfo
from elab.extensions import sqlAlchemy as db

from flask import current_app
from .index import open_file

# 从表格中导入成员信息
def import_user_info(path):
    df=open_file(path)
    # 添加用户
    for index,row in df.iterrows():
        new_user=User(
            id=str(index),
            name=row['id'],
            display_name=row['name'],
            owner=current_app.config['OWNER_NAME'],
            password=row['id'],
        )
        new_user_info=UserInfo(
            id=row['id'],
            name=row['name'],
            department=row['department'],

        )
        db.session.add(new_user)
        db.session.add(new_user_info)

    db.session.commit()
    


    # 创建邮箱

    from elab.db.user import UserView
    from elab.db.mail import UserMailbox
    users=UserView.query.all()

    for user in users:
        user_mailbox=UserMailbox(
            id=user.id,
            name=user.name,
        )
        db.session.add(user_mailbox)
        db.session.commit()




