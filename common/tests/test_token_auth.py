import os

os.environ['APP_ENV'] = 'test'
import unittest
from unittest.mock import patch, MagicMock

from requests import Session

from tcommon.auth_request.token_auth import TokenAuth


class TestTokenAuth(unittest.TestCase):
    def test_token_auth(self):
        with patch.object(Session, 'send', return_value='ok') as mock_method:
            s = Session()
            s.auth = TokenAuth(username='Robin', password='test', scopes=['me'])
            with patch('requests.post') as mock_request:
                ret = MagicMock()
                ret.json = lambda: {'access_token': '123', 'expire_in': 3}
                mock_request.return_value = ret
                r = s.get('http://localhost:8082/api/v1/token_controller/tokenInfo')
                print(r)
                r = s.get('http://localhost:8082/api/v1/token_controller/tokenInfo')
                print(r)
        mock_request.assert_called_once()
        with patch('requests.post') as mock_request:
            ret = MagicMock()
            ret.json = lambda: {'access_token': '456', 'expire_in': 3}
            mock_request.return_value = ret
            another_auth = TokenAuth(username='Robinn', password='test', scopes=['me'])
            token = another_auth._get_token()
            self.assertNotEqual('123', token)
