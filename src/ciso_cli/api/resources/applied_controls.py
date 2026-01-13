from __future__ import annotations
from typing import Any, Optional

from ciso_cli.api.errors import CisoValidationError
from .base import BaseResource


class AppliedControlsResource(BaseResource):
    PATH = "/api/applied-controls/"

    def build_create_payload(
        self,
        *,
        name: str,
        reference_control_id: str,
        folder_id: str,
        description: Optional[str] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        name = (name or "").strip()
        if not name:
            raise CisoValidationError("Applied control name is required")
        if not reference_control_id:
            raise CisoValidationError("reference_control_id is required")
        if not folder_id:
            raise CisoValidationError("folder_id is required")

        payload: dict[str, Any] = {
            "name": name,
            "reference_control": reference_control_id,  # UUID
            "folder": folder_id,                        # UUID
        }
        if description:
            payload["description"] = description

        # allow passing additional fields without hardcoding them here
        payload.update(extra)
        return payload

    def create(self, payload: dict[str, Any]) -> dict | None:
        return self.client.post(self.PATH, json=payload)
