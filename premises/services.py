from .schemas import PremisesCreate
from .models import PremisesNotification
from common.models import Events
from core.utils import get_db
from common.events import get_event_by_name
from user_info.services import get_user_info
from common.services import send_all_ways_notification, save_in_history


async def create_notification(data: dict, event: Events):
    with get_db() as db:
        validated_data = PremisesCreate(**data).dict()
        n = PremisesNotification(**validated_data, event_id=event.id)
        db.add(n)
        db.flush()
        db.refresh(n)

        h = save_in_history(n.id, n.to_user)
        db.add(h)
        db.commit()
        db.refresh(n)
    return n


async def create_premises(data: dict):
    event_name = 'create_premises'
    event = get_event_by_name(event_name)
    n = await create_notification(data, event)

    user_info = get_user_info(n.to_user)
    text = n.formate_notification_text(event.text)
    await send_all_ways_notification(user_info, event.text)
    return n, text


available_events = {
    'create_premises': create_premises
}
receiver = ('premises', available_events)
