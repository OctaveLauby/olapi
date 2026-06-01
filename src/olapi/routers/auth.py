import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ulid import ULID

from auth.keycloak import AuthenticationError
from olapi.auth import authenticator
from olapi.deps import get_db
from olapi.dtos.auth import LoginRequest, TokenResponse
from olapi.dtos.user import User, UserCreate
from olapi.models.user import UserModel

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    existing = db.execute(
        select(UserModel).where(
            (UserModel.username == payload.username) | (UserModel.email == payload.email)
        )
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already taken",
        )
    keycloak_id = authenticator.create_user(payload.email, payload.password)
    logger.info(f"User {payload.email} saved authentication service.")
    user_model = UserModel(
        keycloak_id=keycloak_id,
        username=payload.username,
        email=payload.email,
    )
    try:
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
        logger.info(f"User {payload.email} saved database.")
    except SQLAlchemyError:
        db.rollback()
        authenticator.delete_user(keycloak_id)
        logger.info(f"User {payload.email} deleted from authentication service.")
        raise
    return User.from_model(user_model)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        token_info = authenticator.get_user_token(payload.email, payload.password)
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e

    # Create user if does not exist in db
    keycloak_user = authenticator.get_user_from_token(token=token_info.access_token)
    exists = db.execute(
        select(UserModel).where(UserModel.keycloak_id == keycloak_user.id)
    ).scalar_one_or_none()
    if exists is None:
        logger.info(f"User {payload.email} saved in database at logging.")
        db.add(
            UserModel(
                keycloak_id=keycloak_user.id,
                username=str(ULID()),
                email=payload.email,
            )
        )
        db.commit()
    return TokenResponse.from_info(token_info)
