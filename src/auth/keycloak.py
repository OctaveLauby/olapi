from dataclasses import dataclass
from typing import Any

import httpx
from jose import jwt

# TODO: consider using https://github.com/marcospereirampj/python-keycloak
# TODO: error management (handle http errors - e.g. 409 on create) + usage in router


@dataclass
class KeycloakUser:
    id: str
    token: str


@dataclass
class TokenInfo:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str


class AuthenticationError(Exception):
    pass


class Authenticator:
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

        self._client = httpx.Client(base_url=self._keycloak_url, timeout=10.0)
        self._jwks: dict[str, Any] | None = None

    def _load_jwks(self) -> dict[str, Any]:
        # TODO: add jwk expiration date management
        if self._jwks is not None:
            return self._jwks
        response = self._client.get(
            f"/realms/{self._keycloak_realm}/protocol/openid-connect/certs",
            timeout=10.0,
        )
        response.raise_for_status()
        self._jwks = response.json()
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
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        return str(payload["access_token"])

    def create_user(self, email: str, password: str) -> str:
        token = self._admin_token()
        response = self._client.post(
            f"/admin/realms/{self._keycloak_realm}/users",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "email": email,
                "enabled": True,
                "credentials": [{"type": "password", "value": password, "temporary": False}],
            },
        )
        response.raise_for_status()
        location = response.headers[
            "location"
        ]  # "http://keycloak:8080/admin/realms/olapi/users/<id>"
        return location.rsplit("/", 1)[-1]

    def delete_user(self, keycloak_id: str) -> None:
        token = self._admin_token()
        response = self._client.delete(
            f"/admin/realms/{self._keycloak_realm}/users/{keycloak_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()

    def get_user_token(self, email: str, password: str) -> TokenInfo:
        response = self._client.post(
            f"/realms/{self._keycloak_realm}/protocol/openid-connect/token",
            data={
                "grant_type": "password",
                "client_id": self._keycloak_client_id,
                "email": email,
                "password": password,
            },
        )
        if response.status_code == 401:
            raise AuthenticationError("invalid credentials")
        response.raise_for_status()
        response_data = response.json()
        access_token = response_data["access_token"]
        if not isinstance(access_token, str):
            raise AuthenticationError(f"invalid access token: {access_token!r}")
        return TokenInfo(
            access_token=response_data["access_token"],
            refresh_token=response_data["refresh_token"],
            expires_in=response_data["expires_in"],
            token_type=response_data["token_type"],
        )

    def get_user_from_token(self, token: str) -> KeycloakUser:
        jwks = self._load_jwks()
        header = jwt.get_unverified_header(token)
        public_key = next((k for k in jwks["keys"] if k["kid"] == header.get("kid")), None)
        if public_key is None:
            raise AuthenticationError("Token invalid: public key couldn't be found in jwks.")
        token_json: dict[str, Any] = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=f"{self._keycloak_url}/realms/{self._keycloak_realm}",
            options={"verify_aud": False},
        )
        return KeycloakUser(token=token, id=token_json["sub"])
