import abc
import json
from dataclasses import dataclass, InitVar, field
from threading import Thread

import aioredis
import asyncio
from aioredis import Channel

from tcommon.config import app_config, TestConfig
from tcommon.event_subscriber.model import EventDto
from tcommon.log import logger


@dataclass
class EventSubscriber(metaclass=abc.ABCMeta):
    channel_name: str
    redis_host: InitVar[str] = field(default='localhost')
    redis_port: InitVar[int] = field(default=6379)

    def __post_init__(self, redis_host: str, redis_port: int):
        def run():
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.read_redis_message(redis_host, redis_port))

        if app_config is not TestConfig:
            logger.info(f'Launch thread for Event Subscriber for Channel {self.channel_name}')
            t = Thread(target=run)
            t.daemon = True
            t.start()

    async def read_redis_message(self, redis_host: str, redis_port: int):
        logger.info(f'Init event subscriber redis connection. Channel name {self.channel_name}')
        suffixe = self.__class__.__name__
        subscriber_list = self.channel_name + ':SubscriberList'
        event_notif_channel = self.channel_name + ':EventNotification'
        published_list_name = self.channel_name + ':PublishedList:' + suffixe
        processing_list_name = self.channel_name + ':ProcessingList:' + suffixe
        not_able_to_process_list_name = self.channel_name + ':NotAbleToProcessList:' + suffixe
        logger.info(f'Listens to {event_notif_channel}')
        redis_uri = f'redis://{redis_host}:{redis_port}'
        redis_conn = await aioredis.create_redis(redis_uri)
        subscriber_conn = await aioredis.create_redis(redis_uri)
        channel: Channel = await subscriber_conn.subscribe(event_notif_channel)
        # Put itself in Subscriber set
        logger.info(f'Register in subscriber list {subscriber_list} as {suffixe}')
        redis_conn.sadd(subscriber_list, suffixe)
        # Register to ChannelName:EventNotification
        while await channel[0].wait_message():
            # Check if data in Published list, if so process them
            logger.info('Notification received')
            msg = await channel[0].get()
            logger.info(f'Notif : {msg}')
            # Try to RPOPLPUSH from ChannelName:PublishedList to ChannelNameProcessingList
            try:
                logger.info(f'RPOPLPUSH from {published_list_name} to {processing_list_name}')
                event_data = await redis_conn.rpoplpush(published_list_name, processing_list_name)
                event_data = json.loads(event_data)
                event = EventDto(**event_data)
                logger.info(f'Got event data {event}')
            except Exception as e:
                # If it fails, it means another instance of the service has taken it already
                logger.warning(
                    f"RPOPLPUSH from {published_list_name} to {processing_list_name} didn't work. It must have been taken already -> Exception : {e}")
                continue
            try:
                await self.process_event(event)
            except Exception as e:
                logger.error(f'ERROR while processing data -> {e}.')
                logger.info(f'Task not processed and put in {not_able_to_process_list_name}')
                # TODO: find a way to process the not able to process list
                await redis_conn.lpush(not_able_to_process_list_name, event_data)
            # Once completed, remove entry from Processing list
            await redis_conn.rpop(processing_list_name)
            logger.info('Processing done, awaiting new message.')
            if app_config is TestConfig:
                break

    @abc.abstractmethod
    async def process_event(self, event: EventDto):
        pass
