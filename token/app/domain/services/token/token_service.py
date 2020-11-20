import time
from dataclasses import dataclass
from dataclasses import field
from datetime import timedelta, datetime
from threading import Thread
from typing import Dict, Optional, List

from jose import jwt, ExpiredSignatureError

from app.domain.model.credentials import Credentials
from app.domain.model.scope_not_allowed import ScopeNotAllowedException
from app.domain.model.token_data import TokenData
from app.domain.model.token_not_found import TokenNotFound
from app.domain.model.user import User
from app.domain.model.user_not_found import UserNotFound
from app.domain.services.token.user_connector import UserConnector
from app.infrastructure.config import TestConfig
from app.infrastructure.config import app_config
from app.infrastructure.log import logger


@dataclass
class TokenService:
    connector: UserConnector
    user_info_by_token: Dict[str, User] = field(default_factory=dict)

    PREFIX = ''

    def __post_init__(self):
        logger.info('Init Token Service')
        if app_config is not TestConfig:
            logger.info('Launch clean dead token every minute')
            Thread(target=self.refresh).start()

    def get_by_token(self, name: str, credentials: Optional[Credentials] = None) -> User:
        key = name
        key = self.PREFIX + key
        if key not in self.user_info_by_token:
            if credentials is not None:
                user: User = self._get_from_connector(key, credentials)
                if user is None:
                    raise UserNotFound(f"User {key} couldn't be found")
                self.user_info_by_token[key] = user
            else:
                raise TokenNotFound(f'Token not found : {key}')
        return self._get_from_dict(key)

    def refresh(self):
        while True:
            self._refresh_cache()
            time.sleep(60)

    @staticmethod
    def _is_token_expired(token):
        try:
            jwt.decode(token, app_config.SECRET_KEY, algorithms=[app_config.ALGORITHM])
        except ExpiredSignatureError:
            return True
        return False

    def _refresh_cache(self):
        self.user_info_by_token = {
            k: v for k, v in self.user_info_by_token.items() if not self._is_token_expired(k)
        }

    def _get_from_connector(self, name: str, credentials: Credentials) -> User:
        return self.connector.get_by_name(name, credentials)

    def _get_from_dict(self, name) -> User:
        return self.user_info_by_token[name]

    def _add_to_dict(self, key, user: User):
        self.user_info_by_token[self.PREFIX + key] = user

    def create_access_token(self, username: str, credentials: Credentials, expires_delta: Optional[timedelta] = None,
                            scopes: List[str] = None):
        user = self.connector.get_by_name(username, credentials)
        if scopes and not user.has_scopes(scopes):
            raise ScopeNotAllowedException(
                f'User {user.nickname} is not allowed for scope {" ".join(user.scopes_not_allowed)}')
        to_encode = {"sub": user.nickname, "scopes": scopes if scopes else []}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, app_config.SECRET_KEY, algorithm=app_config.ALGORITHM)
        self._add_to_dict(encoded_jwt, user)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str):
        payload = jwt.decode(token, app_config.SECRET_KEY, algorithms=[app_config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise Exception('No subject found in token')
        scopes = payload.get('scopes', [])
        token_data = TokenData(username=username, scopes=scopes)
        return token_data
