from core.utils import get_db
from .schemas import UserInfoCreate
from .models import UserInfo


async def create_user(data: dict):

    with get_db() as db:
        validated_data = UserInfoCreate(**data).dict()
        user = UserInfo(**validated_data)

        db.add(user)
        db.commit()
        db.refresh(user)

    return user


def get_user_info(_id: str):

    with get_db() as db:
        result = db.query(
            UserInfo
        ).filter(
            UserInfo.id == _id
        ).first()
    return result


available_events = {
    'create_user': create_user
}
receiver = ('user_info', available_events)
