import datetime as dt
import json
import uuid
from dataclasses import dataclass

import aioredis

from app.domain.model.aggregate import Aggregate
from app.domain.model.event import EventIn, Event
from app.domain.services.util import DateTimeEncoder
from app.infrastructure.config import app_config
from app.infrastructure.log import logger


@dataclass
class EventStore:
    redis: aioredis.Redis = None

    async def init_redis(self):
        if self.redis is None:
            logger.info('Init redis connection in Event Store')
            url = f'redis://{app_config.REDIS_HOST}:{app_config.REDIS_PORT}'
            self.redis = await aioredis.create_redis_pool(url)

    def __post_init__(self):
        logger.info('Init EventStore')

    @staticmethod
    def _generate_uuid():
        return uuid.uuid4().hex

    async def save(self, event: EventIn) -> Event:
        logger.info(f'Saving event in event store : {event}')
        ret = Event(
            created_at=dt.datetime.utcnow(),
            event_id=self._generate_uuid(),
            aggregate_id=event.aggregate_id if event.aggregate_id else self._generate_uuid(),
            aggregate_type=event.aggregate_type,
            event_type=event.event_type,
            event_data=event.event_data
        )
        logger.info('Saving it with hset')
        # Add event in a hash
        await self.redis.hset(ret.event_id, 'json', json.dumps(ret.dict(), cls=DateTimeEncoder))
        logger.info('Adding it to aggregate list')
        # Add event commit ID to the event store of the aggregate
        await self.redis.rpush(ret.aggregate_id, ret.event_id)
        return ret

    async def get_aggregate(self, aggregate_id: str) -> Aggregate:
        events = []
        nb_events = await self.redis.llen(aggregate_id)
        events_hash = await self.redis.lrange(aggregate_id, 0, nb_events - 1)
        for hash in events_hash:
            event = await self.redis.hget(hash, 'json')
            event = json.loads(event)
            events.append(event)
        return Aggregate(
            events=events,
            aggregate_id=events[0]['aggregate_id'] if len(events) else '',
            aggregate_type=events[0]['aggregate_type'] if len(events) else ''
        )

    async def close(self):
        logger.info('Closing redis Connection for Event Store')
        self.redis.close()
        await self.redis.wait_closed()
