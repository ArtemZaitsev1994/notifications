import datetime
from typing import Union, Optional, List

from pydantic import BaseModel


class Error(BaseModel):
    code: str
    message: str


class CommonResponse(BaseModel):
    status: int
    payload: Union[dict, list, None]
    error: Optional[Error]


class Notifications(BaseModel):
    text: str
    created_at: datetime.datetime


class NotificationsList(CommonResponse):
    class Payload(BaseModel):
        notifications: List[Notifications]

    payload: Payload


class ReadNotification(BaseModel):
    notification: str
