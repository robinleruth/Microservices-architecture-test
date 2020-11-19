import os

os.environ['APP_ENV'] = 'test'
import aioredis
import asyncio
import pickle
from unittest import IsolatedAsyncioTestCase

from tcommon.event_subscriber.event_subscriber import EventSubscriber


class TestEventSubscriberIntegration(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        class Implem(EventSubscriber):
            async def process_event(self, event_data):
                print(event_data, ' received')
                return event_data

        self.event_sub = Implem('TestChannel')

    async def test_read(self):
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

        async def wait_and_publish():
            await asyncio.sleep(1)
            print(f'publishing in {published_list_name} : {event_data}')
            await redis_conn.lpush(published_list_name, pickle.dumps(event_data))
            print(f'Publishing event notif in {event_notif_channel}')
            await redis_conn.publish(event_notif_channel, 'Message !')

        asyncio.ensure_future(wait_and_publish())
        await self.event_sub.read_redis_message('localhost', 6379)
        redis_conn.close()
