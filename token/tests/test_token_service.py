import os

os.environ['APP_ENV'] = 'test'
os.environ['SECRET_KEY'] = 'secret'
import unittest
from unittest.mock import MagicMock

from app.domain.model.credentials import Credentials
from app.domain.model.user import User
from app.domain.services.token.token_service import TokenService


class TestTokenService(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
