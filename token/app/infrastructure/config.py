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


class DockerConfig(Config):
    PORT = 8080
    USER_SERVICE_URL = 'http://users:8080/api/v1/user_controller/me'


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
