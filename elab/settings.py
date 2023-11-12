



class BaseConfig:
    SECRET_KEY='aaa'

    # elab
    FRONT_INDEX_URL='http://localhost:3000'



    # flask-oidc
    OIDC_CLIENT_SECRETS = 'oidc_client_secrets.json'
    OIDC_SCOPES = ['openid', 'email', 'profile']
    #OVERWRITE_REDIRECT_URI = FRONT_INDEX_URL
    OIDC_ID_TOKEN_COOKIE_TTL=600000

Config={
    'development':BaseConfig,
    'production': BaseConfig,
}

