from typing import List, Optional, Union, Dict
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class PremisesCreate(BaseModel):
    premises: UUID
    from_user: UUID
    to_user: UUID
