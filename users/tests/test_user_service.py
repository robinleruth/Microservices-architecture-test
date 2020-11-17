import os

os.environ['APP_ENV'] = 'test'
import unittest
from typing import List
from app.domain.services.user_not_found_exception import UserNotFoundException
from app.domain.model.user import User
from app.domain.services import user_service
from app.infrastructure.db import Base, engine
from app.infrastructure.db.db_user import DbUser
from app.infrastructure.db.db_session import transaction_context


class TestUserService(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.password = 'test'
        user = DbUser(nickname='Robin', password=self.password, scopes="a b c")
        with transaction_context() as session:
            session.add(user)

    def tearDown(self):
        Base.metadata.drop_all(bind=engine)

    def test_get_all(self):
        lst: List[User] = user_service.get_all_users()
        self.assertTrue(len(lst) == 1)
        print(lst[0])

    def test_pwd_hash(self):
        # user = user_service.get_user_by_name('Robin')
        # self.assertTrue(user is not None)
        # hash = user.password_hash
        # self.assertTrue(password_service.verify_password('test', hash))
        pass

    def test_create_user(self):
        user = user_service.create_user('Nom', 'test_pwd')
        self.assertTrue(user is not None)
        self.assertEqual('Nom', user.nickname)

    def test_user_is_none(self):
        self.assertRaises(UserNotFoundException, user_service.get_user_by_name, 'Test')


if __name__ == '__main__':
    unittest.main(verbosity=2)
