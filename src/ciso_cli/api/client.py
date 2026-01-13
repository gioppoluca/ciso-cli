from __future__ import annotations

import httpx
from typing import Any, Optional
import atexit
from .errors import CisoApiError, CisoAuthError


class CisoApiClient:
    """
    Thin API client for CISO Assistant.

    Auth header required by OpenAPI:
      Authorization: Token <token>
    """

    def __init__(
        self,
        base_url: str,
        api_token: str,
        timeout: int = 30,
        verify_tls: bool = True,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            verify=verify_tls,
            headers={
                "Authorization": f"Token {self.api_token}",
                "Accept": "application/json",
            },
        )
        atexit.register(self.close)

    def close(self) -> None:
        self._client.close()

    def _handle_response(self, resp: httpx.Response) -> Any:
        if resp.status_code in (401, 403):
            raise CisoAuthError(f"Authentication failed ({resp.status_code}).")

        if resp.status_code >= 400:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            raise CisoApiError(f"API error {resp.status_code}: {detail}")

        if not resp.content:
            return None

        ctype = resp.headers.get("content-type", "")
        if "application/json" in ctype:
            return resp.json()

        return resp.text

    def get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        resp = self._client.get(path, params=params)
        return self._handle_response(resp)

    def post(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        resp = self._client.post(path, json=json)
        return self._handle_response(resp)

    def put(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        resp = self._client.put(path, json=json)
        return self._handle_response(resp)

    def delete(self, path: str) -> Any:
        resp = self._client.delete(path)
        return self._handle_response(resp)
