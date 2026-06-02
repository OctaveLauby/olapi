from authentication.keycloak import KeycloakClient
from olapi.settings import settings

auth_client = KeycloakClient(
    keycloak_url=settings.keycloak_url,
    keycloak_admin_user=settings.keycloak_admin_user,
    keycloak_admin_password=settings.keycloak_admin_password,
    keycloak_realm=settings.keycloak_realm,
    keycloak_client_id=settings.keycloak_client_id,
)
