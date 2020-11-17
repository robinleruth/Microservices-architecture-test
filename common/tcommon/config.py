import os

assert 'APP_ENV' in os.environ, 'MAKE SURE TO SET AN ENVIRONMENT'


class Config:
    TOKEN_SERVICE_URL = 'http://localhost:8082/api/v1/token_controller/'
    TOKEN_CREATION = 'token'
    SIGN_IN_PAGE = 'auth'
    TOKEN_INFO = 'tokenInfo'
    CLIENT_ID = 'my_client_id'
    SCOPES = {
        "me": "Read information about the current user."
    }


class DockerConfig(Config):
    TOKEN_SERVICE_URL = 'http://192.168.33.10:8082/api/v1/token_controller/'


class TestConfig(Config):
    pass


env = os.environ['APP_ENV'].upper()
if env == 'TEST':
    app_config = TestConfig
elif env == 'PRD':
    app_config = DockerConfig
else:
    app_config = Config

print(app_config)
