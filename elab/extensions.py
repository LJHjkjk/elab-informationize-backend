'''
导入扩展
'''
from flask_oidc import OpenIDConnect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from elab.file_manage import FileManage



# 普通扩展
oidc = OpenIDConnect()
cors=CORS(origins=['*'],supports_credentials=True)
sqlAlchemy=SQLAlchemy()
file_manage=FileManage()

# 自定义文件扩展

