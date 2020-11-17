import os

assert 'APP_ENV' in os.environ, 'MAKE SURE TO SET AN ENVIRONMENT'


class Config:
    PORT = 8081
    SECRET_KEY = os.environ.get('SECRET', 'secret')
    SQL_URI = 'sqlite:///app.db'
    TOKEN_SERVICE_URL = 'http://localhost:8082/api/v1/token_controller/'
    TOKEN_CREATION = 'token'
    TOKEN_INFO = 'tokenInfo'
    CLIENT_ID = 'my_client_id'
    SIGN_IN_PAGE = 'auth'
    SCOPES = {
        "me": "Read information about the current user.",
        "all": "Read information about everyone",
    }


class DockerConfig(Config):
    PORT = 8080
    TOKEN_SERVICE_URL = 'http://token:8080/api/v1/token_controller/'
    DB_NAME = os.environ.get('DB_NAME', 'database')
    DB_PWD = os.environ.get('DB_PWD', 'password')
    DB_USER = os.environ.get('DB_USER', 'user')
    SQL_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PWD}@database/{DB_NAME}'


class TestConfig(Config):
    SQL_URI = 'sqlite:///test.db'


env = os.environ['APP_ENV'].upper()
if env == 'TEST':
    app_config = TestConfig
elif env == 'PRD':
    app_config = DockerConfig
else:
    app_config = Config

print(app_config)
