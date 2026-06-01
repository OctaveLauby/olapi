from collections.abc import Iterator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from olapi.auth.jwt import TokenError, decode_token
from olapi.db import SessionLocal
from olapi.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")
    try:
        claims = decode_token(token)
    except TokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e
    user = db.execute(select(User).where(User.keycloak_id == claims["sub"])).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unknown user")
    return user
