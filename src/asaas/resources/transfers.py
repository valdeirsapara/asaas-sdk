"""Transfers resource."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Transfers(Resource):
    """Manage transfers in the Asaas platform."""

    BASE_PATH = "/v3/transfers"

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a transfer to an Asaas account.

        Args:
            **kwargs: Transfer data (value, bankAccount, operationType,
                      pixAddressKey, pixAddressKeyType, description, scheduleDate, etc.).

        Returns:
            Created transfer data.
        """
        return self._post(self.BASE_PATH + "/", json=kwargs)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        date_created_ge: str | None = None,
        date_created_le: str | None = None,
        transfer_date_ge: str | None = None,
        transfer_date_le: str | None = None,
        type: str | None = None,
    ) -> PaginatedResponse:
        """List transfers."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "dateCreated[ge]", date_created_ge)
        _set(params, "dateCreated[le]", date_created_le)
        _set(params, "transferDate[ge]", transfer_date_ge)
        _set(params, "transferDate[le]", transfer_date_le)
        _set(params, "type", type)
        return self._list(self.BASE_PATH, params=params)

    def list_all(
        self,
        *,
        type: str | None = None,
        limit: int = 100,
        max_items: int | None = None,
        **kwargs: Any,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all transfers."""
        params: dict[str, Any] = {}
        _set(params, "type", type)
        params.update(kwargs)
        return self._list_all(self.BASE_PATH, params=params, limit=limit, max_items=max_items)

    def get(self, transfer_id: str) -> dict[str, Any]:
        """Retrieve a single transfer."""
        return self._get(f"{self.BASE_PATH}/{transfer_id}")

    def cancel(self, transfer_id: str) -> dict[str, Any]:
        """Cancel a transfer."""
        return self._delete(f"{self.BASE_PATH}/{transfer_id}/cancel")
