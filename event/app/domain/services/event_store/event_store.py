import uuid
from dataclasses import dataclass

from app.infrastructure.log import logger


@dataclass
class EventStore:
    def __post_init__(self):
        logger.info('Init EventStore')

    @staticmethod
    def _generate_uuid():
        return uuid.uuid4().hex
