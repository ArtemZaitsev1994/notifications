import uuid
from .schemas import OrderCreate
from .models import OrderNotification
from sqlalchemy.sql import text


def order_create(data: dict, engine):
    query = '''
    INSERT INTO order_notifications
    (id, "order", from_user, to_user, created_at, event_id, received)
    VALUES (
        :uuid,
        :order,
        :from_user,
        :to_user,
        now(),
        1,
        FALSE
    )
    '''

    with engine.connect() as con:
        validated_data = OrderCreate(**data).dict()
        validated_data['uuid'] = str(uuid.uuid4())
        rs = con.execute(text(query), **validated_data)


available_events = {
    'order_create': order_create
}
