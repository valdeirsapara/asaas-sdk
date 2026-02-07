"""Installments resource."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Installments(Resource):
    """Manage installments (parcelamentos) in the Asaas platform.

    Endpoints:
        POST   /v3/installments/                    - Create credit card installment
        GET    /v3/installments                      - List installments
        GET    /v3/installments/:id                  - Retrieve installment
        DELETE /v3/installments/:id                  - Delete installment
        GET    /v3/installments/:id/payments         - List installment payments
        DELETE /v3/installments/:id/payments         - Cancel pending/overdue payments
        GET    /v3/installments/:id/paymentBook      - Get payment book
        POST   /v3/installments/:id/refund           - Refund installment
        PUT    /v3/installments/:id/splits           - Update installment splits
    """

    BASE_PATH = "/v3/installments"

    # ---- CRUD ----

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new credit card installment.

        Args:
            **kwargs: Installment fields. Commonly used keys include:
                customer, billingType, value, dueDate, installmentCount,
                installmentValue, description, externalReference,
                creditCard, creditCardHolderInfo, creditCardToken,
                remoteIp, etc.

        Returns:
            Created installment data.
        """
        return self._post(f"{self.BASE_PATH}/", json=kwargs)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> PaginatedResponse:
        """List installments (single page).

        Args:
            offset: Page offset.
            limit: Page size.

        Returns:
            Paginated response with installment data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        return self._list(self.BASE_PATH, params=params)

    def get(self, installment_id: str) -> dict[str, Any]:
        """Retrieve a single installment by ID.

        Args:
            installment_id: Installment identifier.

        Returns:
            Installment data.
        """
        return self._get(f"{self.BASE_PATH}/{installment_id}")

    def delete(self, installment_id: str) -> dict[str, Any]:
        """Delete an installment.

        Args:
            installment_id: Installment identifier.

        Returns:
            Deletion confirmation.
        """
        return self._delete(f"{self.BASE_PATH}/{installment_id}")

    # ---- Payments ----

    def list_payments(
        self,
        installment_id: str,
        *,
        status: str | None = None,
    ) -> dict[str, Any]:
        """List payments for an installment.

        Args:
            installment_id: Installment identifier.
            status: Filter by payment status.

        Returns:
            Payment data for the installment.
        """
        params: dict[str, Any] = {}
        _set(params, "status", status)
        return self._get(f"{self.BASE_PATH}/{installment_id}/payments", params=params)

    def cancel_payments(self, installment_id: str) -> dict[str, Any]:
        """Cancel all pending or overdue payments for an installment.

        Args:
            installment_id: Installment identifier.

        Returns:
            Cancellation confirmation.
        """
        return self._delete(f"{self.BASE_PATH}/{installment_id}/payments")

    # ---- Payment Book ----

    def get_payment_book(
        self,
        installment_id: str,
        *,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """Get the payment book (carne) for an installment.

        Args:
            installment_id: Installment identifier.
            sort: Field to sort by.
            order: Sort order (asc or desc).

        Returns:
            Payment book data.
        """
        params: dict[str, Any] = {}
        _set(params, "sort", sort)
        _set(params, "order", order)
        return self._get(f"{self.BASE_PATH}/{installment_id}/paymentBook", params=params)

    # ---- Refund ----

    def refund(self, installment_id: str, **kwargs: Any) -> dict[str, Any]:
        """Refund an installment.

        Args:
            installment_id: Installment identifier.
            **kwargs: Refund fields (e.g. value for partial refund,
                description, etc.).

        Returns:
            Refund data.
        """
        return self._post(f"{self.BASE_PATH}/{installment_id}/refund", json=kwargs)

    # ---- Splits ----

    def update_splits(
        self,
        installment_id: str,
        splits: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Update splits for an installment.

        Args:
            installment_id: Installment identifier.
            splits: List of split configuration dicts, each containing
                walletId, fixedValue or percentualValue, etc.

        Returns:
            Updated splits data.
        """
        payload: dict[str, Any] = {"splits": splits}
        return self._put(f"{self.BASE_PATH}/{installment_id}/splits", json=payload)
