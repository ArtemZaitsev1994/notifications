import asyncio

import aioredis


sub = await aioredis.create_redis(
     'redis://localhost')

ch1, ch2 = await sub.subscribe('channel:1', 'channel:2')
assert isinstance(ch1, aioredis.Channel)
assert isinstance(ch2, aioredis.Channel)

async def async_reader(channel):
    while await channel.wait_message():
        msg = await channel.get(encoding='utf-8')
        # ... process message ...
        print("message in {}: {}".format(channel.name, msg))

tsk1 = asyncio.ensure_future(async_reader(ch1))

# Or alternatively:

async def async_reader2(channel):
    while True:
        msg = await channel.get(encoding='utf-8')
        if msg is None:
            break
        # ... process message ...
        print("message in {}: {}".format(channel.name, msg))

tsk2 = asyncio.ensure_future(async_reader2(ch2))
