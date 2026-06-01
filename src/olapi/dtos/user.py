from datetime import datetime
from typing import Self

from pydantic import BaseModel, EmailStr, Field

from olapi.models.user import UserModel


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    registration_date: datetime

    @classmethod
    def from_model(cls, model: UserModel) -> Self:
        return cls(
            id=model.id,
            username=model.username,
            email=model.email,
            registration_date=model.registration_date,
        )
