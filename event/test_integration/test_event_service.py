import os

os.environ['APP_ENV'] = 'test'
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
        event_service.close()

    async def test_send_event(self):
        event_store = MagicMock()
        event_service = EventService(event_store)
        await event_service.init_redis()
        result = await event_service.send_event('test', {'ok': 'ok', 'a': {'b': 'c'}})
        print(result)
        event_service.close()
