import os

assert 'APP_ENV' in os.environ, 'MAKE SURE TO SET AN ENVIRONMENT'


class Config:
    PORT = 8081
    SECRET_KEY = os.environ.get('SECRET', 'secret')
    SQL_URI = 'sqlite:///app.db'


class DockerConfig(Config):
    PORT = 8080


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
