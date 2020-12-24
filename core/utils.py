import datetime
import uuid
from contextlib import contextmanager
from .db import SessionLocal


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def row2dict(row) -> dict:
    should_be_string = (datetime, uuid.UUID)
    d = {}
    for column in row.__table__.columns:
        attr = getattr(row, column.name)
        d[column.name] = str(attr) if isinstance(attr, should_be_string) else attr
    return d
