from typing import List

from app.domain.model.user import User
from app.domain.services.user_not_found_exception import UserNotFoundException
from app.infrastructure.db.db_session import transaction_context
from app.infrastructure.db.db_user import DbUser


def get_all_users() -> List[User]:
    with transaction_context() as session:
        users_from_db: List[DbUser] = session.query(DbUser).all()
        users = list(map(lambda x: User(**x.serialize), users_from_db))
    return users


def get_user_by_name(name: str) -> User:
    with transaction_context() as session:
        user: DbUser = session.query(DbUser).filter_by(nickname=name).first()
        if user is None:
            raise UserNotFoundException(f'User not found : {name}')
        ret = User(**user.serialize)
    return ret


def create_user(name: str, pwd: str) -> User:
    user = DbUser(nickname=name, password=pwd)
    with transaction_context() as session:
        session.add(user)
        session.commit()
        ret = User(**user.serialize)
    return ret

