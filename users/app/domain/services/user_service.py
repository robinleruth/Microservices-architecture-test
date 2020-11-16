from typing import List

from app.domain.services.user_not_found_exception import UserNotFoundException
from app.infrastructure.db.db_session import transaction_context
from app.infrastructure.db.user import User


def get_all_users() -> List[User]:
    with transaction_context() as session:
        lst = session.query(User).all()
    return lst


def get_user_by_name(name: str) -> User:
    with transaction_context() as session:
        user = session.query(User).filter_by(nickname=name).first()
    if user is None:
        raise UserNotFoundException(f'User not found : {name}')
    return user
