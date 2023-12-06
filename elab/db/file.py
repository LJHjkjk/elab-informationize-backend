from elab.db import sqlAlchemy as db
from datetime import datetime
from enum import Enum

class FileType(Enum):
    # 用户头像
    AVATAR='avatar'
    # 用户照片
    PHOTOGRAPH='photograph'
    # 无
    NONE='none'


class File(db.Model):
    # 文件名
    name=db.Column(db.String(200),primary_key=True)
    # 文件类型
    type=db.Column(db.Enum(FileType),nullable=False)
    # 储存路径
    path=db.Column(db.String(200),nullable=False)
    # 上传时间
    upload_datatime=db.Column(db.DateTime(),default=datetime.now())
    # 拥有者id
    owner_id=db.Column(db.String(100))
    # 拥有者姓名
    owner_name=db.Column(db.String(100))
    # 文件描述
    describe=db.Column(db.String(100))



def init_file():
    db.metadata.create_all(bind=db.engine, tables=[File.__table__])


def drop_file():
    try:
        db.session.execute(db.text('drop table if exists file'))
        db.session.commit()
    except Exception as e:
        print(e)


def forge_file():
    pass