import requests

from app.domain.model.credentials import Credentials
from app.domain.model.user import User
from app.domain.services.token.user_connector import UserConnector
from app.infrastructure.config import app_config
from app.infrastructure.connector.user_service_connection_error import UserServiceConnectionError
from app.infrastructure.log import logger


class ApiUserConnector(UserConnector):
    def get_by_name(self, name: str, credentials: Credentials) -> User:
        logger.info(f'GET {app_config.USER_SERVICE_URL}')
        # TODO: aiohttp
        r = requests.get(app_config.USER_SERVICE_URL, auth=(credentials.username, credentials.password))
        if r.status_code != 200:
            raise UserServiceConnectionError(f'Status code {r.status_code} for GET {app_config.USER_SERVICE_URL}')
        user: User = User(**r.json())
        return user
