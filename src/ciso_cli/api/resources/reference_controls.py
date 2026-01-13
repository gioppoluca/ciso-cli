from __future__ import annotations
from ciso_cli.api.errors import CisoValidationError
from .base import BaseResource


class ReferenceControlsResource(BaseResource):
    PATH = "/api/reference-controls/"

    def get_by_ref_id(self, ref_id: str) -> dict:
        ref_id = (ref_id or "").strip()
        if not ref_id:
            raise CisoValidationError("Empty ref_id")

        items = self.list_all(self.PATH, search=ref_id)
        exact = [x for x in items if str(x.get("ref_id", "")).strip() == ref_id]
        chosen = self._require_one(exact or items, "reference control", ["id", "ref_id", "name"])
        return chosen

    def resolve_id(self, ref_id: str) -> str:
        return str(self.get_by_ref_id(ref_id).get("id"))
