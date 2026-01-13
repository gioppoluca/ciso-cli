import respx
import httpx
from typer.testing import CliRunner

from ciso_cli.main import app

runner = CliRunner()


@respx.mock
def test_cli_build_info_ok(monkeypatch):
    # config via env
    monkeypatch.setenv("CISO_URL", "https://example.test")
    monkeypatch.setenv("CISO_API_TOKEN", "x" * 20)
    monkeypatch.setenv("CISO_TIMEOUT", "10")
    monkeypatch.setenv("CISO_VERIFY_TLS", "true")

    # mock endpoint
    respx.get("https://example.test/api/build/").mock(
        return_value=httpx.Response(200, content=b"")
    )

    result = runner.invoke(app, ["build", "info"])
    assert result.exit_code == 0
    assert "Connected to CISO Assistant API" in result.stdout
