"""Subscriptions resource."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Subscriptions(Resource):
    """Manage subscriptions (assinaturas) in the Asaas platform."""

    BASE_PATH = "/v3/subscriptions"

    def create(
        self,
        customer: str,
        billing_type: str,
        value: float,
        next_due_date: str,
        cycle: str,
        *,
        description: str | None = None,
        external_reference: str | None = None,
        discount: dict[str, Any] | None = None,
        interest: dict[str, Any] | None = None,
        fine: dict[str, Any] | None = None,
        end_date: str | None = None,
        max_payments: int | None = None,
        split: list[dict[str, Any]] | None = None,
        callback: dict[str, Any] | None = None,
        credit_card: dict[str, Any] | None = None,
        credit_card_holder_info: dict[str, Any] | None = None,
        credit_card_token: str | None = None,
        remote_ip: str | None = None,
    ) -> dict[str, Any]:
        """Create a new subscription.

        Args:
            customer: Customer ID.
            billing_type: BOLETO, CREDIT_CARD, UNDEFINED, PIX.
            value: Subscription value.
            next_due_date: First due date (YYYY-MM-DD).
            cycle: WEEKLY, BIWEEKLY, MONTHLY, BIMONTHLY, QUARTERLY, SEMIANNUALLY, YEARLY.
            description: Description.
            external_reference: External reference.
            discount: Discount settings.
            interest: Interest settings.
            fine: Fine settings.
            end_date: Subscription end date (YYYY-MM-DD).
            max_payments: Max number of payments.
            split: Split configuration.
            callback: Callback URLs.
            credit_card: Credit card data.
            credit_card_holder_info: Card holder info.
            credit_card_token: Tokenized card.
            remote_ip: Customer IP.

        Returns:
            Created subscription data.
        """
        payload: dict[str, Any] = {
            "customer": customer,
            "billingType": billing_type,
            "value": value,
            "nextDueDate": next_due_date,
            "cycle": cycle,
        }
        _set(payload, "description", description)
        _set(payload, "externalReference", external_reference)
        _set(payload, "discount", discount)
        _set(payload, "interest", interest)
        _set(payload, "fine", fine)
        _set(payload, "endDate", end_date)
        _set(payload, "maxPayments", max_payments)
        _set(payload, "split", split)
        _set(payload, "callback", callback)
        _set(payload, "creditCard", credit_card)
        _set(payload, "creditCardHolderInfo", credit_card_holder_info)
        _set(payload, "creditCardToken", credit_card_token)
        _set(payload, "remoteIp", remote_ip)
        return self._post(self.BASE_PATH + "/", json=payload)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        customer: str | None = None,
        customer_group_name: str | None = None,
        billing_type: str | None = None,
        status: str | None = None,
        deleted_only: bool | None = None,
        include_deleted: bool | None = None,
        external_reference: str | None = None,
        order: str | None = None,
        sort: str | None = None,
    ) -> PaginatedResponse:
        """List subscriptions (single page)."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "customer", customer)
        _set(params, "customerGroupName", customer_group_name)
        _set(params, "billingType", billing_type)
        _set(params, "status", status)
        _set(params, "deletedOnly", deleted_only)
        _set(params, "includeDeleted", include_deleted)
        _set(params, "externalReference", external_reference)
        _set(params, "order", order)
        _set(params, "sort", sort)
        return self._list(self.BASE_PATH, params=params)

    def list_all(
        self,
        *,
        customer: str | None = None,
        billing_type: str | None = None,
        status: str | None = None,
        external_reference: str | None = None,
        limit: int = 100,
        max_items: int | None = None,
        **kwargs: Any,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all subscriptions."""
        params: dict[str, Any] = {}
        _set(params, "customer", customer)
        _set(params, "billingType", billing_type)
        _set(params, "status", status)
        _set(params, "externalReference", external_reference)
        params.update(kwargs)
        return self._list_all(self.BASE_PATH, params=params, limit=limit, max_items=max_items)

    def get(self, subscription_id: str) -> dict[str, Any]:
        """Retrieve a single subscription."""
        return self._get(f"{self.BASE_PATH}/{subscription_id}")

    def update(self, subscription_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update an existing subscription."""
        payload = {k: v for k, v in kwargs.items() if v is not None}
        return self._put(f"{self.BASE_PATH}/{subscription_id}", json=payload)

    def delete(self, subscription_id: str) -> dict[str, Any]:
        """Remove a subscription."""
        return self._delete(f"{self.BASE_PATH}/{subscription_id}")

    # ---- Payments ----

    def list_payments(self, subscription_id: str, *, status: str | None = None) -> dict[str, Any]:
        """List payments for a subscription."""
        params: dict[str, Any] = {}
        _set(params, "status", status)
        return self._get(f"{self.BASE_PATH}/{subscription_id}/payments", params=params)

    def get_payment_book(self, subscription_id: str, *, month: int | None = None, year: int | None = None, sort: str | None = None, order: str | None = None) -> dict[str, Any]:
        """Generate a payment book (carnê) for a subscription."""
        params: dict[str, Any] = {}
        _set(params, "month", month)
        _set(params, "year", year)
        _set(params, "sort", sort)
        _set(params, "order", order)
        return self._get(f"{self.BASE_PATH}/{subscription_id}/paymentBook", params=params)

    # ---- Credit Card ----

    def update_credit_card(self, subscription_id: str, *, credit_card: dict[str, Any], credit_card_holder_info: dict[str, Any], remote_ip: str | None = None) -> dict[str, Any]:
        """Update the credit card for a subscription without charging."""
        payload: dict[str, Any] = {
            "creditCard": credit_card,
            "creditCardHolderInfo": credit_card_holder_info,
        }
        _set(payload, "remoteIp", remote_ip)
        return self._put(f"{self.BASE_PATH}/{subscription_id}/creditCard", json=payload)

    # ---- Invoice Settings ----

    def create_invoice_settings(self, subscription_id: str, **kwargs: Any) -> dict[str, Any]:
        """Create invoice (nota fiscal) settings for a subscription."""
        return self._post(f"{self.BASE_PATH}/{subscription_id}/invoiceSettings", json=kwargs)

    def get_invoice_settings(self, subscription_id: str) -> dict[str, Any]:
        """Retrieve invoice settings for a subscription."""
        return self._get(f"{self.BASE_PATH}/{subscription_id}/invoiceSettings")

    def update_invoice_settings(self, subscription_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update invoice settings for a subscription."""
        return self._put(f"{self.BASE_PATH}/{subscription_id}/invoiceSettings", json=kwargs)

    def delete_invoice_settings(self, subscription_id: str) -> dict[str, Any]:
        """Remove invoice settings from a subscription."""
        return self._delete(f"{self.BASE_PATH}/{subscription_id}/invoiceSettings")

    # ---- Invoices ----

    def list_invoices(
        self,
        subscription_id: str,
        *,
        offset: int | None = None,
        limit: int | None = None,
        effective_date: str | None = None,
        external_reference: str | None = None,
        status: str | None = None,
        customer: str | None = None,
    ) -> PaginatedResponse:
        """List invoices for a subscription's payments."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "effectiveDate", effective_date)
        _set(params, "externalReference", external_reference)
        _set(params, "status", status)
        _set(params, "customer", customer)
        return self._list(f"{self.BASE_PATH}/{subscription_id}/invoices", params=params)
