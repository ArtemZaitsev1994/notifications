import json

from fastapi import (
    Depends, Body,
    WebSocket, APIRouter,
    WebSocketDisconnect,
    Request
)
from fastapi.responses import HTMLResponse
from aio_pika import connect, IncomingMessage, ExchangeType, RobustConnection

from common.manager import ConnectionManager
from settings import REDIS_HOST, REDIS_PORT, RABBIT_WEBSOCKETS_EXCHANGE
from sqlalchemy.orm import Session
from core.utils import check_auth, get_db, row2dict
from .events import create_events, get_event_by_id
from .schemas import NotificationsList
from .services import get_list_notifications


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


@router.get('/create_events')
def _events():
    create_events()


@router.get("/not/{self_id}")
async def get(self_id):
    return HTMLResponse(html % (self_id))


websocket_manager = ConnectionManager()


@router.websocket("/notifications/{current_user}")
async def websocket_endpoint(
        current_user: str,
        websocket: WebSocket,
        # db: Session = Depends(get_db)
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

    # Messages processing
    try:
        while True:
            data = await websocket.receive_json()

    except WebSocketDisconnect:
        websocket_manager.disconnect(current_user, websocket)


async def listen_websockets(rabbit_conn: RobustConnection):
    async with rabbit_conn:
        # Creating channel
        channel = await rabbit_conn.channel()

        websockets_messages = await channel.declare_exchange(
            RABBIT_WEBSOCKETS_EXCHANGE, ExchangeType.FANOUT
        )

        # Declaring queue
        queue = await channel.declare_queue()
        await queue.bind(websockets_messages)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    msg = message.body.decode('utf-8')
                    if not msg:
                        continue
                    msg = json.loads(msg)

                    response = {
                        'payload': {
                            'type': 'notification',
                            'messages': msg['text']
                        }
                    }
                    response.update(success_response)
                    await websocket_manager.send_personal_message(msg['to_user'], response)


@router.post('/notifications/', response_model=NotificationsList)
async def notifications(
    request: Request = Depends(check_auth),
    session: Session = Depends(get_db),
    limit: int = Body(...),
    offset: int = Body(...)
):
    """Get all notifications for user"""
    limit = min(limit, 10)
    self_user_id = request.state.user
    with session as db:
        notifications = get_list_notifications(
            db,
            self_user_id,
            limit=limit,
            offset=offset
        )

    events = set(x.event_id for x in notifications)
    events = get_event_by_id(events)
    events = {
        x.id: x
        for x
        in events
    }
    result = []
    for note in notifications:
        event = events[note.event_id]

        result.append(
            {
                'text': note.formate_notification_text(event.text),
                'created_at': note.created_at
            }
        )

    response = {
        'payload': {
            'notifications': result
        }
    }
    response.update(success_response)
    return response


@router.post('/read_notification/')
async def notifications(
    notification: str = Body(...),
    request: Request = Depends(check_auth),
    session: Session = Depends(get_db)
):
    print(notification)
    return {}
