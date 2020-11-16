from app.domain.model.credentials import Credentials
from app.domain.model.user import User
from app.domain.services.token.user_connector import UserConnector


class ApiUserConnector(UserConnector):
    def get_by_name(self, name: str, credentials: Credentials) -> User:
        pass
