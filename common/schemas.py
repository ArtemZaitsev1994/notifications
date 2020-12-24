from typing import Union, Optional

from pydantic import BaseModel


class Error(BaseModel):
    code: str
    message: str


class CommonResponse(BaseModel):
    status: int
    payload: Union[dict, list, None]
    error: Optional[Error]
