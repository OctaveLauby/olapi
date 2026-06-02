import logging
from dataclasses import dataclass
from typing import Any, cast

import httpx2
from jose import jwt
from starlette import status as status_codes

from authentication import exceptions

logger = logging.getLogger(__name__)


@dataclass
class TokenInfo:
    access_token: str
    expires_in: int


def _check_response(response: httpx2.Response) -> None:
    try:
        response.raise_for_status()
    except httpx2.HTTPStatusError:
        response.read()
        logger.error(
            f"Failed {response.request.method} {response.request.url.path}"
            f": {response.status_code} {response.text}"
        )  # Log response details as they are not shown in raised error
        raise


class KeycloakClient:
    def __init__(
        self,
        keycloak_url: str,
        keycloak_admin_user: str,
        keycloak_admin_password: str,
        keycloak_realm: str,
        keycloak_client_id: str,
    ):
        self._keycloak_url = keycloak_url
        self._keycloak_admin_user = keycloak_admin_user
        self._keycloak_admin_password = keycloak_admin_password
        self._keycloak_realm = keycloak_realm
        self._keycloak_client_id = keycloak_client_id

        self._client = httpx2.Client(
            base_url=self._keycloak_url,
            timeout=10.0,
            event_hooks={"response": [_check_response]},
        )
        self._jwks: dict[str, Any] | None = None

    def _load_jwks(self) -> dict[str, Any]:
        # TODO: add jwk expiration date management
        if self._jwks is not None:
            return self._jwks
        response = self._client.get(
            f"/realms/{self._keycloak_realm}/protocol/openid-connect/certs",
            timeout=10.0,
        )
        self._jwks = cast(dict[str, Any], response.json())
        return self._jwks

    def _admin_token(self) -> str:
        # TODO: cache that
        response = self._client.post(
            "/realms/master/protocol/openid-connect/token",
            data={
                "grant_type": "password",
                "client_id": "admin-cli",
                "username": self._keycloak_admin_user,
                "password": self._keycloak_admin_password,
            },
        )
        payload: dict[str, Any] = response.json()
        return str(payload["access_token"])

    def create_user(self, email: str, password: str) -> str:
        token = self._admin_token()
        try:
            response = self._client.post(
                f"/admin/realms/{self._keycloak_realm}/users",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "email": email,
                    "enabled": True,
                    "credentials": [{"type": "password", "value": password, "temporary": False}],
                },
            )
        except httpx2.HTTPStatusError as exc:
            if exc.response.status_code == status_codes.HTTP_409_CONFLICT:
                raise exceptions.UserExistsError(f"User '{email}' already exist.") from None
            raise
        location = response.headers[
            "location"
        ]  # "http://keycloak:8080/admin/realms/olapi/users/<id>"
        return location.rsplit("/", 1)[-1]

    def delete_user(self, user_id: str) -> None:
        token = self._admin_token()
        self._client.delete(
            f"/admin/realms/{self._keycloak_realm}/users/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

    def get_user_token(self, email: str, password: str) -> TokenInfo:
        try:
            response = self._client.post(
                f"/realms/{self._keycloak_realm}/protocol/openid-connect/token",
                data={
                    "grant_type": "password",
                    "client_id": self._keycloak_client_id,
                    "username": email,
                    "password": password,
                },
            )
        except httpx2.HTTPStatusError as exc:
            if exc.response.status_code == status_codes.HTTP_401_UNAUTHORIZED:
                raise exceptions.UnauthorizedError("Unauthorized") from None
            raise
        response_data = response.json()
        # {'access_token': '*.*.*-*-*-*', 'expires_in': 300, 'token_type': 'Bearer',
        #  'refresh_token': '*.*.*-*-*-*', 'refresh_expires_in': 1800,
        #  'not-before-policy': 0, 'scope': 'email profile', 'session_state': '*-*-*-*-*'
        # }
        return TokenInfo(
            access_token=response_data["access_token"],
            expires_in=response_data["expires_in"],
        )

    def validate_token(self, token: str) -> str:
        """Validate token with jwks and return user id."""
        jwks = self._load_jwks()
        header = jwt.get_unverified_header(token)
        public_key = next((k for k in jwks["keys"] if k["kid"] == header.get("kid")), None)
        if public_key is None:
            raise exceptions.UnauthorizedError(
                "Token invalid: public key couldn't be found in jwks."
            )
        token_json: dict[str, Any] = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=f"{self._keycloak_url}/realms/{self._keycloak_realm}",
            options={"verify_aud": False},
        )
        assert isinstance(token_json["sub"], str)
        return token_json["sub"]
