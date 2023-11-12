'''
创建app，注册变量蓝图等
'''

from flask import Flask
import os


from elab.extensions import oidc,cors
from elab.blueprints import blueprint

from elab.settings import Config



def create_app(config_name=None):
    '''
    工厂函数
    flask run会自动调用这个函数 
    '''
    app=Flask(__name__)

    # 根据运行模式加载配置
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask('elab')
    app.config.from_object(Config[config_name])

    # 注册
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errorhandlers(app)

    
    return app


def register_extensions(app):
    '''
    注册flask扩展
    '''
    cors.init_app(app)
    oidc.init_app(app)

    
def register_blueprints(app):
    '''
    注册flask蓝图
    '''
    app.register_blueprint(blueprint)

def register_commands(app):
    '''
    注册CLI命令
    '''

def register_errorhandlers(app):
    '''
    注册全局默认错误处理界面
    '''



