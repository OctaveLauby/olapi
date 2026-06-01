from typing import Any

import httpx

from olapi.config import settings


class KeycloakError(Exception):
    pass


class KeycloakClient:
    def __init__(self) -> None:
        self._client = httpx.Client(base_url=settings.keycloak_url, timeout=10.0)

    def _admin_token(self) -> str:
        r = self._client.post(
            "/realms/master/protocol/openid-connect/token",
            data={
                "grant_type": "password",
                "client_id": "admin-cli",
                "username": settings.keycloak_admin_user,
                "password": settings.keycloak_admin_password,
            },
        )
        r.raise_for_status()
        payload: dict[str, Any] = r.json()
        return str(payload["access_token"])

    def create_user(self, username: str, email: str, password: str) -> str:
        token = self._admin_token()
        r = self._client.post(
            f"/admin/realms/{settings.keycloak_realm}/users",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": username,
                "email": email,
                "enabled": True,
                "credentials": [{"type": "password", "value": password, "temporary": False}],
            },
        )
        if r.status_code == 409:
            raise KeycloakError("user already exists in keycloak")
        r.raise_for_status()
        location = r.headers["location"]
        return location.rsplit("/", 1)[-1]

    def delete_user(self, keycloak_id: str) -> None:
        token = self._admin_token()
        r = self._client.delete(
            f"/admin/realms/{settings.keycloak_realm}/users/{keycloak_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        r.raise_for_status()

    def login(self, username: str, password: str) -> dict[str, Any]:
        r = self._client.post(
            f"/realms/{settings.keycloak_realm}/protocol/openid-connect/token",
            data={
                "grant_type": "password",
                "client_id": settings.keycloak_client_id,
                "username": username,
                "password": password,
            },
        )
        if r.status_code == 401:
            raise KeycloakError("invalid credentials")
        r.raise_for_status()
        payload: dict[str, Any] = r.json()
        return payload


keycloak = KeycloakClient()
