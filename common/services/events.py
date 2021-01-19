from core.utils import get_db
from ..models import Events


events = {
    'create_order': {
        'name': 'create_order',
        'id': 1,
        'text': '''
    New order has been created for your premises!        
    '''
    },
    'update_order': {
        'name': 'update_order',
        'id': 2,
        'text': '''
    Order has been changed by tenant!        
    '''
    },
    'decline_order': {
        'name': 'decline_order',
        'id': 3,
        'text': '''
    Order has been denied by owner!        
    '''
    },
    'confirm_order': {
        'name': 'confirm_order',
        'id': 4,
        'text': '''
    Order has been confirmed by owner!        
    '''
    },
    'create_premises': {
        'name': 'create_premises',
        'id': 5,
        'text': '''
    New premises has been created!        
    '''
    },
    'payment_succeeded': {
        'name': 'payment_succeeded',
        'id': 6,
        'text': '''
    Payment succeeded.        
    '''
    },
    'subscription_started': {
        'name': 'subscription_started',
        'id': 7,
        'text': '''
    Subscription has been started.      
    '''
    }
}


def create_events():
    with get_db() as db:
        for i in events.values():
            e = Events(
                text=i['text'].strip(),
                id=i['id'],
                name=i['name']
            )
            db.add(e)
            db.commit()


def get_event_by_name(event):
    with get_db() as db:
        result = db.query(
            Events
        ).filter(
            Events.name == event
        ).first()
    return result


def get_event_by_id(id):
    with get_db() as db:
        if isinstance(id, str):
            result = db.query(
                Events
            ).filter(
                Events.id == id
            ).first()
        else:
            result = db.query(
                Events
            ).filter(
                Events.id.in_(id)
            ).all()
    return result
