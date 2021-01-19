from .schemas import OrderCreate
from .models import OrderNotification
from common.services.services import common_notification_processing


async def create_order(data: dict):
    event_name = 'create_order'
    validated_data = OrderCreate(**data).dict()
    n = await common_notification_processing(
        event_name,
        validated_data,
        OrderNotification
    )
    return n


async def confirm_order(data: dict):
    event_name = 'confirm_order'
    validated_data = OrderCreate(**data).dict()
    n = await common_notification_processing(
        event_name,
        validated_data,
        OrderNotification
    )
    return n


async def decline_order(data: dict):
    event_name = 'decline_order'
    validated_data = OrderCreate(**data).dict()
    n = await common_notification_processing(
        event_name,
        validated_data,
        OrderNotification
    )
    return n


async def update_order(data: dict):
    event_name = 'update_order'
    validated_data = OrderCreate(**data).dict()
    n = await common_notification_processing(
        event_name,
        validated_data,
        OrderNotification
    )
    return n


available_events = {
    'create_order': create_order,
    'confirm_order': confirm_order,
    'decline_order': decline_order,
    'update_order': update_order
}
receiver = ('orders', available_events)
