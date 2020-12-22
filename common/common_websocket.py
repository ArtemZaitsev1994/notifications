import json
from uuid import UUID
from typing import List
from html import escape, unescape
import aioredis

from fastapi import (
    Depends, Body,
    WebSocket, APIRouter,
    WebSocketDisconnect,
    Request
)
from fastapi.responses import HTMLResponse
from common.manager import ConnectionManager
from sqlalchemy.orm import Session

from settings import REDIS_PORT, REDIS_HOST
from core.utils import get_db

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>LOAD</button>
        </form>

        <form action="" onsubmit="send(event)">
            <button>SEND</button>
        </form>


        <form action="" onsubmit="getPrev(event)">
            <button>Last One</button>
        </form>
        <ul id='messages'>


        <form action="" onsubmit="readMess(event)">
            <button>Read</button>
        </form>


        <form action="" onsubmit="banUser(event)">
            <button>Ban User</button>
        </form>


        <form action="" onsubmit="sendFile(event)">
        <input id="files" name="files" type="file" multiple>
        <button>files send FORM ENDPOINT</button>
        </form>

        <script>
            current_page = 1
            page_size = 10
            var message =  {
                'type': 'message',
                'message': '',
                'files': []
            }
            chat_id = '342e1a32-2321-472e-b835-6c7a633b1fa1'
            var ws = new WebSocket("ws://0.0.0.0:8002/notifications/%s");
            ws.onopen = function(event) {
                // ws.send(JSON.stringify(data))
                prev_mess =  {
                    'page': current_page,
                    'size': page_size,
                    'type': 'previous'
                }
                 ws.send(JSON.stringify(prev_mess))
            }
            ws.onmessage = function(event) {
                data = JSON.parse(event.data)
                console.log(data)
                data = data.payload
                if (data['type'] == 'message') {
                    mess = data.message
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(`${mess.sender.firstname} ${mess.created_at}: ${mess.text}`)
                    message.appendChild(content)
                    messages.appendChild(message)
                } else if (data['type'] == 'previous') {
                    for (mess of data.messages) {
                        var messages = document.getElementById('messages')
                        var message = document.createElement('li')
                        text = `${mess.sender.firstname} ${mess.created_at}: ${mess.text}`
                        message.textContent = text
                        messages.appendChild(message)
                    } 
                    current_page += 1   
                } else if (data['type'] == 'disconnect') {
                } else if (data['type'] == 'connect') {
                }
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                message =  {
                    'type': 'message',
                    'message': input.value,
                    'files': []
                }

                var files = document.getElementById('files').files
                  for (file of files) {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.fileName = file.name;
                    reader.onload = (event) => {
                      const fileName = event.target.fileName.split('.');
                      const content = event.currentTarget.result;
                      send_data = {
                        'ext': fileName[fileName.length - 1],
                        'file': content
                      }
                      console.log(message)
                      message.files.push(send_data);
                    };
                }
                input.value = ''
                event.preventDefault()
            };
            function send(event) {
                event.preventDefault()
                console.log(message)
                ws.send(JSON.stringify(message))
            };
            function getPrev(event) {
                var input = document.getElementById("messageText")
                prev_mess =  {
                    'page': current_page,
                    'size': page_size,
                    'type': 'previous'
                }
                ws.send(JSON.stringify(prev_mess))
                event.preventDefault()
            };
            function readMess(event) {
                prev_mess =  {
                    'message_id': 2,
                    'type': 'read'
                }
                ws.send(JSON.stringify(prev_mess))
                event.preventDefault()
            };
            function banUser(event) {
                prev_mess =  {
                    'type': 'access_denied'
                }
                ws.send(JSON.stringify(prev_mess))
                event.preventDefault()
            };
            function sendFile(event) {
                event.preventDefault()
              var files = document.getElementById('files').files
              for (file of files) {
                const reader = new FileReader();
                reader.readAsBinaryString(file);
                reader.fileName = file.name;
                reader.onload = (event) => {
                console.log(event)
                  const fileName = event.target.fileName.split('.');
                  const content = event.currentTarget.result;
                  send_data = {
                    'ext': fileName[fileName.length - 1],
                    'file': content
                  }
                  console.log(send_data)
                  ws.send(JSON.stringify(send_data));
                };
              }
            }


        </script>
    </body>
</html>
"""

success_response = {
    'status': 200,
    'error': None
}
error_response = {
    'status': 500,
    'payload': None
}


@router.get("/not/{self_id}")
async def get(self_id):
    return HTMLResponse(html % (self_id))


websocket_manager = ConnectionManager()


@router.websocket("/notifications/{current_user}")
async def websocket_endpoint(
        current_user: str,
        websocket: WebSocket,
        db: Session = Depends(get_db)
):
    # Проверяем токен пришедший от соединения
    if not await websocket_manager.check_auth(websocket):
        return await websocket_manager.auth_failed_error(websocket)

    # TODO
    # init_data = await websocket.receive_json()

    # Запрашиваем данные о пользователях с сервера аутентификации
    # users = await get_list_users_info({'users_uuid': [str(x.user) for x in chat_room.users]})
    # if len(users) != 2:
    #     return await websocket_manager.wrong_users_id_error(websocket)

    await websocket.accept()
    await websocket_manager.add_connection(current_user, websocket)
    redis = await aioredis.create_redis(f"redis://{REDIS_HOST}:{REDIS_PORT}")

    channel, *_ = await redis.psubscribe(current_user)

    # Messages processing
    try:
        while await channel.wait_message():
            _, msg = await channel.get(encoding='utf-8')
            msg = json.loads(msg)
            print(msg)

            response = {
                'payload': {
                    'type': msg,
                    'messages': msg
                }
            }
            response.update(success_response)
            await websocket_manager.send_personal_message(websocket, response)

    except WebSocketDisconnect:
        websocket_manager.disconnect(chat_room.id, websocket)
        response = {
            'payload': {
                'type': 'disconnect',
                'message': f'User left {users[current_user]["firstname"]}'
            }
        }
        response.update(success_response)
        await websocket_manager.broadcast(chat_room.id, response)
