'''
导入扩展
'''

from flask_oidc import OpenIDConnect
from flask_cors import CORS


oidc = OpenIDConnect()
cors=CORS(origins=['http://localhost:3000'])



