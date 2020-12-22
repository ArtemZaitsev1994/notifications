from fastapi import APIRouter
from common.common_websocket import router


routes = APIRouter()

routes.include_router(router)

def set_routes(app):
    for route in routes:
        app.include_router(
            route.router,
            prefix=route.prefix,
        )
