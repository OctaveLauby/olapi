from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from settings import settings

# TODO: use context managers ?

engine = create_engine(settings.database_url, pool_pre_ping=True)
session_maker = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    db = session_maker()
    try:
        yield db
    finally:
        db.close()
