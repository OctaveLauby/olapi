from collections.abc import Iterator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from authentication import exceptions as auth_exceptions
from olapi.auth import auth_client
from olapi.database import session_maker
from olapi.models.user import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_session() -> Iterator[Session]:
    db = session_maker()
    try:
        yield db
    finally:
        db.close()


def current_user(
    token: str | None = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> UserModel:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")
    try:
        user_auth_id = auth_client.validate_token(token)
    except auth_exceptions.UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e
    try:
        user = session.execute(
            select(UserModel).where(UserModel.auth_id == user_auth_id)
        ).scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="unknown user"
        ) from None
    return user
