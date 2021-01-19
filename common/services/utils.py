from common.models import NotificationBase, NotificationsHistory, Events


async def send_sms(phone_number: str, text: str):
    print(f'Sent sms with text: "{text}". to {phone_number}')


async def send_email(email: str, text: str):
    print(f'Sent email with text: "{text}". to {email}')


async def send_push(*args, **kwargs):
    ...


def save_in_history(notification: str, to_user: str):
    return NotificationsHistory(notification=notification, to_user=to_user)


async def add_notification_to_history(db, event_id: str, to_user: str):
    h = save_in_history(event_id, to_user)
    db.add(h)
    db.commit()
    return h


async def create_notification(db, data: dict, event: Events, Nnotification_model):
    n = Nnotification_model(**data, event_id=event.id)
    db.add(n)
    db.flush()
    db.refresh(n)
    return n
