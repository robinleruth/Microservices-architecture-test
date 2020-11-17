import logging

import requests
from requests import Session

from tcommon.get_token import TOKEN, get_token

logger = logging.getLogger(__name__)

s = Session()
s.headers.update({"Authorization": f"Bearer {TOKEN}"})


def get(url, **kwargs):
    r = s.get(url, **kwargs)
    if r.status_code == 401:
        logger.info("")
        s.headers.update({"Authorization": f"Bearer {get_token()}"})
        r = s.get(url, **kwargs)
    return r


def post(url, data=None, json=None, **kwargs):
    try:
        r = requests.post(url, data, json, **kwargs)
    except:
        r = requests.post(url, data, json, **kwargs)
    return r
