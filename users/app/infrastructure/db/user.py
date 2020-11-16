from sqlalchemy import Column, func, String, Boolean
from sqlalchemy import Integer

from app.domain.services import password_service
from app.infrastructure.db import Base


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    created_at = Column(Integer, default=func.now())
    updated_at = Column(Integer, default=func.now(), onupdate=func.now())
    last_seen_at = Column(Integer, default=func.now())
    nickname = Column(String(32), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    online = Column(Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = password_service.generate_password_hash(password)

    def ping(self):
        self.last_seen_at = func.now()
        self.online = True