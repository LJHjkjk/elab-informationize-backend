



class BaseConfig:
    SECRET_KEY='aaa'

    # elab
    FRONT_INDEX_URL='http://localhost:3000'

    #flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123123@localhost/casdoor'


    # flask-oidc
    OIDC_CLIENT_SECRETS = 'oidc_client_secrets.json'
    OIDC_SCOPES = ['openid', 'email', 'profile']
    #OVERWRITE_REDIRECT_URI = FRONT_INDEX_URL
    OIDC_ID_TOKEN_COOKIE_TTL=600000

    # flask-mongodbengine
    MONGODB_SETTINGS={
        'db':'elab',
        'host':'localhost',
        'port':27017,
        'username':'root',
        'password':'123123'
    }

Config={
    'development':BaseConfig,
    'production': BaseConfig,
}

