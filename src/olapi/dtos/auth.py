from typing import Self

from pydantic import BaseModel, EmailStr

from auth.keycloak import TokenInfo


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str

    @classmethod
    def from_info(cls, info: TokenInfo) -> Self:
        return cls(
            access_token=info.access_token,
            refresh_token=info.refresh_token,
            expires_in=info.expires_in,
            token_type=info.token_type,
        )
