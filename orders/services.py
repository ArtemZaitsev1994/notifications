from .schemas import OrderCreate
from .models import OrderNotification
from core.utils import get_db


def order_create(data: dict):
    with get_db() as db:
        validated_data = OrderCreate(**data).dict()
        n = OrderNotification(**validated_data)

        db.add(n)
        db.commit()
    return True


available_events = {
    'order_create': order_create
}
