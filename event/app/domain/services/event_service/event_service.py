import json
from dataclasses import dataclass
from typing import Dict, Any

import aioredis

from app.domain.model.event import EventIn, Event
from app.domain.services.event_store.event_store import EventStore
from app.infrastructure.config import app_config
from app.infrastructure.log import logger


@dataclass
class EventService:
    store: EventStore
    redis: aioredis.Redis = None

    def __post_init__(self):
        logger.info('Init Event Service')

    async def init_redis(self):
        if self.redis is None:
            logger.info('Init redis connection in Event Service')
            url = f'redis://{app_config.REDIS_HOST}:{app_config.REDIS_PORT}'
            self.redis = await aioredis.create_redis_pool(url)

    async def process_event(self, event: EventIn) -> Event:
        logger.info(f'Processing event {event}')
        event_out: Event = await self.save_in_event_store(event)
        await self.send_event(event.channel_name, event.event_data)
        await self.publish_notification(event.channel_name)
        return event_out

    async def publish_notification(self, channel_name: str):
        chan = channel_name + app_config.EVENT_NOTIFICATION_SUFFIXE
        logger.info(f'Publishing notification to subscribers on {chan}')
        return await self.redis.publish(chan, 'Notification')

    async def send_event(self, channel_name: str, event_data: Dict[str, Any]):
        chan = channel_name + app_config.PUBLISHED_LIST_SUFFIXED
        logger.info(f'Sending event on channel {chan}. Event : {event_data}')
        return await self.redis.lpush(chan, json.dumps(event_data))

    async def save_in_event_store(self, event: EventIn) -> Event:
        return await self.store.save(event)

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()
