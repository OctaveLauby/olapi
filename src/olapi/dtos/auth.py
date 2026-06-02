from typing import Self

from pydantic import BaseModel, EmailStr

from authentication.keycloak import TokenInfo


class Credentials(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int

    @classmethod
    def from_info(cls, info: TokenInfo) -> Self:
        return cls(
            access_token=info.access_token,
            expires_in=info.expires_in,
        )
