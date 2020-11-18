import datetime as dt
import logging
from typing import List

import requests
from requests.auth import AuthBase

from tcommon.config import app_config

logger = logging.getLogger(__name__)


def memoize_token(func):
    cached_token = None

    def inner(self, *args, **kwargs):
        nonlocal cached_token
        if self.expire_time is not None:
            remaining = self.expire_time - dt.datetime.utcnow()
            print(f'Remaining : {remaining}')
        if cached_token is None or (self.expire_time is not None and remaining.seconds < 10):
            print('No token cached')
            cached_token = func(self, *args, **kwargs)
        return cached_token

    return inner


class TokenAuth(AuthBase):
    def __init__(self, username: str, password: str, scopes: List[str]):
        self.username = username
        self.password = password
        self.scopes = ' '.join(scopes)
        self.expire_time = None

    def __call__(self, r):
        r.headers['Authorization'] = f"Authorization {self._get_token()}"
        return r

    @memoize_token
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
        self.expire_time = dt.datetime.utcnow() + dt.timedelta(minutes=expire_in)
        return token
