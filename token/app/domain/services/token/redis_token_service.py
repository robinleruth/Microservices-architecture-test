import pickle
from dataclasses import dataclass
from dataclasses import field
from typing import Set

import redis

from app.domain.model.credentials import Credentials
from app.domain.model.user import User
from app.domain.services.token.token_service import TokenService
from app.infrastructure.config import app_config


@dataclass
class RedisTokenService(TokenService):
    keys: Set[str] = field(default_factory=set)
    user_info_by_token: redis.Redis = None

    PREFIX = 'TOKEN:'

    def __post_init__(self):
        super().__post_init__()
        self.user_info_by_token = redis.Redis(host=app_config.REDIS_HOST, port=app_config.REDIS_PORT)

    def _get_from_connector(self, name, credentials: Credentials):
        return pickle.dumps(self.connector.get_by_name(name, credentials))

    def _get_from_dict(self, key):
        if key not in self.keys:
            self.keys.add(key)
        return pickle.loads(self.user_info_by_token[key])

    def _refresh_cache(self):
        for token in self.keys:
            if self._is_token_expired(token.split(self.PREFIX)[1]):
                self.keys.remove(token)
                self.user_info_by_token.delete(token)

    def _add_to_dict(self, key, user: User):
        self.keys.add(self.PREFIX + key)
        self.user_info_by_token[self.PREFIX + key] = pickle.dumps(user)
