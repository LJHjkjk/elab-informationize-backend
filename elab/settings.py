class BaseConfig:
    # file
    UPLOADED_AVATARS_DEST = 'static/avatars'
    UPLOADED_PHOTOGRAPHS_DEST = 'asset/photographs'

    # elab
    FRONT_INDEX_URL='http://localhost:3000'
    SECRET_KEY='aaa'
    HOST='example.com'
    PORT=''
    ADMIN_PASSWARD='123132'
    OWNER_NAME='built-in'

    # flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123123@localhost/casdoor'

    # flask-oidc
    OIDC_CLIENT_SECRETS = 'oidc_client_secrets.json'
    OIDC_SCOPES = ['openid', 'email', 'profile']
    #OVERWRITE_REDIRECT_URI = FRONT_INDEX_URL
    OIDC_ID_TOKEN_COOKIE_TTL=600000


Config={
    'development':BaseConfig,
    'production': BaseConfig,
}

