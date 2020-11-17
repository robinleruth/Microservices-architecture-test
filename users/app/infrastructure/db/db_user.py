from sqlalchemy import Column, func, String, Boolean, DateTime
from sqlalchemy import Integer

from app.domain.services import password_service
from app.infrastructure.db import Base


class DbUser(Base):
    __tablename__ = 't_users'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_seen_at = Column(DateTime, default=func.now())
    nickname = Column(String(32), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    online = Column(Boolean, default=False)
    scopes = Column(String)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = password_service.generate_password_hash(password)

    def ping(self):
        self.last_seen_at = func.now()
        self.online = True

    @property
    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_seen_at': self.last_seen_at,
            'nickname': self.nickname,
            'online': self.online,
            'scopes': self.scopes
        }
