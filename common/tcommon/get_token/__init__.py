import logging

import requests

from tcommon.authenticate_token import UnauthorizedException
from tcommon.config import app_config

TOKEN = ''
logger = logging.getLogger(__name__)


def get_token(username: str, password: str) -> str:
    """
    :param username: stored in session ?
    :param password: stored in session ?
    :return:token
    """
    global TOKEN
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = f"grant_type=&username={username}&password={password}&scope=&client_id=&client_secret="
    url = app_config.TOKEN_SERVICE_URL + app_config.TOKEN_CREATION
    logger.info(f"POST {url}")
    r = requests.post(url, headers=headers, data=data)
    if r.status_code != 201:
        if r.status_code == 401:
            raise UnauthorizedException(str(r.json()))
        else:
            raise Exception(f'An error occured while POST {url} : status code {r.status_code}, message {r.json()}')
    TOKEN = r.json()['access_token']
    return TOKEN
