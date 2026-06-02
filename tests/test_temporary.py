from conftest import TEST_AUTH_ID
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from olapi.models.user import UserModel


def test_get_hello(app_client: TestClient, db_session: Session):
    response = app_client.get("/hello")
    assert response.status_code == 401

    db_session.add(UserModel(auth_id=TEST_AUTH_ID, username="alice", email="alice.bob@example.com"))
    db_session.commit()
    response = app_client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello alice !"}


def test_fails():
    assert False  # noqa: B011
