import os

os.environ['APP_ENV'] = 'test'
import aioredis
import datetime as dt
from dataclasses import asdict
import asyncio
import json
from unittest import IsolatedAsyncioTestCase
from tcommon.event_subscriber.model import EventDto
from tcommon.event_subscriber.util import DateTimeEncoder

from tcommon.event_subscriber.event_subscriber import EventSubscriber


class TestEventSubscriberIntegration(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        class Implem(EventSubscriber):
            async def process_event(self, event_data):
                print(f'In process_event : {event_data} received')
                return event_data

        self.event_sub = Implem('TestChannel')

    async def test_read(self):
        subscriber_list = 'TestChannel' + ':SubscriberList'
        event_notif_channel = 'TestChannel' + ':EventNotification'
        published_list_name = 'TestChannel' + ':PublishedList'
        processing_list_name = 'TestChannel' + ':ProcessingList'
        not_able_to_process_list_name = 'TestChannel' + ':NotAbleToProcessList'
        redis_uri = 'redis://localhost:6379'
        redis_conn = await aioredis.create_redis(redis_uri)
        event_data = {
            'test': 'ok',
            'test2': {
                'a': 'b',
                'c': 'b'
            }
        }
        event = EventDto(aggregate_type='Order',
                         aggregate_id='123',
                         event_id='484ca82951914f05857dd4908c3fcdbe',
                         event_type='OrderCreated',
                         event_data=event_data,
                         created_at=dt.datetime(2020, 11, 20, 9, 15, 39, 411263))

        async def wait_and_publish():
            await asyncio.sleep(1)
            # For each sub in set
            sub_set = await redis_conn.smembers(subscriber_list, encoding='utf-8')
            for sub in sub_set:
                published_list = f'{published_list_name}:{sub}'
                print(f'publishing in {published_list} : {event}')
                await redis_conn.lpush(published_list, json.dumps(asdict(event), cls=DateTimeEncoder))
            print(f'Publishing event notif in {event_notif_channel}')
            await redis_conn.publish(event_notif_channel, 'Message !')

        asyncio.ensure_future(wait_and_publish())
        await self.event_sub.read_redis_message('localhost', 6379)
        redis_conn.close()
