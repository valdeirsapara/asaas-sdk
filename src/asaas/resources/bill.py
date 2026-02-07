"""Bill resource -- manage bill payments (pagamentos de contas) in the Asaas platform."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Bill(Resource):
    """Manage bill payments (pagamentos de contas) in the Asaas platform.

    Endpoints:
        POST /v3/bill              - Create bill payment
        GET  /v3/bill              - List bill payments
        GET  /v3/bill/:id          - Retrieve bill payment
        POST /v3/bill/:id/cancel   - Cancel bill payment
        POST /v3/bill/simulate     - Simulate bill payment
    """

    BASE_PATH = "/v3/bill"

    # ---- CRUD ----

    def create(
        self,
        *,
        identification_field: str | None = None,
        schedule_date: str | None = None,
        description: str | None = None,
        discount: float | None = None,
        interest: float | None = None,
        fine: float | None = None,
        value: float | None = None,
        due_date: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a new bill payment.

        Args:
            identification_field: Barcode or typeable line (linha digitavel).
            schedule_date: Scheduled payment date (YYYY-MM-DD).
            description: Payment description.
            discount: Discount value.
            interest: Interest value.
            fine: Fine value.
            value: Payment value.
            due_date: Bill due date (YYYY-MM-DD).
            **kwargs: Additional bill payment fields.

        Returns:
            Created bill payment data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "identificationField", identification_field)
        _set(payload, "scheduleDate", schedule_date)
        _set(payload, "description", description)
        _set(payload, "discount", discount)
        _set(payload, "interest", interest)
        _set(payload, "fine", fine)
        _set(payload, "value", value)
        _set(payload, "dueDate", due_date)
        payload.update(kwargs)
        return self._post(self.BASE_PATH, json=payload)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> PaginatedResponse:
        """List bill payments (single page).

        Args:
            offset: Page offset.
            limit: Page size.

        Returns:
            Paginated response with bill payment data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        return self._list(self.BASE_PATH, params=params)

    def list_all(
        self,
        *,
        limit: int = 100,
        max_items: int | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all bill payments.

        Args:
            limit: Items per page.
            max_items: Max total items to return.

        Yields:
            Individual bill payment records.
        """
        return self._list_all(self.BASE_PATH, limit=limit, max_items=max_items)

    def get(self, bill_id: str) -> dict[str, Any]:
        """Retrieve a single bill payment by ID.

        Args:
            bill_id: Bill payment identifier.

        Returns:
            Bill payment data.
        """
        return self._get(f"{self.BASE_PATH}/{bill_id}")

    # ---- Actions ----

    def cancel(self, bill_id: str) -> dict[str, Any]:
        """Cancel a bill payment.

        Args:
            bill_id: Bill payment identifier.

        Returns:
            Cancellation confirmation.
        """
        return self._post(f"{self.BASE_PATH}/{bill_id}/cancel", json={})

    def simulate(
        self,
        *,
        identification_field: str | None = None,
        bar_code: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Simulate a bill payment without executing it.

        Args:
            identification_field: Barcode or typeable line (linha digitavel).
            bar_code: Bar code of the bill.
            **kwargs: Additional simulation fields.

        Returns:
            Simulation result data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "identificationField", identification_field)
        _set(payload, "barCode", bar_code)
        payload.update(kwargs)
        return self._post(f"{self.BASE_PATH}/simulate", json=payload)
