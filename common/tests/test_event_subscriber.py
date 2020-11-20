import os

os.environ['APP_ENV'] = 'test'
from unittest import IsolatedAsyncioTestCase

from tcommon.event_subscriber.event_subscriber import EventSubscriber


class TestEventSubsriber(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        class Implem(EventSubscriber):
            async def process_event(self, event_data):
                print(event_data, ' received')
                return event_data

        self.event_sub = Implem('TestChannel')

    def tearDown(self) -> None:
        pass

    async def test_process_event(self):
        result = await self.event_sub.process_event('event data')
        self.assertEqual('event data', result)
