import os

os.environ['APP_ENV'] = 'test'
import unittest
from typing import List
from app.domain.services import user_service, password_service
from app.infrastructure.db import Base, engine
from app.infrastructure.db.user import User
from app.infrastructure.db.db_session import transaction_context


class TestUserService(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.password = 'test'
        user = User(nickname='Robin', password=self.password)
        with transaction_context() as session:
            session.add(user)

    def tearDown(self):
        Base.metadata.drop_all(bind=engine)

    def test_get_all(self):
        lst: List[User] = user_service.get_all_users()
        self.assertTrue(len(lst) == 1)

    def test_pwd_hash(self):
        user = user_service.get_user_by_name('Robin')
        self.assertTrue(user is not None)
        hash = user.password_hash
        self.assertTrue(password_service.verify_password('test', hash))


if __name__ == '__main__':
    unittest.main(verbosity=2)
