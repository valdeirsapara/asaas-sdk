"""Escrow resource -- finish escrow operations in the Asaas platform."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Escrow(Resource):
    """Manage escrow operations in the Asaas platform.

    Endpoints:
        POST /v3/escrow/:id/finish - Finish an escrow
    """

    BASE_PATH = "/v3/escrow"

    def finish(
        self,
        escrow_id: str,
        *,
        status: str | None = None,
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Finish an escrow process.

        Args:
            escrow_id: Escrow identifier.
            status: Final escrow status.
            description: Description for the finish operation.
            **kwargs: Additional fields for the finish operation.

        Returns:
            Finished escrow data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "status", status)
        _set(payload, "description", description)
        payload.update(kwargs)
        return self._post(f"{self.BASE_PATH}/{escrow_id}/finish", json=payload)
