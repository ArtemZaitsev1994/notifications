import asyncio
import uvloop

from fastapi import FastAPI

from routers import routes
from _redis import get_redis_pool, set_readers


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = FastAPI()
app.include_router(routes)


@app.on_event('startup')
async def startup():
    asyncio.ensure_future(set_readers())
