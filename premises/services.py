from .schemas import PremisesCreate
from .models import PremisesNotification
from common.services.services import common_notification_processing


async def create_premises(data: dict):
    event_name = 'create_premises'
    validated_data = PremisesCreate(**data).dict()
    n = await common_notification_processing(
        event_name,
        validated_data,
        PremisesNotification
    )
    return n


available_events = {
    'create_premises': create_premises
}
receiver = ('premises', available_events)
