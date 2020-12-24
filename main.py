import asyncio
import uvloop

from fastapi import FastAPI

from routers import routes
from rabbit.rabbit import listen_notifications, get_rabbit_conn
from common.common_websocket import listen_websockets
# from redis_utils._redis import get_redis_pool
from starlette.middleware.cors import CORSMiddleware

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = FastAPI()
app.include_router(routes)

origins = [
    "http://localhost:3001",
    "https://localhost:3001",
    "http://192.168.101.75:3001",
    "http://134.122.73.229:3050"
]

headers = [
    'access-control-allow-credentials',
    'access-control-allow-headers,'
    'accept',
    'ccept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Credentials',
    'set-cookie',
    'access-control-allow-methods',
    'access-control-allow-origin',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["OPTIONS", "DELETE", "GET", "POST", "PUT"],
    allow_headers=headers,
)


@app.on_event('startup')
async def startup():
    loop = asyncio.get_event_loop()

    # redis_pool = await get_redis_pool()
    rabbit_conn = await get_rabbit_conn(loop)

    asyncio.ensure_future(listen_notifications(rabbit_conn))
    asyncio.ensure_future(listen_websockets(rabbit_conn))
