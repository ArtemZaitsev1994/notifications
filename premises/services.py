import uuid

from sqlalchemy import text
from .schemas import PremisesCreate


def premises_create(data: dict, engine):
    query = '''
    INSERT INTO premises_notifications
    (id, premises, from_user, to_user, created_at, event_id, received)
    VALUES (
        :uuid,
        :premises,
        :from_user,
        :to_user,
        now(),
        1,
        FALSE
    )
    '''

    with engine.connect() as con:
        validated_data = PremisesCreate(**data).dict()
        validated_data['uuid'] = str(uuid.uuid4())
        rs = con.execute(text(query), **validated_data)

available_events = {
    'premises_create': premises_create
}

