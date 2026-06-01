import httpx
from jose import jwt
from jose.exceptions import JWTError

from olapi.config import settings

_jwks: dict | None = None


def _get_jwks() -> dict:
    global _jwks
    if _jwks is None:
        fetched = httpx.get(
            f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/certs",
            timeout=10.0,
        ).json()
        _jwks = fetched
        return fetched
    return _jwks


class TokenError(Exception):
    pass


def decode_token(token: str) -> dict:
    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        jwks = _get_jwks()
        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if key is None:
            raise TokenError("unknown signing key")
        return jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=f"{settings.keycloak_url}/realms/{settings.keycloak_realm}",
            options={"verify_aud": False},
        )
    except JWTError as e:
        raise TokenError(str(e)) from e
