import os

os.environ['APP_ENV'] = 'test'
import datetime as dt
from app.domain.model.event import Event
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from app.domain.services.event_service.event_service import EventService


class TestEventService(IsolatedAsyncioTestCase):
    async def test_publish_notif(self):
        event_store = MagicMock()
        event_service = EventService(event_store)
        await event_service.init_redis()
        result = await event_service.publish_notification('test')
        print(result)
        await event_service.close()

    async def test_send_event(self):
        event_store = MagicMock()
        event_service = EventService(event_store)
        await event_service.init_redis()
        event = Event(aggregate_type='Order',
                      aggregate_id='123',
                      event_id='484ca82951914f05857dd4908c3fcdbe',
                      event_type='OrderCreated',
                      event_data={'a': 'b', 'c': {'a': 'b'}},
                      created_at=dt.datetime(2020, 11, 20, 9, 15, 39, 411263))
        result = await event_service.send_event('test', event)
        print(result)
        await event_service.close()
