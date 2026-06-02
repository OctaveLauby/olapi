import logging

import httpx

from olapi.schemas.auth import Credentials, TokenResponse

logger = logging.getLogger(__name__)


def main(
    email: str,
    password: str,
) -> None:
    response = httpx.post(
        "http://localhost:8000/login",
        json=Credentials(email=email, password=password).model_dump(mode="json"),
    )
    response.raise_for_status()
    token_info = TokenResponse.model_validate(response.json())
    logger.info(f"Token fetched: {token_info}")

    response = httpx.get(
        "http://localhost:8000/hello",
        headers={"Authorization": f"Bearer {token_info.access_token}"},
    )
    response.raise_for_status()
    logger.info(f"Hello response: {response.json()}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    main(
        email="olauby@example.com",
        password="123",
    )
