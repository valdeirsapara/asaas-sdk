"""Payments resource -- the largest resource in the Asaas API (31 endpoints)."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Payments(Resource):
    """Manage payments (cobranças) in the Asaas platform."""

    BASE_PATH = "/v3/payments"

    # ---- CRUD ----

    def create(
        self,
        customer: str,
        billing_type: str,
        value: float,
        due_date: str,
        *,
        description: str | None = None,
        external_reference: str | None = None,
        installment_count: int | None = None,
        installment_value: float | None = None,
        discount: dict[str, Any] | None = None,
        interest: dict[str, Any] | None = None,
        fine: dict[str, Any] | None = None,
        postal_service: bool | None = None,
        split: list[dict[str, Any]] | None = None,
        callback: dict[str, Any] | None = None,
        credit_card: dict[str, Any] | None = None,
        credit_card_holder_info: dict[str, Any] | None = None,
        credit_card_token: str | None = None,
        authorized_only: bool | None = None,
        remote_ip: str | None = None,
    ) -> dict[str, Any]:
        """Create a new payment (charge).

        Args:
            customer: Customer ID.
            billing_type: Payment method: BOLETO, CREDIT_CARD, UNDEFINED, PIX, etc.
            value: Payment amount.
            due_date: Due date in YYYY-MM-DD format.
            description: Payment description.
            external_reference: External reference ID.
            installment_count: Number of installments.
            installment_value: Value per installment.
            discount: Discount settings dict.
            interest: Interest settings dict.
            fine: Fine settings dict.
            postal_service: Send via postal service.
            split: Split payment configuration list.
            callback: Callback URLs dict.
            credit_card: Credit card data dict.
            credit_card_holder_info: Card holder info dict.
            credit_card_token: Tokenized credit card.
            authorized_only: Authorize only without capturing.
            remote_ip: Customer remote IP for credit card.

        Returns:
            Created payment data.
        """
        payload: dict[str, Any] = {
            "customer": customer,
            "billingType": billing_type,
            "value": value,
            "dueDate": due_date,
        }
        _set(payload, "description", description)
        _set(payload, "externalReference", external_reference)
        _set(payload, "installmentCount", installment_count)
        _set(payload, "installmentValue", installment_value)
        _set(payload, "discount", discount)
        _set(payload, "interest", interest)
        _set(payload, "fine", fine)
        _set(payload, "postalService", postal_service)
        _set(payload, "split", split)
        _set(payload, "callback", callback)
        _set(payload, "creditCard", credit_card)
        _set(payload, "creditCardHolderInfo", credit_card_holder_info)
        _set(payload, "creditCardToken", credit_card_token)
        _set(payload, "authorizedOnly", authorized_only)
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
        """List payments (single page).

        Returns:
            Paginated response with payment data.
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

    def list_all(
        self,
        *,
        customer: str | None = None,
        billing_type: str | None = None,
        status: str | None = None,
        subscription: str | None = None,
        external_reference: str | None = None,
        limit: int = 100,
        max_items: int | None = None,
        **kwargs: Any,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all payments.

        Yields:
            Individual payment records.
        """
        params: dict[str, Any] = {}
        _set(params, "customer", customer)
        _set(params, "billingType", billing_type)
        _set(params, "status", status)
        _set(params, "subscription", subscription)
        _set(params, "externalReference", external_reference)
        params.update(kwargs)
        return self._list_all(self.BASE_PATH, params=params, limit=limit, max_items=max_items)

    def get(self, payment_id: str) -> dict[str, Any]:
        """Retrieve a single payment by ID."""
        return self._get(f"{self.BASE_PATH}/{payment_id}")

    def update(self, payment_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update an existing payment.

        Args:
            payment_id: Payment identifier.
            **kwargs: Fields to update (snake_case supported):
                billing_type, value, due_date, description, external_reference, etc.

        Returns:
            Updated payment data.
        """
        payload = _snake_to_camel_payload(kwargs)
        return self._put(f"{self.BASE_PATH}/{payment_id}", json=payload)

    def delete(self, payment_id: str) -> dict[str, Any]:
        """Delete a payment."""
        return self._delete(f"{self.BASE_PATH}/{payment_id}")

    # ---- Actions ----

    def restore(self, payment_id: str) -> dict[str, Any]:
        """Restore a previously deleted payment."""
        return self._post(f"{self.BASE_PATH}/{payment_id}/restore", json={})

    def refund(self, payment_id: str, *, value: float | None = None, description: str | None = None) -> dict[str, Any]:
        """Refund a payment.

        Args:
            payment_id: Payment identifier.
            value: Partial refund value. None for full refund.
            description: Refund description.

        Returns:
            Refund data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "value", value)
        _set(payload, "description", description)
        return self._post(f"{self.BASE_PATH}/{payment_id}/refund", json=payload)

    def refund_bank_slip(self, payment_id: str) -> dict[str, Any]:
        """Refund a bank slip (boleto) payment."""
        return self._post(f"{self.BASE_PATH}/{payment_id}/bankSlip/refund", json={})

    def capture_authorized(self, payment_id: str) -> dict[str, Any]:
        """Capture a pre-authorized credit card payment."""
        return self._post(f"{self.BASE_PATH}/{payment_id}/captureAuthorizedPayment", json={})

    def pay_with_credit_card(
        self,
        payment_id: str,
        *,
        credit_card: dict[str, Any] | None = None,
        credit_card_holder_info: dict[str, Any] | None = None,
        credit_card_token: str | None = None,
    ) -> dict[str, Any]:
        """Pay a payment with credit card.

        Args:
            payment_id: Payment identifier.
            credit_card: Credit card data dict.
            credit_card_holder_info: Card holder info dict.
            credit_card_token: Tokenized credit card.

        Returns:
            Payment data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "creditCard", credit_card)
        _set(payload, "creditCardHolderInfo", credit_card_holder_info)
        _set(payload, "creditCardToken", credit_card_token)
        return self._post(f"{self.BASE_PATH}/{payment_id}/payWithCreditCard", json=payload)

    def receive_in_cash(self, payment_id: str, *, payment_date: str, value: float, notification_disabled: bool | None = None) -> dict[str, Any]:
        """Confirm cash receipt for a payment.

        Args:
            payment_id: Payment identifier.
            payment_date: Date of the cash payment (YYYY-MM-DD).
            value: Received amount.
            notification_disabled: Disable notification for this action.

        Returns:
            Payment data.
        """
        payload: dict[str, Any] = {"paymentDate": payment_date, "value": value}
        _set(payload, "notificationDisabled", notification_disabled)
        return self._post(f"{self.BASE_PATH}/{payment_id}/receiveInCash", json=payload)

    def undo_received_in_cash(self, payment_id: str) -> dict[str, Any]:
        """Undo a cash receipt confirmation."""
        return self._post(f"{self.BASE_PATH}/{payment_id}/undoReceivedInCash", json={})

    def simulate(self, **kwargs: Any) -> dict[str, Any]:
        """Simulate a sale."""
        return self._post(f"{self.BASE_PATH}/simulate", json=kwargs)

    # ---- Info ----

    def get_status(self, payment_id: str) -> dict[str, Any]:
        """Get the current status of a payment."""
        return self._get(f"{self.BASE_PATH}/{payment_id}/status")

    def get_billing_info(self, payment_id: str) -> dict[str, Any]:
        """Get payment billing information (boleto line, pix code, etc)."""
        return self._get(f"{self.BASE_PATH}/{payment_id}/billingInfo")

    def get_viewing_info(self, payment_id: str) -> dict[str, Any]:
        """Get viewing information for a payment."""
        return self._get(f"{self.BASE_PATH}/{payment_id}/viewingInfo")

    def get_identification_field(self, payment_id: str) -> dict[str, Any]:
        """Get the boleto identification field (linha digitável)."""
        return self._get(f"{self.BASE_PATH}/{payment_id}/identificationField")

    def get_pix_qr_code(self, payment_id: str) -> dict[str, Any]:
        """Get PIX QR Code for a payment."""
        return self._get(f"{self.BASE_PATH}/{payment_id}/pixQrCode")

    def get_limits(self) -> dict[str, Any]:
        """Retrieve payment limits for the account."""
        return self._get(f"{self.BASE_PATH}/limits")

    # ---- Refunds ----

    def list_refunds(self, payment_id: str) -> dict[str, Any]:
        """List refunds for a payment."""
        return self._get(f"{self.BASE_PATH}/{payment_id}/refunds")

    # ---- Chargeback ----

    def get_chargeback(self, payment_id: str) -> dict[str, Any]:
        """Retrieve chargeback data for a payment."""
        return self._get(f"{self.BASE_PATH}/{payment_id}/chargeback")

    # ---- Escrow ----

    def get_escrow(self, payment_id: str) -> dict[str, Any]:
        """Retrieve escrow data for a payment."""
        return self._get(f"{self.BASE_PATH}/{payment_id}/escrow")

    # ---- Documents ----

    def upload_document(self, payment_id: str, *, file: Any, available_after_payment: bool | None = None, type: str | None = None) -> dict[str, Any]:
        """Upload a document to a payment.

        Args:
            payment_id: Payment identifier.
            file: File-like object or tuple (filename, file_obj, content_type).
            available_after_payment: Whether the document is available after payment.
            type: Document type.

        Returns:
            Document data.
        """
        files = {"file": file}
        data: dict[str, Any] = {}
        _set(data, "availableAfterPayment", available_after_payment)
        _set(data, "type", type)
        return self._http.request("POST", f"{self.BASE_PATH}/{payment_id}/documents", files=files, data=data)

    def list_documents(self, payment_id: str) -> dict[str, Any]:
        """List documents attached to a payment."""
        return self._get(f"{self.BASE_PATH}/{payment_id}/documents")

    def get_document(self, payment_id: str, document_id: str) -> dict[str, Any]:
        """Retrieve a single document from a payment."""
        return self._get(f"{self.BASE_PATH}/{payment_id}/documents/{document_id}")

    def update_document(self, payment_id: str, document_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update document settings for a payment."""
        return self._put(f"{self.BASE_PATH}/{payment_id}/documents/{document_id}", json=kwargs)

    def delete_document(self, payment_id: str, document_id: str) -> dict[str, Any]:
        """Delete a document from a payment."""
        return self._delete(f"{self.BASE_PATH}/{payment_id}/documents/{document_id}")

    # ---- Splits ----

    def list_paid_splits(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        payment_id: str | None = None,
        status: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        """List paid splits."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "paymentId", payment_id)
        _set(params, "status", status)
        params.update(kwargs)
        return self._list(f"{self.BASE_PATH}/splits/paid", params=params)

    def get_paid_split(self, split_id: str) -> dict[str, Any]:
        """Retrieve a single paid split."""
        return self._get(f"{self.BASE_PATH}/splits/paid/{split_id}")

    def list_received_splits(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        payment_id: str | None = None,
        status: str | None = None,
        **kwargs: Any,
    ) -> PaginatedResponse:
        """List received splits."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "paymentId", payment_id)
        _set(params, "status", status)
        params.update(kwargs)
        return self._list(f"{self.BASE_PATH}/splits/received", params=params)

    def get_received_split(self, split_id: str) -> dict[str, Any]:
        """Retrieve a single received split."""
        return self._get(f"{self.BASE_PATH}/splits/received/{split_id}")


# -- Helpers --

_SNAKE_MAP = {
    "billing_type": "billingType",
    "due_date": "dueDate",
    "external_reference": "externalReference",
    "installment_count": "installmentCount",
    "installment_value": "installmentValue",
    "postal_service": "postalService",
    "credit_card": "creditCard",
    "credit_card_holder_info": "creditCardHolderInfo",
    "credit_card_token": "creditCardToken",
    "authorized_only": "authorizedOnly",
    "remote_ip": "remoteIp",
    "customer_group_name": "customerGroupName",
    "notification_disabled": "notificationDisabled",
    "payment_date": "paymentDate",
}


def _snake_to_camel_payload(kwargs: dict[str, Any]) -> dict[str, Any]:
    return {_SNAKE_MAP.get(k, k): v for k, v in kwargs.items() if v is not None}
