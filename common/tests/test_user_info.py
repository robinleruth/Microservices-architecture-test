import os

os.environ['APP_ENV'] = 'test'
import unittest
from unittest.mock import MagicMock

from tcommon.authenticate_token import get_user_info_by_token, UnauthorizedException


class TestUserInfo(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_user_info_fail(self):
        response = MagicMock()
        response.status_code = 401
        response.json = lambda: {'detail': 'Could not validate credentials'}
        import requests
        requests.get = MagicMock(return_value=response)
        self.assertRaises(UnauthorizedException, get_user_info_by_token, 'aa')

    def test_user_info_success(self):
        response = MagicMock()
        response.status_code = 200
        response.json = lambda: {
            'nickname': 'Robin'
        }
        import requests
        requests.get = MagicMock(return_value=response)
        user = get_user_info_by_token('aa')
        self.assertEqual('Robin', user.nickname)
