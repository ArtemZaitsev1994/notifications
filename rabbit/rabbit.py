import json

import aio_pika
from aio_pika import (
    connect,
    IncomingMessage,
    ExchangeType,
    Message,
    DeliveryMode,
    RobustConnection
)
from uvloop import Loop
from pydantic import ValidationError

from orders.services import receiver as order_receiver
from premises.services import receiver as premises_receiver
from user_info.services import receiver as user_info_receiver
from settings import (
    REDIS_HOST,
    REDIS_PORT,
    RABBIT_WEBSOCKETS_EXCHANGE,
    RABBIT_NOTIFICATIONS_EXCHANGE,
    RABBIT_HOST
)
from .schemas import RabbitMessage


consumers = {
    name: consumer
    for name, consumer
    in [
        order_receiver,
        premises_receiver,
        user_info_receiver
    ]
}

async def get_rabbit_conn(loop: Loop):
    connection = await aio_pika.connect_robust(
        RABBIT_HOST, loop=loop
    )
    return connection


async def listen_notifications(rabbit_conn: RobustConnection):

    async with rabbit_conn:
        # Creating channel
        channel = await rabbit_conn.channel()

        notifications_exchange = await channel.declare_exchange(
            RABBIT_NOTIFICATIONS_EXCHANGE, ExchangeType.FANOUT
        )
        websockets_messages = await channel.declare_exchange(
            RABBIT_WEBSOCKETS_EXCHANGE, ExchangeType.FANOUT
        )

        # Declaring queue
        queue = await channel.declare_queue()
        await queue.bind(notifications_exchange)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        msg = message.body.decode('utf-8')
                        if not msg:
                            continue
                        msg = json.loads(msg)

                        try:
                            msg = RabbitMessage(**msg).dict()
                        except ValidationError:
                            continue

                        func = consumers.get(msg['section'], {}).get(msg['action'])
                        action_result = await func(msg['data'])

                        if msg.get('need_response_to_websocket') and len(action_result) == 2:
                            notification, text = action_result
                            notification_info = {
                                'to_user': str(notification.to_user),
                                'text': text
                            }

                            # send message to websockets
                            message_body = json.dumps(notification_info)
                            message = Message(
                                bytes(message_body, 'utf-8'),
                                delivery_mode=DeliveryMode.PERSISTENT
                            )
                            await websockets_messages.publish(message, routing_key="")

                    except Exception as err:
                        print(err)
                        continue
