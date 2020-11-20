import requests

from tcommon.authenticate_token.model import User
from tcommon.authenticate_token.unauthorized_exception import UnauthorizedException
from tcommon.config import app_config
from tcommon.log import logger


def get_user_info_by_token(token: str) -> User:
    url = app_config.TOKEN_SERVICE_URL + app_config.TOKEN_INFO
    logger.info(f"GET {url}")
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if r.status_code != 200:
        if r.status_code == 401:
            raise UnauthorizedException(str(r.json()))
        else:
            raise Exception(f'An error occured while getting {url} : status code {r.status_code}, message {r.json()}')
    return User(**r.json())
