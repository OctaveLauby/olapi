import httpx2
import pytest

from authentication.keycloak import check_response


def _response(status_code: int) -> httpx2.Response:
    return httpx2.Response(status_code, request=httpx2.Request("GET", "http://keycloak/test"))


def test_check_response_passes_on_success():
    check_response(_response(200))


def test_check_response_raises_on_error():
    with pytest.raises(httpx2.HTTPStatusError):
        check_response(_response(404))
