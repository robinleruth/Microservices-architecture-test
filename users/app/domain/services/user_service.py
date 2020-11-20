from typing import List

from app.domain.model.user import User
from app.domain.services.user_not_found_exception import UserNotFoundException
from app.infrastructure.db.db_session import transaction_context
from app.infrastructure.db.db_user import DbUser
from app.infrastructure.log import logger


def get_all_users() -> List[User]:
    with transaction_context() as session:
        users_from_db: List[DbUser] = session.query(DbUser).all()
        users = list(map(lambda x: User(**x.serialize), users_from_db))
    return users


def get_user_by_name(name: str) -> DbUser:
    with transaction_context() as session:
        user: DbUser = session.query(DbUser).filter_by(nickname=name).first()
        if user is None:
            raise UserNotFoundException(f'User not found : {name}')
    return user


def create_user(name: str, pwd: str, scopes: List[str] = None) -> User:
    logger.info(f'Creating user {name}')
    user = DbUser(nickname=name, password=pwd, scopes=' '.join(scopes) if scopes else '')
    with transaction_context() as session:
        session.add(user)
        session.commit()
        ret = User(**user.serialize)
    return ret


def update_scope(name: str, scopes: List[str]) -> User:
    logger.info(f'Updating scope of user {name} with {scopes}')
    with transaction_context() as session:
        user = session.query(DbUser).filter_by(nickname=name).first()
        if user is None:
            raise Exception(f'No user named {name}')
        user.scopes = ' '.join(scopes)
        session.commit()
        ret = User(**user.serialize)
    return ret

