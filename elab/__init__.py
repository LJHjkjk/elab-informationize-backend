'''
创建app,注册变量蓝图等
'''

from flask import Flask
import os


from elab.extensions import oidc,cors,mongodb,sqlAlchemy
from elab.blueprints import blueprint

from elab.settings import Config
from elab.db import init_db,drop_db,forge_db
import click



def create_app(config_name=None):
    '''
    工厂函数
    flask run会自动调用这个函数 
    '''


    # 根据运行模式加载配置
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app=Flask(__name__)
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
    cors.init_app(app,supports_credentials=True,origins=['*'])
    oidc.init_app(app)
    mongodb.init_app(app)
    sqlAlchemy.init_app(app)

    
def register_blueprints(app):
    '''
    注册flask蓝图
    '''
    app.register_blueprint(blueprint)

def register_commands(app):
    '''
    注册CLI命令
    '''
    # 初始化数据库
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            # 删除原来的数据
            drop_db()
            click.echo('成功删除')
        # 创建新数据
        init_db()
        click.echo('成功创建')


    @app.cli.command()
    def forge():
        forge_db()




def register_errorhandlers(app):
    '''
    注册全局默认错误处理界面
    '''