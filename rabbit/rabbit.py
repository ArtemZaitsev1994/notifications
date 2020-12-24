import json
import aioredis

import aio_pika
from orders.receiver import receiver as order_receiver
from premises.receiver import receiver as premises_receiver
from premises.services import premises_create
from settings import REDIS_HOST, REDIS_PORT


consumers = {
    name: consumer
    for name, consumer
    in [
        order_receiver,
        premises_receiver
    ]
}


async def listen_notifications(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@localhost/", loop=loop
    )

    queue_name = "notifications"

    # redis connection to publish messages for websocket handler
    redis = await aioredis.create_redis(f"redis://{REDIS_HOST}:{REDIS_PORT}")

    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        msg = message.body.decode('utf-8')
                        if not msg:
                            continue
                        msg = json.loads(msg)

                        func = consumers.get(msg['section'], {}).get(msg['action'])
                        notification = func(msg['data'])
                        print(notification)

                        await redis.publish(msg['to_user'], notification.text)

                    except Exception as err:
                        print(err)
                        continue
                    # consumer = premises_receiver[1]
                    # if consumer is None or (func := consumer.get(message.get('type'), '')) is None:
                    #     print(f'Wrong message {message}')
                    #     continue

                    # print(message['data'])
                    # try:
                    #     func(message['data'])
                    # except Exception as e:
                    #     print(f'Error: {e}')

                    # if queue.name in message.body.decode():
                    #     break