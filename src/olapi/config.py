from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = "postgresql+psycopg://olapi:olapi@postgres:5432/olapi"
    keycloak_url: str = "http://keycloak:8080"
    keycloak_realm: str = "olapi"
    keycloak_client_id: str = "olapi-api"
    keycloak_admin_user: str = "admin"
    keycloak_admin_password: str = "admin"


settings = Settings()
