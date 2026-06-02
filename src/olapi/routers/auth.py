import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ulid import ULID

from authentication.keycloak import AuthenticationError
from olapi.auth import auth_client
from olapi.dependencies import get_session
from olapi.models.user import UserModel
from olapi.schemas.auth import Credentials, TokenResponse
from olapi.schemas.user import User, UserCreatePayload

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreatePayload, session: Session = Depends(get_session)) -> User:
    existing = session.execute(
        select(UserModel).where(
            (UserModel.username == payload.username) | (UserModel.email == payload.email)
        )
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already taken",
        )
    user_auth_id = auth_client.create_user(payload.email, payload.password)
    logger.debug(f"User {payload.email} saved authentication service.")
    user_model = UserModel(
        keycloak_id=user_auth_id,
        username=payload.username,
        email=payload.email,
    )
    try:
        session.add(user_model)
        session.commit()
        session.refresh(user_model)
        logger.debug(f"User {payload.email} saved database.")
    except SQLAlchemyError:
        session.rollback()
        auth_client.delete_user(user_auth_id)
        logger.debug(f"User {payload.email} deleted from authentication service.")
        raise
    return User.from_model(user_model)


@router.post("/login", response_model=TokenResponse)
def login(payload: Credentials, session: Session = Depends(get_session)) -> TokenResponse:
    try:
        token_info = auth_client.get_user_token(payload.email, payload.password)
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e

    # Create user if does not exist in db
    user_keycloak_id = auth_client.validate_token(token=token_info.access_token)
    exists = session.execute(
        select(UserModel).where(UserModel.auth_id == user_keycloak_id)
    ).scalar_one_or_none()
    if exists is None:
        logger.debug(f"User {payload.email} saved in database at logging.")
        session.add(
            UserModel(
                keycloak_id=user_keycloak_id,
                username=str(ULID()),
                email=payload.email,
            )
        )
        session.commit()
    return TokenResponse.from_info(token_info)
