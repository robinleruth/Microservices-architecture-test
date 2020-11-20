import os

os.environ['APP_ENV'] = 'test'
from unittest import IsolatedAsyncioTestCase
from app.domain.model.event import EventIn
from app.domain.model.aggregate import Aggregate

from app.domain.services.event_store.event_store import EventStore


class TestEventStore(IsolatedAsyncioTestCase):
    async def test(self):
        event_store = EventStore()
        await event_store.init_redis()
        event = EventIn(
            aggregate_id='123',
            channel_name='test_event_store',
            aggregate_type='Order',
            event_type='OrderCreated',
            event_data={
                'a': 'b',
                'c': {
                    'a': 'b'
                }
            }
        )
        result = await event_store.save(event)
        print(result)
        result = await event_store.save(event)
        print(result)

        agg: Aggregate = await event_store.get_aggregate(result.aggregate_id)
        print(agg)
        print(len(agg.events))
        for i in agg.events:
            print(i)
        await event_store.close()
