import uuid
import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, desc, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSON


from core.db import Base


class NotificationBase:

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    to_user = Column(UUID(as_uuid=True))
    from_user = Column(UUID(as_uuid=True))
    received = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    event_id = Column(Integer)


class Events(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text())