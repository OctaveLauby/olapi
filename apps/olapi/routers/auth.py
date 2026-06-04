import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session
from ulid import ULID

from auth import auth_client
from authentication import exceptions as auth_exceptions
from database import get_session
from dtos.auth import Credentials, TokenResponse
from dtos.user import User, UserCreatePayload
from models.user import UserModel

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreatePayload, session: Session = Depends(get_session)) -> User:
    try:
        session.execute(
            select(UserModel).where(
                (UserModel.username == payload.username) | (UserModel.email == payload.email)
            )
        ).scalar_one_or_none()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already taken.",
        ) from None
    try:
        user_auth_id = auth_client.create_user(payload.email, payload.password)
    except auth_exceptions.UserExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email already registered in authentication service",
        ) from None
    logger.debug(f"User {payload.email} saved authentication service.")
    user_model = UserModel(auth_id=user_auth_id, username=payload.username, email=payload.email)
    try:
        session.add(user_model)
        session.commit()
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
    except auth_exceptions.UnauthorizedError as e:
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
                auth_id=user_keycloak_id,
                username=str(ULID()),
                email=payload.email,
            )
        )
        session.commit()
    return TokenResponse.from_info(token_info)
