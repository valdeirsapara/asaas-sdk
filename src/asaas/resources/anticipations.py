"""Anticipations resource -- manage payment anticipations in the Asaas platform."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Anticipations(Resource):
    """Manage anticipations (antecipacoes) in the Asaas platform.

    Endpoints:
        POST /v3/anticipations                - Request anticipation
        GET  /v3/anticipations                - List anticipations
        GET  /v3/anticipations/:id            - Retrieve anticipation
        POST /v3/anticipations/:id/cancel     - Cancel anticipation
        POST /v3/anticipations/simulate       - Simulate anticipation
        PUT  /v3/anticipations/configurations  - Update auto-anticipation config
        GET  /v3/anticipations/configurations  - Get auto-anticipation config
        GET  /v3/anticipations/limits          - Get anticipation limits
    """

    BASE_PATH = "/v3/anticipations"

    # ---- CRUD ----

    def create(
        self,
        *,
        payment: str | None = None,
        installment: str | None = None,
        anticipation_days: int | None = None,
        requestable_anticipation_total: float | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Request a new anticipation.

        Args:
            payment: Payment ID to anticipate.
            installment: Installment ID to anticipate.
            anticipation_days: Number of days to anticipate.
            requestable_anticipation_total: Total amount to anticipate.
            **kwargs: Additional anticipation fields.

        Returns:
            Created anticipation data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "payment", payment)
        _set(payload, "installment", installment)
        _set(payload, "anticipationDays", anticipation_days)
        _set(payload, "requestableAnticipationTotal", requestable_anticipation_total)
        payload.update(kwargs)
        return self._post(self.BASE_PATH, json=payload)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        payment: str | None = None,
        installment: str | None = None,
        status: str | None = None,
    ) -> PaginatedResponse:
        """List anticipations (single page).

        Args:
            offset: Page offset.
            limit: Page size.
            payment: Filter by payment ID.
            installment: Filter by installment ID.
            status: Filter by status (PENDING, APPROVED, DENIED, etc.).

        Returns:
            Paginated response with anticipation data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "payment", payment)
        _set(params, "installment", installment)
        _set(params, "status", status)
        return self._list(self.BASE_PATH, params=params)

    def list_all(
        self,
        *,
        payment: str | None = None,
        installment: str | None = None,
        status: str | None = None,
        limit: int = 100,
        max_items: int | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all anticipations.

        Args:
            payment: Filter by payment ID.
            installment: Filter by installment ID.
            status: Filter by status.
            limit: Items per page.
            max_items: Max total items to return.

        Yields:
            Individual anticipation records.
        """
        params: dict[str, Any] = {}
        _set(params, "payment", payment)
        _set(params, "installment", installment)
        _set(params, "status", status)
        return self._list_all(self.BASE_PATH, params=params, limit=limit, max_items=max_items)

    def get(self, anticipation_id: str) -> dict[str, Any]:
        """Retrieve a single anticipation by ID.

        Args:
            anticipation_id: Anticipation identifier.

        Returns:
            Anticipation data.
        """
        return self._get(f"{self.BASE_PATH}/{anticipation_id}")

    # ---- Actions ----

    def cancel(self, anticipation_id: str) -> dict[str, Any]:
        """Cancel a pending anticipation.

        Args:
            anticipation_id: Anticipation identifier.

        Returns:
            Cancellation confirmation.
        """
        return self._post(f"{self.BASE_PATH}/{anticipation_id}/cancel", json={})

    def simulate(
        self,
        *,
        payment: str | None = None,
        installment: str | None = None,
        anticipation_days: int | None = None,
        requestable_anticipation_total: float | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Simulate an anticipation without actually requesting it.

        Args:
            payment: Payment ID to simulate anticipation for.
            installment: Installment ID to simulate anticipation for.
            anticipation_days: Number of days to anticipate.
            requestable_anticipation_total: Total amount to anticipate.
            **kwargs: Additional simulation fields.

        Returns:
            Simulation result data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "payment", payment)
        _set(payload, "installment", installment)
        _set(payload, "anticipationDays", anticipation_days)
        _set(payload, "requestableAnticipationTotal", requestable_anticipation_total)
        payload.update(kwargs)
        return self._post(f"{self.BASE_PATH}/simulate", json=payload)

    # ---- Auto-anticipation Configuration ----

    def update_auto_config(
        self,
        *,
        enabled: bool | None = None,
        anticipation_days: int | None = None,
        billing_types: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update the automatic anticipation configuration.

        Args:
            enabled: Whether auto-anticipation is enabled.
            anticipation_days: Number of days for auto-anticipation.
            billing_types: Billing types eligible for auto-anticipation.
            **kwargs: Additional configuration fields.

        Returns:
            Updated configuration data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "enabled", enabled)
        _set(payload, "anticipationDays", anticipation_days)
        _set(payload, "billingTypes", billing_types)
        payload.update(kwargs)
        return self._put(f"{self.BASE_PATH}/configurations", json=payload)

    def get_auto_config(self) -> dict[str, Any]:
        """Retrieve the automatic anticipation configuration.

        Returns:
            Auto-anticipation configuration data.
        """
        return self._get(f"{self.BASE_PATH}/configurations")

    # ---- Limits ----

    def get_limits(self) -> dict[str, Any]:
        """Retrieve the anticipation limits for the account.

        Returns:
            Anticipation limits data.
        """
        return self._get(f"{self.BASE_PATH}/limits")
