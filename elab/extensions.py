'''
导入扩展
'''

from flask_oidc import OpenIDConnect
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy




oidc = OpenIDConnect()
cors=CORS(origins=['*'],supports_credentials=True)
mongodb = MongoEngine()
sqlAlchemy=SQLAlchemy()



