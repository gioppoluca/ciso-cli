from __future__ import annotations

from typing import Any, Optional

from ciso_cli.api.errors import CisoValidationError
from .base import BaseResource


class FoldersResource(BaseResource):
    PATH = "/api/folders/"

    def get_by_domain(self, domain: str) -> dict:
        domain = (domain or "").strip()
        if not domain:
            raise CisoValidationError("Empty domain/folder")

        items = self.list_all(self.PATH, search=domain)
        exact = [
            x for x in items
            if str(x.get("name", "")).strip() == domain or str(x.get("path", "")).strip() == domain
        ]
        chosen = self._require_one(exact or items, "folder", ["id", "name", "path"])
        return chosen

    def resolve_id(self, domain: str) -> str:
        folder = self.get_by_domain(domain)
        fid = folder.get("id")
        if not fid:
            raise CisoValidationError(f"Folder payload missing 'id' for domain='{domain}'")
        return str(fid)

    # NEW: payload builder for creation
    def build_create_payload(
        self,
        *,
        name: str,
        parent_id: str,
        description: Optional[str] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        name = (name or "").strip()
        parent_id = (parent_id or "").strip()

        if not name:
            raise CisoValidationError("Folder name is required")
        if not parent_id:
            raise CisoValidationError("parent_id is required (folder must be attached to a parent)")

        payload: dict[str, Any] = {
            "name": name,
            "parent": parent_id,  # UUID of parent folder
        }
        if description not in (None, ""):
            payload["description"] = str(description)

        payload.update(extra)
        return payload

    # NEW: create folder via POST
    def create(self, payload: dict[str, Any]) -> dict | None:
        return self.client.post(self.PATH, json=payload)
