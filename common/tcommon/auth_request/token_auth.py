import datetime as dt
from functools import wraps
from typing import List

import requests
from requests.auth import AuthBase

from tcommon.config import app_config
from tcommon.log import logger


def memoize_token(func):
    cached_tokens = {}

    @wraps(func)
    def inner(self, *args, **kwargs):
        nonlocal cached_tokens
        if self.expire_time is not None:
            remaining = self.expire_time - dt.datetime.utcnow()
            print(f'Remaining validity time for token for user {self.username} : {remaining}')
            logger.info(f'Remaining validity time for token for user {self.username} : {remaining}')
        if self not in cached_tokens or (self.expire_time is not None and remaining.seconds < 10):
            print(f'No token cached for {self.username}')
            logger.info(f'No token cached for {self.username}')
            cached_tokens[self] = func(self, *args, **kwargs)
        return cached_tokens[self]

    return inner


class TokenAuth(AuthBase):
    def __init__(self, username: str, password: str, scopes: List[str]):
        self.username = username
        self.password = password
        self.scopes = ' '.join(scopes)
        self.expire_time = None

    def __eq__(self, o: object) -> bool:
        return self.__class__ == o.__class__ and self.username == o.username

    def __hash__(self):
        return hash(self.username)

    def __call__(self, r):
        r.headers['Authorization'] = f"Bearer {self._get_token()}"
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
        if r.status_code == 401:
            raise Exception(f'Unauthorized : {r.json()}')
        if r.status_code == 403:
            raise Exception(f'Forbidden : {r.json()}')
        token = r.json()['access_token']
        expire_in = r.json()['expire_in']
        self.expire_time = dt.datetime.utcnow() + dt.timedelta(minutes=expire_in)
        return token
