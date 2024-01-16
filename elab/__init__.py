'''
创建app,注册变量蓝图等
'''

from flask import Flask,request,abort
import os

from elab.extensions import oidc,cors,sqlAlchemy,file_manage
from elab.blueprints import blueprint

from elab.settings import Config
from elab.db import init_db,drop_db,forge_db
import click
from flask_uploads import configure_uploads
from elab.import_data import import_user_info,import_user_position,import_positon_info,import_duty_info,\
import_material_info_from_directory,import_material_info

def create_app(config_name=None):
    '''
    工厂函数
    flask run会自动调用这个函数 
    '''


    # 根据运行模式加载配置
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app=Flask(__name__,static_folder=None)
    app.config.from_object(Config[config_name])

    # 注册
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_requesthandlers(app)

    return app


def register_extensions(app):
    '''
    注册flask扩展
    '''
    cors.init_app(app,supports_credentials=True,origins=['*'])
    oidc.init_app(app)
    sqlAlchemy.init_app(app)
    file_manage.init_app(app)

    
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

    # 创建真实数据
    @app.cli.command()
    def forge():
        forge_db()

    # 导入数据
    @app.cli.command('import')
    @click.option('--type','-t', type=click.Choice(['user','position','duty',
                                                    'user_position','all','material',
                                                    'material_directory']))
    @click.option('--path','-p',default=None)
    def import_data(type,path):
        def import_user(path):
            path=path if path is not None else '../material/user.csv'
            import_user_info(path)
            click.echo('用户导入成功')
        def import_duty(path):
            path=path if path is not None else '../material/duty.csv'
            import_duty_info(path)
            click.echo('职责导入成功')
        def import_position(path):
            path=path if path is not None else '../material/position.json'
            import_positon_info(path)
            click.echo('职务导入成功')
        def import_user_postion_default(path):
            return
            import_user_position(path)
            click.echo('用户职务导入成功')
        def import_materail(path):
            path=path if path is not None else '../material/material.csv'
            import_material_info(path)
            click.echo('物料导入成功')
        def import_materail_from_directory(path):
            path=path if path is not None else '../material/material/'
            import_material_info_from_directory(path)
            click.echo('物料目录导入成功')
            

        fun_map={
            'user':import_user,
            'duty':import_duty,
            'position':import_position,
            'user_position':import_user_postion_default,
            'material':import_materail,
            'material_directory':import_materail_from_directory
        }
        if type=='all':
            fun_map['user'](path)
            fun_map['duty'](path)
            fun_map['position'](path)
            fun_map['user_position'](path)
            fun_map['material_directory'](path)
            return
        fun_map[type](path)



def register_requesthandlers(app):
    @app.before_request
    def before_request():
        if request.path.startswith('/_uploads'):
            abort(403, 'Access Forbidden: Paths starting with "/_uploads" are not allowed.')

    @app.before_first_request
    def before_first_request():
        file_manage.set_access()
