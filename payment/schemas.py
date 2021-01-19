from uuid import UUID

from pydantic import BaseModel


class PaymentNotificationSerializer(BaseModel):
    order: UUID
    to_user: UUID
    stripe_id: str
