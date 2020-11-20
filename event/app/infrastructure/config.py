import os

assert 'APP_ENV' in os.environ, 'MAKE SURE TO SET AN ENVIRONMENT'
basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.split(basedir)[0]


class Config:
    PORT = 8083
    SECRET_KEY = os.environ.get('SECRET', 'secret')
    SQL_URI = 'sqlite:///app.db'
    SCOPES = {
        "me": "Read information about the current user.",
        "event": "Has the opportunity to send event"
    }
    CLIENT_ID = 'event_service'
    BASEDIR = basedir
    LOG_FOLDER = os.path.join(BASEDIR, 'logs')
    LOG_FILENAME = 'app.log'
    LOG_FILE_PATH = os.path.join(LOG_FOLDER, LOG_FILENAME)
    LOGGER_NAME = 'event_logger'
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    EVENT_NOTIFICATION_SUFFIXE = ':EventNotification'
    PUBLISHED_LIST_SUFFIXED = ':PublishedList'
    SUBSCRIBER_LIST_SUFFIXE = ':SubscriberList'


class DockerConfig(Config):
    PORT = 8080
    DB_NAME = os.environ.get('DB_NAME', 'database')
    DB_PWD = os.environ.get('DB_PWD', 'password')
    DB_USER = os.environ.get('DB_USER', 'user')
    SQL_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PWD}@database/{DB_NAME}'
    REDIS_HOST = 'redis'


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
