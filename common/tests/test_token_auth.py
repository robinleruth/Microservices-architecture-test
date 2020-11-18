import os

os.environ['APP_ENV'] = 'test'
import unittest
from unittest.mock import patch, MagicMock

from requests import Session

from tcommon.auth_request.token_auth import TokenAuth


class TestTokenAuth(unittest.TestCase):
    def test_token_auth(self):
        s = Session()
        s.auth = TokenAuth(username='Robin', password='test', scopes=['me'])
        with patch('requests.post') as mock_request:
            ret = MagicMock()
            ret.json = lambda: {'access_token': '123', 'expire_in': 1}
            mock_request.return_value = ret
            r = s.get('http://localhost:8082/api/v1/token_controller/tokenInfo')
            print(r)
