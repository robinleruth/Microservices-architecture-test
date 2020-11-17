from sqlalchemy import Column, func, String, DateTime
from sqlalchemy import Integer

from app.infrastructure.db import Base


class DbClientId(Base):
    __tablename__ = 't_client_id'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_seen_at = Column(DateTime, default=func.now())
    client_id = Column(String, nullable=False, unique=True)

    @property
    def serialize(self):
        return {}
