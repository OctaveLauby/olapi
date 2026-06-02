import logging

import httpx2

from authentication import exceptions as auth_exceptions
from authentication.keycloak import KeycloakClient

logger = logging.getLogger(__name__)


def main(
    email: str,
    password: str,
    delete: bool = False,
) -> None:
    authenticator = KeycloakClient(
        keycloak_url="http://localhost:8080",
        keycloak_realm="olapi",
        keycloak_client_id="olapi-api",
        keycloak_admin_user="admin",
        keycloak_admin_password="admin",
    )
    try:
        token_info = authenticator.get_user_token(email=email, password=password)
        logger.info(f"Got token from existing user: '{token_info}'.")
    except httpx2.ConnectError:
        logger.info("Could not connect to keycloack: make sure keycloak container is up.")
        raise
    except auth_exceptions.AuthenticationError:
        user_id = authenticator.create_user(email=email, password=password)
        logger.info(f"New user created with id='{user_id}'.")
        token_info = authenticator.get_user_token(email=email, password=password)
        logger.info(f"New token created: {token_info}.")
    user_auth_id = authenticator.validate_token(token_info.access_token)
    logger.info(f"Got user from token: {user_auth_id}.")

    if delete:
        authenticator.delete_user(user_id=user_auth_id)
        logger.info("User deleted.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    main(
        email="someone@example.com",
        password="123",
        delete=False,
    )
