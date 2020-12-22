import asyncio
import json

from .services import available_events
from redis_utils.producer import TramProducer


async def premises_receiver(channel):
    producer = TramProducer(channel)
    try:
        async for msg in producer:
            func = available_events.get(msg['type'])
            if func is None:
                print(f'wrong message: {msg}')
                continue

            try:
                func(msg['data'])
            except Exception as e:
                print(f'error {e}')
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f'error {e}')

    # while await channel.wait_message():
    #     msg = await channel.get_json()
    #
    #     print(available_events)
    #     func = available_events.get(msg['type'])
    #     if func is None:
    #         print(f'wrong message: {msg}')
    #         continue
    #
    #     try:
    #         func(msg['data'])
    #     except Exception as e:
    #         print(f'error {e}')


receiver = ('channel:premises', available_events)
