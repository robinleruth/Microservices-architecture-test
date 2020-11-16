import pickle
from dataclasses import dataclass
from dataclasses import field
from typing import Set

import redis

from app.domain.model.credentials import Credentials
from app.domain.services.token.token_service import TokenService


@dataclass
class RedisTokenService(TokenService):
    keys: Set[str] = field(default_factory=set)
    user_info_by_token: redis.Redis = None

    PREFIX = 'MODEL:'

    def __post_init__(self):
        super().__post_init__()
        self.user_info_by_token = redis.Redis()

    def _get_from_connector(self, name, credentials: Credentials):
        return pickle.dumps(self.connector.get_by_name(name, credentials))

    def _get_from_dict(self, key):
        if key not in self.keys:
            self.keys.add(key)
        return pickle.loads(self.user_info_by_token[key])

    def _refresh_cache(self):
        # TODO: upgdate key when ttl < 0
        for d in self.keys:
            pass
            # self.user_info_by_token[d] = self._get_from_connector(d)
