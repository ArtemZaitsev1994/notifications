from typing import List

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from user_info.models import UserInfo
from common.models import NotificationBase, NotificationsHistory
from orders.models import OrderNotification
from premises.models import PremisesNotification



async def send_sms(phone_number: str, text: str):
    print(f'Sent sms with text: "{text}". to {phone_number}')


async def send_email(email: str, text: str):
    print(f'Sent email with text: "{text}". to {email}')


async def send_push(*args, **kwargs):
    ...


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


def save_in_history(notification: str, to_user: str):
    return NotificationsHistory(notification=notification, to_user=to_user)
