from __future__ import annotations
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
        return str(self.get_by_domain(domain).get("id"))
