import os
import json

def read_site_info(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data


class BaseConfig:
    # file
    UPLOADED_AVATARS_DEST = 'static/avatars'
    UPLOADED_PHOTOGRAPHS_DEST = 'asset/photographs'

    # elab
    ADMIN_PASSWARD='123132'
    SITE_INFO=read_site_info('site_info.json')


    # flask-oidc
    OIDC_CLIENT_SECRETS = 'oidc_client_secrets.json'
    OIDC_SCOPES = ['openid', 'email', 'profile']
    OIDC_ID_TOKEN_COOKIE_TTL=600000
    OIDC_COOKIE_SECURE=False


class DevelopmentConfig(BaseConfig):
    # elab
    FRONT_INDEX_URL="http://localhost:3000"
    SECRET_KEY='aaa'
    OWNER_NAME='built-in'
    HOST_ADDRESS='localhost:5000'
    ROOT_URL='http://'+HOST_ADDRESS

    # flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123123@localhost/casdoor'


class ProductionConfig(BaseConfig):
    # elab
    HOST_ADDRESS=os.environ.get('HOST_ADRRESS')
    ROOT_URL=f'http://{HOST_ADDRESS}'
    FRONT_INDEX_URL=value = os.environ.get('FRONT_INDEX_URL')
    SECRET_KEY= os.environ.get('SECRET_KEY')
    OWNER_NAME=os.environ.get('OWNER_NAME')
    # flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI=f'mysql+pymysql://root:{os.environ.get("DB_PASSWARD")}@{os.environ.get("DB_ADDRESS")}/casdoor'
    # oidc
    OVERWRITE_REDIRECT_URI = "http://"+os.environ.get('CASDOOR_ADDRESS')+"/oidc_callback"


Config={
    'development':ProductionConfig,
    'production': ProductionConfig,
}

