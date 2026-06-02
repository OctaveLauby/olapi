from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from olapi.auth import check_authentication
from olapi.database import get_session
from olapi.main import app
from olapi.models.base import BaseModel

TEST_AUTH_ID = "test-auth-id"


@pytest.fixture
def db_session() -> Generator[Session]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    BaseModel.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def app_client(db_session: Session) -> Generator[TestClient]:
    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[check_authentication] = lambda: TEST_AUTH_ID
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
