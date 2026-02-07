"""Mobile phone recharges resource."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class MobilePhoneRecharges(Resource):
    """Manage mobile phone recharges (recargas de celular) in the Asaas platform.

    Endpoints:
        POST /v3/mobilePhoneRecharges                      - Request recharge
        GET  /v3/mobilePhoneRecharges                      - List recharges
        GET  /v3/mobilePhoneRecharges/:id                  - Retrieve recharge
        POST /v3/mobilePhoneRecharges/:id/cancel           - Cancel recharge
        GET  /v3/mobilePhoneRecharges/:phoneNumber/provider - Get provider
    """

    BASE_PATH = "/v3/mobilePhoneRecharges"

    # ---- CRUD ----

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Request a new mobile phone recharge.

        Args:
            **kwargs: Recharge fields. Commonly used keys include:
                phoneNumber, value, etc.

        Returns:
            Created recharge data.
        """
        return self._post(self.BASE_PATH, json=kwargs)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> PaginatedResponse:
        """List mobile phone recharges (single page).

        Args:
            offset: Page offset.
            limit: Page size.

        Returns:
            Paginated response with recharge data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        return self._list(self.BASE_PATH, params=params)

    def get(self, recharge_id: str) -> dict[str, Any]:
        """Retrieve a single recharge by ID.

        Args:
            recharge_id: Recharge identifier.

        Returns:
            Recharge data.
        """
        return self._get(f"{self.BASE_PATH}/{recharge_id}")

    # ---- Actions ----

    def cancel(self, recharge_id: str) -> dict[str, Any]:
        """Cancel a mobile phone recharge.

        Args:
            recharge_id: Recharge identifier.

        Returns:
            Cancellation confirmation.
        """
        return self._post(f"{self.BASE_PATH}/{recharge_id}/cancel", json={})

    # ---- Provider ----

    def get_provider(self, phone_number: str) -> dict[str, Any]:
        """Get the provider for a given phone number.

        Args:
            phone_number: Phone number to look up the provider for.

        Returns:
            Provider data for the phone number.
        """
        return self._get(f"{self.BASE_PATH}/{phone_number}/provider")
