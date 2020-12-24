from pydantic import BaseModel


class RabbitMessage(BaseModel):
    section: str
    action: str
    data: dict
    need_response_to_websocket: bool
