"""Sandbox resource -- only available in sandbox environment."""

from __future__ import annotations

from typing import Any

from .base import Resource


class Sandbox(Resource):
    """Sandbox-only utilities for testing payments."""

    BASE_PATH = "/v3/sandbox/payment"

    def confirm_payment(self, payment_id: str) -> dict[str, Any]:
        """(Sandbox only) Confirm/simulate a payment.

        Args:
            payment_id: Payment identifier.

        Returns:
            Confirmed payment data.
        """
        return self._post(f"{self.BASE_PATH}/{payment_id}/confirm", json={})

    def force_overdue(self, payment_id: str) -> dict[str, Any]:
        """(Sandbox only) Force a payment to become overdue.

        Args:
            payment_id: Payment identifier.

        Returns:
            Payment data with overdue status.
        """
        return self._post(f"{self.BASE_PATH}/{payment_id}/overdue", json={})
