from .schemas import PaymentNotificationSerializer
from .models import PaymentNotification
from common.services.services import common_notification_processing


async def payment_succeeded(data: dict):
    event_name = 'payment_succeeded'
    validated_data = PaymentNotificationSerializer(**data).dict()
    n = await common_notification_processing(
        event_name,
        validated_data,
        PaymentNotification
    )
    return n


async def subscription_started(data: dict):
    event_name = 'subscription_started'
    validated_data = PaymentNotificationSerializer(**data).dict()
    n = await common_notification_processing(
        event_name,
        validated_data,
        PaymentNotification
    )
    return n


available_events = {
    'payment_succeeded': payment_succeeded,
    'subscription_started': subscription_started,
}
receiver = ('payment', available_events)
