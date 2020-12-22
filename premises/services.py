from .schemas import PremisesCreate
from .models import PremisesNotification
from core.utils import get_db


def premises_create(data: dict):
    with get_db() as db:
        validated_data = PremisesCreate(**data).dict()
        n = PremisesNotification(**validated_data)

        db.add(n)
        db.commit()


available_events = {
    'premises_create': premises_create
}
