import asyncio
import json

import aioredis

from settings import REDIS_PORT, REDIS_HOST
from orders.receiver import receiver as order_receiver
from premises.receiver import receiver as premises_receiver


consumers = {
    name: consumer
    for name, consumer
    in [
        order_receiver,
        premises_receiver
    ]
}


async def get_redis_pool() -> aioredis.ConnectionsPool:
    try:
        pool = await aioredis.create_redis_pool(
            (REDIS_HOST, REDIS_PORT), encoding='utf-8')
        return pool
    except ConnectionRefusedError:
        print('cannot connect to redis on:', REDIS_HOST, REDIS_PORT)
        return None


async def single_reader(mpsc):
    from core.utils import get_db
    from core.db import engine
    db = next(get_db())
    async for channel, message in mpsc.iter():

        message = json.loads(message.decode("utf-8"))
        print(message.get('type'))
        consumer = consumers.get(channel.name.decode("utf-8"))
        print(consumer)
        if consumer is None or (func := consumer.get(message.get('type'), '')) is None:
            print(f'Wrong message {message}')
            continue

        print(message['data'])
        try:
            func(message['data'], engine)
        except Exception as e:
            print(f'Error: {e}')
        # else:
        #     db.commit()


async def set_readers():

    from aioredis.pubsub import Receiver

    mpsc = Receiver()

    # run reader
    asyncio.ensure_future(single_reader(mpsc))

    pool = await get_redis_pool()

    # use mpsc to add channles
    await pool.subscribe(
        *[
            mpsc.channel(x)
            for x
            in consumers
        ]
    )
