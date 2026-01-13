import pytest
import respx
import httpx

from ciso_cli.api.client import CisoApiClient
from ciso_cli.api.errors import CisoAuthError, CisoApiError


@respx.mock
def test_get_sets_token_header_and_handles_empty_body():
    route = respx.get("https://example.test/api/build/").mock(
        return_value=httpx.Response(200, content=b"")
    )

    client = CisoApiClient(base_url="https://example.test", api_token="abc1234567890")
    try:
        out = client.get("/api/build/")
        assert out is None
        assert route.called

        # verifica header Authorization: Token <token>
        req = route.calls[0].request
        assert req.headers["Authorization"] == "Token abc1234567890"
    finally:
        client.close()


@respx.mock
def test_401_raises_auth_error():
    respx.get("https://example.test/api/build/").mock(return_value=httpx.Response(401))

    client = CisoApiClient(base_url="https://example.test", api_token="badtoken____")
    try:
        with pytest.raises(CisoAuthError):
            client.get("/api/build/")
    finally:
        client.close()


@respx.mock
def test_500_raises_api_error_with_json_detail():
    respx.get("https://example.test/api/build/").mock(
        return_value=httpx.Response(500, json={"detail": "boom"})
    )

    client = CisoApiClient(base_url="https://example.test", api_token="abc1234567890")
    try:
        with pytest.raises(CisoApiError) as e:
            client.get("/api/build/")
        assert "500" in str(e.value)
        assert "boom" in str(e.value)
    finally:
        client.close()
