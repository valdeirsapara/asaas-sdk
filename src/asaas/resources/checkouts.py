"""Checkouts resource -- manage checkout links in the Asaas platform."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Checkouts(Resource):
    """Manage checkout links in the Asaas platform.

    Endpoints:
        POST /v3/checkouts              - Create checkout link
        POST /v3/checkouts/:id/cancel   - Cancel checkout link
    """

    BASE_PATH = "/v3/checkouts"

    def create(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        billing_type: str | None = None,
        charge_type: str | None = None,
        value: float | None = None,
        due_date: str | None = None,
        subscription_cycle: str | None = None,
        max_installment_count: int | None = None,
        notification_enabled: bool | None = None,
        end_date: str | None = None,
        callback: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a new checkout link.

        Args:
            name: Checkout name.
            description: Checkout description.
            billing_type: Payment method (BOLETO, CREDIT_CARD, UNDEFINED, PIX).
            charge_type: Charge type (DETACHED, RECURRENT, INSTALLMENT).
            value: Payment value.
            due_date: Due date (YYYY-MM-DD).
            subscription_cycle: Subscription cycle (WEEKLY, MONTHLY, etc.).
            max_installment_count: Maximum number of installments.
            notification_enabled: Whether to enable notifications.
            end_date: End date for the checkout (YYYY-MM-DD).
            callback: Callback URLs configuration.
            **kwargs: Additional checkout fields.

        Returns:
            Created checkout data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "name", name)
        _set(payload, "description", description)
        _set(payload, "billingType", billing_type)
        _set(payload, "chargeType", charge_type)
        _set(payload, "value", value)
        _set(payload, "dueDate", due_date)
        _set(payload, "subscriptionCycle", subscription_cycle)
        _set(payload, "maxInstallmentCount", max_installment_count)
        _set(payload, "notificationEnabled", notification_enabled)
        _set(payload, "endDate", end_date)
        _set(payload, "callback", callback)
        payload.update(kwargs)
        return self._post(self.BASE_PATH, json=payload)

    def cancel(self, checkout_id: str) -> dict[str, Any]:
        """Cancel an existing checkout link.

        Args:
            checkout_id: Checkout identifier.

        Returns:
            Cancellation confirmation.
        """
        return self._post(f"{self.BASE_PATH}/{checkout_id}/cancel", json={})
