from uuid import UUID

from pydantic import BaseModel


class OrderCreate(BaseModel):
    order: UUID
    from_user: UUID
    to_user: UUID
