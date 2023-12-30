import os

class BaseConfig:
    # file
    UPLOADED_AVATARS_DEST = 'static/avatars'
    UPLOADED_PHOTOGRAPHS_DEST = 'asset/photographs'

    # elab
    ADMIN_PASSWARD='123132'


    # flask-oidc
    OIDC_CLIENT_SECRETS = 'oidc_client_secrets.json'
    OIDC_SCOPES = ['openid', 'email', 'profile']
    OVERWRITE_REDIRECT_URI = "http://"+os.environ.get('HOST_ADRRESS')+"/oidc_callback"
    OIDC_ID_TOKEN_COOKIE_TTL=600000
    OIDC_COOKIE_SECURE=False


class DevelopmentConfig(BaseConfig):
    # elab
    FRONT_INDEX_URL="http://"+os.environ.get('HOST_ADRRESS')
    SECRET_KEY='aaa'
    OWNER_NAME='built-in'



    # flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123123@localhost/casdoor'


class ProductionConfig(BaseConfig):
    # elab
    FRONT_INDEX_URL=value = os.environ.get('FRONT_INDEX_URL')
    SECRET_KEY= os.environ.get('FRONT_INDEX_URL')
    OWNER_NAME=os.environ.get('OWNER_NAME')
    # flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI=f'mysql+pymysql://root:{os.environ.get("DB_PASSWORD")}@localhost/casdoor'


Config={
    'development':DevelopmentConfig,
    'production': ProductionConfig,
}

