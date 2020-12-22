import json

from common.shemas import CommonResponse
from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def add_connection(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        del self.active_connections[user_id]

    async def send_personal_message(self, websocket: WebSocket, message: dict):
        await websocket.send_text(json.dumps(CommonResponse(**message).dict()))

    async def broadcast(self, useres: list, message: dict):
        for user in useres:
            await self.send_personal_message(self.active_connections[user], message)

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

    async def chat_limit_error(self, websocket: WebSocket):
        # response = {
        #     'status': 403,
        #     'payload': None,
        #     'error': {
        #         'code': 'LIMIT_EXCEEDED',
        #         'message': 'Limit of new chats per day exceeded'
        #     }
        # }
        # await self.send_personal_message(websocket, response)
        # websocket.close(code=403)
        await websocket.close(code=403)

    async def access_denied_error(self, websocket: WebSocket):
        await websocket.close(code=403)
