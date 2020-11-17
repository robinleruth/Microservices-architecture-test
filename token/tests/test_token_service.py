import os

os.environ['APP_ENV'] = 'test'
os.environ['SECRET_KEY'] = 'secret'
import time
import unittest
from unittest.mock import MagicMock
from datetime import timedelta

from app.domain.model.credentials import Credentials
from app.domain.model.token_not_found import TokenNotFound
from app.domain.model.user import User
from app.domain.services.token.token_service import TokenService


class TestTokenService(unittest.TestCase):
    def test_service(self):
        connector = MagicMock()
        connector.get_by_name = MagicMock(return_value=User(nickname='Robin'))
        self.service = TokenService(connector)
        user = self.service.get_by_token('aaa', Credentials('a', 'b'))
        print(user)
        # self.service._refresh_cache()

    def test_redis_service(self):
        # connector = MagicMock()
        # connector.get_by_name = MagicMock(return_value=User(nickname='Robin'))
        # self.service = RedisTokenService(connector)
        # user = self.service.get_by_token('aaa', Credentials('a', 'b'))
        # print(user)
        # self.service._refresh_cache()
        pass

    def test_create_token(self):
        connector = MagicMock()
        connector.get_by_name = MagicMock(return_value=User(nickname='Robin'))
        self.service = TokenService(connector)
        token = self.service.create_access_token('Robin', Credentials('a', 'b'))
        user = self.service.get_by_token(token)
        self.assertEqual('Robin', user.nickname)

    def test_cache_refresh(self):
        connector = MagicMock()
        connector.get_by_name = MagicMock(return_value=User(nickname='Robin'))
        self.service = TokenService(connector)
        token = self.service.create_access_token('Robin', Credentials('a', 'b'), timedelta(seconds=2))
        user = self.service.get_by_token(token)
        self.assertEqual('Robin', user.nickname)
        time.sleep(1)
        self.service._refresh_cache()
        user = self.service.get_by_token(token)
        self.assertEqual('Robin', user.nickname)
        time.sleep(2)
        self.service._refresh_cache()
        self.assertRaises(TokenNotFound, self.service.get_by_token, token)

    def test_user_has_scope_fail(self):
        user = User(nickname='R', scopes_allowed=['a', 'b'])
        self.assertTrue(user.has_scopes(['a']))

    def test_user_has_scope_succeed(self):
        user = User(nickname='R', scopes_allowed=['a', 'b'])
        self.assertFalse(user.has_scopes(['a', 'c']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
