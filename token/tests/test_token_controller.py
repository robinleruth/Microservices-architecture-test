import os

os.environ['APP_ENV'] = 'test'
os.environ['SECRET_KEY'] = 'secret'
import unittest
from unittest.mock import MagicMock

from starlette.testclient import TestClient

from app.interface import api
from app.domain.services.token.token_service import TokenService
from app.domain.model.user import User
from app.domain.model.credentials import Credentials
from app.domain.services.token.bean import get_token_service


class TestTokenController(unittest.TestCase):
    def setUp(self):
        connector = MagicMock()
        connector.get_by_name = MagicMock(return_value=User(nickname='Robin', scopes_allowed=['me']))
        self.token_service = TokenService(connector)
        self.client = TestClient(api)

    def tearDown(self):
        pass

    def test_post(self):
        async def override_dependency():
            return self.token_service
        api.dependency_overrides[get_token_service] = override_dependency
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = self.client.post('/api/v1/token_controller/token', headers=headers,
                                    data="grant_type=&username=Robin&password=aaa&scope=&client_id=&client_secret=")
        self.assertEqual(201, response.status_code)

    def test_get(self):
        async def override_dependency():
            return self.token_service
        api.dependency_overrides[get_token_service] = override_dependency
        token = 'footokenbar'
        response = self.client.get('/api/v1/token_controller/tokenInfo',
                                   headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(403, response.status_code)
        token = self.token_service.create_access_token('Robin', Credentials('Robin', 'aaa'), scopes=['me'])
        response = self.client.get('/api/v1/token_controller/tokenInfo',
                                   headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(200, response.status_code)
        self.assertEqual('Robin', response.json()['nickname'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
