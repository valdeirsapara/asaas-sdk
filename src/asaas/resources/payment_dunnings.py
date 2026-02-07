"""Payment dunnings resource."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class PaymentDunnings(Resource):
    """Manage payment dunnings (negativacoes) in the Asaas platform.

    Endpoints:
        POST /v3/paymentDunnings                                - Create dunning
        GET  /v3/paymentDunnings                                - List dunnings
        GET  /v3/paymentDunnings/:id                            - Retrieve dunning
        POST /v3/paymentDunnings/:id/cancel                     - Cancel dunning
        POST /v3/paymentDunnings/:id/documents                  - Resend documents
        GET  /v3/paymentDunnings/:id/history                    - List dunning history
        GET  /v3/paymentDunnings/:id/partialPayments            - List partial payments
        POST /v3/paymentDunnings/simulate                       - Simulate dunning
        GET  /v3/paymentDunnings/paymentsAvailableForDunning    - List available payments
    """

    BASE_PATH = "/v3/paymentDunnings"

    # ---- CRUD ----

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new payment dunning.

        Args:
            **kwargs: Dunning fields. Commonly used keys include:
                payment, type (CREDIT_BUREAU or PROTEST),
                description, etc.

        Returns:
            Created dunning data.
        """
        return self._post(self.BASE_PATH, json=kwargs)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        status: str | None = None,
        type: str | None = None,
        payment: str | None = None,
        request_start_date: str | None = None,
        request_end_date: str | None = None,
    ) -> PaginatedResponse:
        """List payment dunnings (single page).

        Args:
            offset: Page offset.
            limit: Page size.
            status: Filter by status.
            type: Filter by type (CREDIT_BUREAU or PROTEST).
            payment: Filter by payment ID.
            request_start_date: Filter by request start date (YYYY-MM-DD).
            request_end_date: Filter by request end date (YYYY-MM-DD).

        Returns:
            Paginated response with dunning data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "status", status)
        _set(params, "type", type)
        _set(params, "payment", payment)
        _set(params, "requestStartDate", request_start_date)
        _set(params, "requestEndDate", request_end_date)
        return self._list(self.BASE_PATH, params=params)

    def get(self, dunning_id: str) -> dict[str, Any]:
        """Retrieve a single payment dunning by ID.

        Args:
            dunning_id: Dunning identifier.

        Returns:
            Dunning data.
        """
        return self._get(f"{self.BASE_PATH}/{dunning_id}")

    # ---- Actions ----

    def cancel(self, dunning_id: str) -> dict[str, Any]:
        """Cancel a payment dunning.

        Args:
            dunning_id: Dunning identifier.

        Returns:
            Cancellation confirmation.
        """
        return self._post(f"{self.BASE_PATH}/{dunning_id}/cancel", json={})

    def resend_documents(self, dunning_id: str, **kwargs: Any) -> dict[str, Any]:
        """Resend documents for a payment dunning.

        Args:
            dunning_id: Dunning identifier.
            **kwargs: Document fields (e.g. documents list, etc.).

        Returns:
            Resend confirmation data.
        """
        return self._post(f"{self.BASE_PATH}/{dunning_id}/documents", json=kwargs)

    # ---- History & Partial Payments ----

    def list_history(
        self,
        dunning_id: str,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> PaginatedResponse:
        """List history entries for a payment dunning.

        Args:
            dunning_id: Dunning identifier.
            offset: Page offset.
            limit: Page size.

        Returns:
            Paginated response with dunning history entries.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        return self._list(f"{self.BASE_PATH}/{dunning_id}/history", params=params)

    def list_partial_payments(
        self,
        dunning_id: str,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> PaginatedResponse:
        """List partial payments for a payment dunning.

        Args:
            dunning_id: Dunning identifier.
            offset: Page offset.
            limit: Page size.

        Returns:
            Paginated response with partial payment data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        return self._list(f"{self.BASE_PATH}/{dunning_id}/partialPayments", params=params)

    # ---- Simulation & Available Payments ----

    def simulate(self, payment: str) -> dict[str, Any]:
        """Simulate a payment dunning.

        Args:
            payment: Payment ID to simulate dunning for.

        Returns:
            Simulation result data.
        """
        payload: dict[str, Any] = {"payment": payment}
        return self._post(f"{self.BASE_PATH}/simulate", json=payload)

    def list_available_payments(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> PaginatedResponse:
        """List payments available for dunning.

        Args:
            offset: Page offset.
            limit: Page size.

        Returns:
            Paginated response with payments available for dunning.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        return self._list(f"{self.BASE_PATH}/paymentsAvailableForDunning", params=params)
