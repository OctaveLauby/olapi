from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ulid import ULID

from olapi.auth.jwt import decode_token
from olapi.auth.keycloak import KeycloakError, keycloak
from olapi.deps import get_db
from olapi.models.user import User
from olapi.schemas.auth import LoginRequest, TokenResponse
from olapi.schemas.user import UserCreate, UserOut


router = APIRouter()


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    existing = db.execute(
        select(User).where(
            (User.username == payload.username) | (User.email == payload.email)
        )
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already taken",
        )

    try:
        keycloak_id = keycloak.create_user(
            payload.username, payload.email, payload.password
        )
    except KeycloakError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    user = User(
        keycloak_id=keycloak_id,
        username=payload.username,
        email=payload.email,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        db.rollback()
        keycloak.delete_user(keycloak_id)
        raise
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    try:
        token = keycloak.login(payload.username, payload.password)
    except KeycloakError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e

    # JIT-provision local row for users created directly in Keycloak (e.g. via admin UI).
    claims = decode_token(token["access_token"])
    keycloak_id = claims["sub"]
    exists = db.execute(
        select(User).where(User.keycloak_id == keycloak_id)
    ).scalar_one_or_none()
    if exists is None:
        db.add(
            User(
                keycloak_id=keycloak_id,
                username=str(ULID()),
                email=claims.get("email") or f"{keycloak_id}@unknown.local",
            )
        )
        db.commit()
    return token
