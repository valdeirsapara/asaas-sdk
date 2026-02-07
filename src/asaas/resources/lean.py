"""Lean payments resource -- summarized payment data."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Lean(Resource):
    """Manage lean (summarized) payments in the Asaas platform.

    The lean endpoints return summarized payment data with fewer fields
    compared to the standard payments resource, providing faster responses.

    Endpoints:
        POST   /v3/lean/payments/                                - Create payment
        GET    /v3/lean/payments                                  - List payments
        GET    /v3/lean/payments/:id                              - Retrieve payment
        PUT    /v3/lean/payments/:id                              - Update payment
        DELETE /v3/lean/payments/:id                              - Delete payment
        POST   /v3/lean/payments/:id/restore                     - Restore payment
        POST   /v3/lean/payments/:id/refund                      - Refund payment
        POST   /v3/lean/payments/:id/captureAuthorizedPayment    - Capture authorized
        POST   /v3/lean/payments/:id/receiveInCash               - Receive in cash
        POST   /v3/lean/payments/:id/undoReceivedInCash          - Undo received in cash
    """

    BASE_PATH = "/v3/lean/payments"

    # ---- CRUD ----

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new lean payment.

        Args:
            **kwargs: Payment fields. Commonly used keys include:
                customer, billingType, value, dueDate, description,
                externalReference, installmentCount, installmentValue,
                discount, interest, fine, postalService, split,
                callback, creditCard, creditCardHolderInfo,
                creditCardToken, authorizedOnly, remoteIp, etc.

        Returns:
            Created lean payment data.
        """
        return self._post(f"{self.BASE_PATH}/", json=kwargs)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        customer: str | None = None,
        customer_group_name: str | None = None,
        billing_type: str | None = None,
        status: str | None = None,
        subscription: str | None = None,
        installment: str | None = None,
        external_reference: str | None = None,
        payment_date: str | None = None,
        anticipated: bool | None = None,
        date_created_ge: str | None = None,
        date_created_le: str | None = None,
        payment_date_ge: str | None = None,
        payment_date_le: str | None = None,
        estimated_credit_date_ge: str | None = None,
        estimated_credit_date_le: str | None = None,
        due_date_ge: str | None = None,
        due_date_le: str | None = None,
        user: str | None = None,
    ) -> PaginatedResponse:
        """List lean payments (single page).

        Args:
            offset: Page offset.
            limit: Page size.
            customer: Filter by customer ID.
            customer_group_name: Filter by customer group name.
            billing_type: Filter by billing type (BOLETO, CREDIT_CARD, PIX, etc.).
            status: Filter by status.
            subscription: Filter by subscription ID.
            installment: Filter by installment ID.
            external_reference: Filter by external reference.
            payment_date: Filter by exact payment date (YYYY-MM-DD).
            anticipated: Filter by anticipated status.
            date_created_ge: Filter by creation date >= (YYYY-MM-DD).
            date_created_le: Filter by creation date <= (YYYY-MM-DD).
            payment_date_ge: Filter by payment date >= (YYYY-MM-DD).
            payment_date_le: Filter by payment date <= (YYYY-MM-DD).
            estimated_credit_date_ge: Filter by estimated credit date >= (YYYY-MM-DD).
            estimated_credit_date_le: Filter by estimated credit date <= (YYYY-MM-DD).
            due_date_ge: Filter by due date >= (YYYY-MM-DD).
            due_date_le: Filter by due date <= (YYYY-MM-DD).
            user: Filter by user.

        Returns:
            Paginated response with lean payment data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "customer", customer)
        _set(params, "customerGroupName", customer_group_name)
        _set(params, "billingType", billing_type)
        _set(params, "status", status)
        _set(params, "subscription", subscription)
        _set(params, "installment", installment)
        _set(params, "externalReference", external_reference)
        _set(params, "paymentDate", payment_date)
        _set(params, "anticipated", anticipated)
        _set(params, "dateCreated[ge]", date_created_ge)
        _set(params, "dateCreated[le]", date_created_le)
        _set(params, "paymentDate[ge]", payment_date_ge)
        _set(params, "paymentDate[le]", payment_date_le)
        _set(params, "estimatedCreditDate[ge]", estimated_credit_date_ge)
        _set(params, "estimatedCreditDate[le]", estimated_credit_date_le)
        _set(params, "dueDate[ge]", due_date_ge)
        _set(params, "dueDate[le]", due_date_le)
        _set(params, "user", user)
        return self._list(self.BASE_PATH, params=params)

    def get(self, payment_id: str) -> dict[str, Any]:
        """Retrieve a single lean payment by ID.

        Args:
            payment_id: Payment identifier.

        Returns:
            Lean payment data.
        """
        return self._get(f"{self.BASE_PATH}/{payment_id}")

    def update(self, payment_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update an existing lean payment.

        Args:
            payment_id: Payment identifier.
            **kwargs: Fields to update (e.g. billingType, value,
                dueDate, description, externalReference, etc.).

        Returns:
            Updated lean payment data.
        """
        return self._put(f"{self.BASE_PATH}/{payment_id}", json=kwargs)

    def delete(self, payment_id: str) -> dict[str, Any]:
        """Delete a lean payment.

        Args:
            payment_id: Payment identifier.

        Returns:
            Deletion confirmation.
        """
        return self._delete(f"{self.BASE_PATH}/{payment_id}")

    # ---- Actions ----

    def restore(self, payment_id: str) -> dict[str, Any]:
        """Restore a previously deleted lean payment.

        Args:
            payment_id: Payment identifier.

        Returns:
            Restored lean payment data.
        """
        return self._post(f"{self.BASE_PATH}/{payment_id}/restore", json={})

    def refund(self, payment_id: str, **kwargs: Any) -> dict[str, Any]:
        """Refund a lean payment.

        Args:
            payment_id: Payment identifier.
            **kwargs: Refund fields (e.g. value for partial refund,
                description, etc.).

        Returns:
            Refund data.
        """
        return self._post(f"{self.BASE_PATH}/{payment_id}/refund", json=kwargs)

    def capture_authorized(self, payment_id: str) -> dict[str, Any]:
        """Capture a pre-authorized lean payment.

        Args:
            payment_id: Payment identifier.

        Returns:
            Captured lean payment data.
        """
        return self._post(f"{self.BASE_PATH}/{payment_id}/captureAuthorizedPayment", json={})

    def receive_in_cash(self, payment_id: str, **kwargs: Any) -> dict[str, Any]:
        """Confirm cash receipt for a lean payment.

        Args:
            payment_id: Payment identifier.
            **kwargs: Cash receipt fields (e.g. paymentDate, value,
                notificationDisabled).

        Returns:
            Lean payment data.
        """
        return self._post(f"{self.BASE_PATH}/{payment_id}/receiveInCash", json=kwargs)

    def undo_received_in_cash(self, payment_id: str) -> dict[str, Any]:
        """Undo a cash receipt confirmation for a lean payment.

        Args:
            payment_id: Payment identifier.

        Returns:
            Lean payment data.
        """
        return self._post(f"{self.BASE_PATH}/{payment_id}/undoReceivedInCash", json={})
