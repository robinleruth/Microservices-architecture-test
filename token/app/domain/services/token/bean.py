from functools import lru_cache

import redis

from app.domain.services.token.redis_token_service import RedisTokenService
from app.domain.services.token.token_service import TokenService
from app.infrastructure.connector.api_user_connector import ApiUserConnector
from app.infrastructure.log import logger


@lru_cache()
def get_token_service() -> TokenService:
    connector = ApiUserConnector()
    r = redis.Redis()
    try:
        r.ping()
        logger.info('Redis connection available')
        service = RedisTokenService(connector)
    except:
        service = TokenService(connector)
    return service
