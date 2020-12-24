import datetime
import uuid
from contextlib import contextmanager

import jwt
from fastapi import Request, HTTPException
from starlette import status

from .db import SessionLocal
from settings import SECRET_KEY


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def row2dict(row) -> dict:
    should_be_string = (datetime.datetime, uuid.UUID)
    d = {}
    for column in row.__table__.columns:
        attr = getattr(row, column.name)
        d[column.name] = str(attr) if isinstance(attr, should_be_string) else attr
    return d


def check_auth(request: Request):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header not provided'
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=['HS256'])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token invalid'
        )
    request.state.user = payload['id']
    return request
