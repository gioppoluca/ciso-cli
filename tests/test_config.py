import os
import pytest
from pydantic import ValidationError

from ciso_cli.config import get_settings


def test_settings_ok_from_env(monkeypatch):
    monkeypatch.setenv("CISO_URL", "http://localhost:8000")
    monkeypatch.setenv("CISO_API_TOKEN", "x" * 20)
    monkeypatch.setenv("CISO_TIMEOUT", "12")
    monkeypatch.setenv("CISO_VERIFY_TLS", "true")

    s = get_settings()
    assert str(s.url) == "http://localhost:8000/"
    assert s.api_token == "x" * 20
    assert s.timeout == 12
    assert s.verify_tls is True


def test_settings_missing_token_raises(monkeypatch):
    monkeypatch.setenv("CISO_ENV_FILE", "")  # disable .env reading
    monkeypatch.setenv("CISO_URL", "http://localhost:8000")
    monkeypatch.delenv("CISO_API_TOKEN", raising=False)

    with pytest.raises(ValidationError):
        get_settings()
