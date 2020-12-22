import asyncio
import json

from .services import available_events
from redis_utils.producer import TramProducer


async def order_receiver(channel):
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


# async def order_receiver(channel):
#     while await channel.wait_message():
#         msg = await channel.get_json()
#
#         print(msg)
#         func = available_events.get(msg['type'])
#         if func is None:
#             print(f'wrong message: {msg}')
#             continue
#         try:
#             func(msg['data'])
#         except Exception as e:
#             print(e)
#             print('!')


        # try:
        #     await func(msg['data'])
        # except:
        #     ...

receiver = ('channel:order', available_events)
