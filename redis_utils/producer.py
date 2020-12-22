import asyncio
import aioredis


class TramProducer:
    def __init__(self, channel: aioredis.Channel):
        self._future = None
        self._channel = channel

    def __aiter__(self):
        return self

    def __anext__(self):
        return asyncio.shield(self._get_message())

    async def _get_message(self):
        if self._future:
            return await self._future

        self._future = asyncio.get_event_loop().create_future()
        message = await self._channel.get_json()
        future, self._future = self._future, None
        future.set_result(message)
        return message
