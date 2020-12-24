from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserInfoCreate(BaseModel):
    id: UUID
    cellphone: Optional[str]
    country_code: Optional[str]
    email: str
