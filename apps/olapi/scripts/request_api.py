import logging

import httpx2
from authentication.keycloak import check_response

from dtos.auth import Credentials, TokenResponse
from dtos.user import User, UserCreatePayload

logger = logging.getLogger(__name__)


def main(
    username: str,
    email: str,
    password: str,
) -> None:

    response = httpx2.post(
        "http://localhost:8000/users",
        json=UserCreatePayload(
            email=email,
            password=password,
            username=username,
        ).model_dump(mode="json"),
    )
    check_response(response)
    user = User.model_validate(response.json())
    logger.info(f"User created: {user}")

    response = httpx2.post(
        "http://localhost:8000/login",
        json=Credentials(email=email, password=password).model_dump(mode="json"),
    )
    check_response(response)
    token_info = TokenResponse.model_validate(response.json())
    logger.info(f"Token fetched: {token_info}")

    response = httpx2.get(
        "http://localhost:8000/hello",
        headers={"Authorization": f"Bearer {token_info.access_token}"},
    )
    check_response(response)
    logger.info(f"Hello response: {response.json()}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    main(
        username="someone",
        email="someone@example.com",
        password="123456789",
    )
