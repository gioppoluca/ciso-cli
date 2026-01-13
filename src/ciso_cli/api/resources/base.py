from __future__ import annotations
from typing import Any, Optional

from ciso_cli.api.client import CisoApiClient
from ciso_cli.api.errors import CisoValidationError


class BaseResource:
    def __init__(self, client: CisoApiClient):
        self.client = client

    def list_all(self, path: str, *, search: Optional[str] = None, limit: int = 200) -> list[dict]:
        """
        Generic DRF-style pagination helper.
        """
        offset = 0
        out: list[dict] = []

        while True:
            params: dict[str, Any] = {"limit": limit, "offset": offset}
            if search:
                params["search"] = search

            payload = self.client.get(path, params=params)

            if isinstance(payload, dict) and "results" in payload:
                results = payload.get("results") or []
                out.extend(results)
                count = int(payload.get("count") or 0)
                offset += limit
                if offset >= count:
                    break
            elif isinstance(payload, list):
                out.extend(payload)
                break
            else:
                break

        return out

    def _require_one(self, items: list[dict], what: str, key_fields: list[str]) -> dict:
        if not items:
            raise CisoValidationError(f"{what} not found")
        if len(items) > 1:
            preview = []
            for x in items[:5]:
                preview.append({k: x.get(k) for k in key_fields})
            raise CisoValidationError(f"Multiple {what} matched. Top matches: {preview}")
        return items[0]
