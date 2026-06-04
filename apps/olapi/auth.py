from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from authentication import exceptions as auth_exceptions
from authentication.keycloak import KeycloakClient
from database import get_session
from models.user import UserModel
from settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)
auth_client = KeycloakClient(
    keycloak_url=settings.keycloak_url,
    keycloak_admin_user=settings.keycloak_admin_user,
    keycloak_admin_password=settings.keycloak_admin_password,
    keycloak_realm=settings.keycloak_realm,
    keycloak_client_id=settings.keycloak_client_id,
)


def check_authentication(token: str | None = Depends(oauth2_scheme)) -> str:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")
    try:
        user_auth_id = auth_client.validate_token(token)
    except auth_exceptions.UnauthorizedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid"
        ) from None
    return user_auth_id


def get_user(
    user_auth_id: str = Depends(check_authentication),
    session: Session = Depends(get_session),
) -> UserModel:
    try:
        user = session.execute(
            select(UserModel).where(UserModel.auth_id == user_auth_id)
        ).scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="unknown user"
        ) from None
    return user
