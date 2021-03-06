from uuid import UUID

from pydantic import BaseModel


class PremisesCreate(BaseModel):
    premises: UUID
    from_user: UUID
    to_user: UUID
