import os

assert 'APP_ENV' in os.environ, 'MAKE SURE TO SET AN ENVIRONMENT'
assert 'SECRET_KEY' in os.environ, 'SECRET_KEY is not in env, generate it with $ openssl rand -hex 32 and put it in env'


class Config:
    PORT = 8082
    # Generate with "$ openssl rand -hex 32"
    SECRET_KEY = os.environ['SECRET_KEY']
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    USER_SERVICE_URL = 'http://localhost:8081/api/v1/user_controller/me'
    SQL_URI = 'sqlite:///app.db'
    ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
    ADMIN_PWD = os.environ.get('ADMIN_PWD', 'admin')
    SCOPES = {
        "me": "Read information about the current user."
    }


class DockerConfig(Config):
    PORT = 8080
    USER_SERVICE_URL = 'http://users:8080/api/v1/user_controller/me'
    DB_NAME = os.environ.get('DB_NAME', 'database')
    DB_PWD = os.environ.get('DB_PWD', 'password')
    DB_USER = os.environ.get('DB_USER', 'user')
    SQL_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PWD}@database/{DB_NAME}'


class TestConfig(Config):
    SQL_URI = 'sqlite:///temp.db'


env = os.environ['APP_ENV'].upper()
if env == 'TEST':
    app_config = TestConfig
elif env == 'PRD':
    app_config = DockerConfig
else:
    app_config = Config

print(app_config)
