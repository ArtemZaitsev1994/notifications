from typing import List

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from user_info.models import UserInfo
from user_info.services import get_user_info
from orders.models import OrderNotification
from premises.models import PremisesNotification
from core.utils import get_db
from .utils import (
    send_sms,
    send_email,
    send_push,
    create_notification,
    add_notification_to_history
)
from .events import get_event_by_name
from ..models import NotificationBase, NotificationsHistory


async def send_all_ways_notification(user: UserInfo, notification: str):
    if user.available_sms_notification and user.cellphone and user.country_code:
        phone_number = user.country_code + user.phone
        await send_sms(phone_number, notification)

    if user.available_email_notification and user.email:
        await send_email(user.email, notification)

    await send_push()


def get_list_notifications(
    db: Session,
    user: str,
    limit: int = 10,
    offset: int = 0
) -> List[NotificationBase]:
    notifications_id = db.query(
        NotificationsHistory.notification
    ).filter(
        NotificationsHistory.to_user == user
    ).order_by(
        desc(NotificationsHistory.created_at)
    ).offset(offset).limit(limit).all()

    notifications_id = [x[0] for x in notifications_id]

    notifications = db.query(
        OrderNotification
    ).filter(
        OrderNotification.id.in_(notifications_id)
    ).all()

    notifications += db.query(
        PremisesNotification
    ).filter(
        PremisesNotification.id.in_(notifications_id)
    ).all()

    return sorted(notifications, key=lambda x: x.created_at, reverse=True)


async def common_notification_processing(action: str, data: dict, notification_model):
    event = get_event_by_name(action)

    with get_db() as db:
        n = await create_notification(db, data, event, notification_model)
        await add_notification_to_history(db, n.id, n.to_user)
        db.refresh(n)

    user_info = get_user_info(n.to_user)
    text = n.formate_notification_text(event.text)
    await send_all_ways_notification(user_info, event.text)
    return n, text
