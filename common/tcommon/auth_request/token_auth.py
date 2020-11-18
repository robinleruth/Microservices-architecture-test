import logging
from typing import List

import requests
from requests.auth import AuthBase

from tcommon.config import app_config

logger = logging.getLogger(__name__)


class TokenAuth(AuthBase):
    def __init__(self, username: str, password: str, scopes: List[str]):
        self.username = username
        self.password = password
        self.scopes = ' '.join(scopes)

    def __call__(self, r):
        r.headers['Authorization'] = f"Authorization {self._get_token()}"
        return r

    def _get_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"
        }
        data = f"grant_type=&username={self.username}&password={self.password}&scope={self.scopes}&client_id=&client_secret="
        url = app_config.TOKEN_SERVICE_URL + app_config.TOKEN_CREATION
        logger.info(f'GET Token {url}')
        r = requests.post(url, headers=headers, data=data)
        token = r.json()['access_token']
        expire_in = r.json()['expire_in']
        return token
