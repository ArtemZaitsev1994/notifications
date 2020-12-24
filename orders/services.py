from .schemas import OrderCreate
from .models import OrderNotification
from common.models import Events
from core.utils import get_db
from common.events import get_event_by_name
from user_info.services import get_user_info
from common.services import send_all_ways_notification, save_in_history


async def create_notification(data: dict, event: Events):
    with get_db() as db:
        validated_data = OrderCreate(**data).dict()
        n = OrderNotification(**validated_data, event_id=event.id)
        db.add(n)
        db.flush()
        db.refresh(n)

        h = save_in_history(n.id, n.to_user)
        db.add(h)
        db.commit()
        db.refresh(n)
    return n


async def common_notification_processing(action: str, data: dict):
    event = get_event_by_name(action)
    n = await create_notification(data, event)

    user_info = get_user_info(n.to_user)
    text = n.formate_notification_text(event.text)
    await send_all_ways_notification(user_info, event.text)
    return n, text


async def create_order(data: dict):
    event_name = 'create_order'
    return await common_notification_processing(event_name, data)


async def confirm_order(data: dict):
    event_name = 'confirm_order'
    return await common_notification_processing(event_name, data)


async def decline_order(data: dict):
    event_name = 'decline_order'
    return await common_notification_processing(event_name, data)


async def update_order(data: dict):
    event_name = 'update_order'
    return await common_notification_processing(event_name, data)


available_events = {
    'create_order': create_order,
    'confirm_order': confirm_order,
    'decline_order': decline_order,
    'update_order': update_order
}
receiver = ('orders', available_events)
