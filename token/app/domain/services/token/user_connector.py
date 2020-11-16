from abc import ABCMeta, abstractmethod

from app.domain.model.credentials import Credentials
from app.domain.model.user import User


class UserConnector(metaclass=ABCMeta):
    @abstractmethod
    def get_by_name(self, name: str, credentials: Credentials) -> User:
        pass
