import json
from collections import defaultdict

from .schemas import CommonResponse
from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(list)

    async def add_connection(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)

    async def send_personal_message(self, user_id: str, message: dict):
        for websocket in self.active_connections[user_id]:
            await websocket.send_text(json.dumps(CommonResponse(**message).dict()))

    async def check_auth(self, websocket: WebSocket):
        return True

    async def auth_failed_error(self, websocket: WebSocket):
        await websocket.close(code=403)

    async def wrong_users_id_error(self, websocket: WebSocket):
        # response = {
        #     'status': 400,
        #     'payload': None,
        #     'error': {
        #         'code': 'NOT_FOUND',
        #         'message': 'Users are with uuid not found'
        #     }
        # }
        # await self.send_personal_message(websocket, response)
        # self.disconnect(room_id, websocket)
        await websocket.close(code=403)

    async def access_denied_error(self, websocket: WebSocket):
        await websocket.close(code=403)
