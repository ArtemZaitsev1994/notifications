import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cellphone = Column(String())
    country_code = Column(String())
    available_sms_notification = Column(Boolean(), default=True)
    email = Column(String())
    available_email_notification = Column(Boolean(), default=True)
