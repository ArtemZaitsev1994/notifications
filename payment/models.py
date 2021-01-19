from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from common.models import NotificationBase
from core.db import Base


class PaymentNotification(Base, NotificationBase):
    __tablename__ = 'payment_notifications'

    order = Column(UUID(as_uuid=True))
    stripe_id = Column(String(100))

    def formate_notification_text(self, event_text):
        return event_text
