import os

assert 'APP_ENV' in os.environ, 'MAKE SURE TO SET AN ENVIRONMENT'
basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.split(basedir)[0]


class Config:
    PORT = 8081
    SECRET_KEY = os.environ.get('SECRET', 'secret')
    SQL_URI = 'sqlite:///app.db'
    CLIENT_ID = '123'
    SCOPES = {
        "me": "Read information about the current user.",
        "all": "Read information about everyone",
    }
    BASEDIR = basedir
    LOG_FOLDER = os.path.join(BASEDIR, 'logs')
    LOG_FILENAME = 'app.log'
    LOG_FILE_PATH = os.path.join(LOG_FOLDER, LOG_FILENAME)
    LOGGER_NAME = 'users_logger'


class DockerConfig(Config):
    PORT = 8080
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
