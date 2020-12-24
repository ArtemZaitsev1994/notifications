from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from common.models import NotificationBase
from core.db import Base


class PremisesNotification(Base, NotificationBase):
    __tablename__ = 'premises_notifications'

    premises = Column(UUID(as_uuid=True))

    def formate_notification_text(self, event_text):
        return event_text
