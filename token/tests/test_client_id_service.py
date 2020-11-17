import os


os.environ['APP_ENV'] = 'test'
os.environ['SECRET_KEY'] = 'secret'
import unittest
from app.infrastructure.db import engine, Base, DbClientId
from app.infrastructure.db.db_session import transaction_context
from app.domain.services.client_id import client_id_service


class TestClientIdService(unittest.TestCase):
    def setUp(self) -> None:
        Base.metadata.create_all(bind=engine)
        self.password = 'test'
        user = DbClientId(client_id='aaa')
        with transaction_context() as session:
            session.add(user)

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=engine)

    def test_is_present(self):
        is_present = client_id_service.client_id_present_in_db('aaa')
        self.assertTrue(is_present)

    def test_is_not_present(self):
        is_present = client_id_service.client_id_present_in_db('bbb')
        self.assertFalse(is_present)

    def test_get_all(self):
        lst = client_id_service.get_all()
        self.assertEqual(1, len(lst))
        self.assertEqual('aaa', lst[0])

    def test_add_one(self):
        client_id_service.add_one('bbb')
        lst = client_id_service.get_all()
        self.assertEqual(2, len(lst))


if __name__ == '__main__':
    unittest.main(verbosity=2)
