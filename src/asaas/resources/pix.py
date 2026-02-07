"""PIX resource -- 23 endpoints for PIX operations."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Pix(Resource):
    """Manage PIX operations in the Asaas platform."""

    BASE_PATH = "/v3/pix"

    # ---- Address Keys ----

    def create_address_key(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new PIX address key.

        Args:
            **kwargs: Key data (type, etc.).

        Returns:
            Created address key data.
        """
        return self._post(f"{self.BASE_PATH}/addressKeys", json=kwargs)

    def list_address_keys(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        status: str | None = None,
        status_list: str | None = None,
    ) -> PaginatedResponse:
        """List PIX address keys."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "status", status)
        _set(params, "statusList", status_list)
        return self._list(f"{self.BASE_PATH}/addressKeys", params=params)

    def get_address_key(self, key_id: str) -> dict[str, Any]:
        """Retrieve a single PIX address key."""
        return self._get(f"{self.BASE_PATH}/addressKeys/{key_id}")

    def delete_address_key(self, key_id: str) -> dict[str, Any]:
        """Remove a PIX address key."""
        return self._delete(f"{self.BASE_PATH}/addressKeys/{key_id}")

    # ---- QR Codes ----

    def create_static_qr_code(self, **kwargs: Any) -> dict[str, Any]:
        """Create a static PIX QR Code.

        Args:
            **kwargs: QR code configuration (addressKey, description, value, etc.).

        Returns:
            Created QR code data.
        """
        return self._post(f"{self.BASE_PATH}/qrCodes/static", json=kwargs)

    def delete_static_qr_code(self, qr_code_id: str) -> dict[str, Any]:
        """Delete a static PIX QR Code."""
        return self._delete(f"{self.BASE_PATH}/qrCodes/static/{qr_code_id}")

    def pay_qr_code(self, **kwargs: Any) -> dict[str, Any]:
        """Pay a PIX QR Code.

        Args:
            **kwargs: Payment data (qrCode, value, description, scheduleDate, etc.).

        Returns:
            Transaction data.
        """
        return self._post(f"{self.BASE_PATH}/qrCodes/pay", json=kwargs)

    def decode_qr_code(self, **kwargs: Any) -> dict[str, Any]:
        """Decode a PIX QR Code for payment.

        Args:
            **kwargs: QR code payload to decode.

        Returns:
            Decoded QR code data.
        """
        return self._post(f"{self.BASE_PATH}/qrCodes/decode", json=kwargs)

    # ---- Token Bucket ----

    def get_token_bucket(self) -> dict[str, Any]:
        """Check available tokens in the address key rate limit bucket."""
        return self._get(f"{self.BASE_PATH}/tokenBucket/addressKey")

    # ---- Transactions ----

    def list_transactions(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        status: str | None = None,
        type: str | None = None,
        end_to_end_identifier: str | None = None,
    ) -> PaginatedResponse:
        """List PIX transactions."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "status", status)
        _set(params, "type", type)
        _set(params, "endToEndIdentifier", end_to_end_identifier)
        return self._list(f"{self.BASE_PATH}/transactions", params=params)

    def get_transaction(self, transaction_id: str) -> dict[str, Any]:
        """Retrieve a single PIX transaction."""
        return self._get(f"{self.BASE_PATH}/transactions/{transaction_id}")

    def cancel_transaction(self, transaction_id: str) -> dict[str, Any]:
        """Cancel a scheduled PIX transaction."""
        return self._post(f"{self.BASE_PATH}/transactions/{transaction_id}/cancel", json={})

    # ---- Recurring Transactions ----

    def list_recurrings(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        status: str | None = None,
        value: float | None = None,
        search_text: str | None = None,
    ) -> PaginatedResponse:
        """List PIX recurring transactions."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "status", status)
        _set(params, "value", value)
        _set(params, "searchText", search_text)
        return self._list(f"{self.BASE_PATH}/transactions/recurrings", params=params)

    def get_recurring(self, recurring_id: str) -> dict[str, Any]:
        """Retrieve a single PIX recurring transaction."""
        return self._get(f"{self.BASE_PATH}/transactions/recurrings/{recurring_id}")

    def cancel_recurring(self, recurring_id: str) -> dict[str, Any]:
        """Cancel a PIX recurring transaction."""
        return self._post(f"{self.BASE_PATH}/transactions/recurrings/{recurring_id}/cancel", json={})

    def list_recurring_items(
        self,
        recurring_id: str,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> PaginatedResponse:
        """List items of a PIX recurring transaction."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        return self._list(f"{self.BASE_PATH}/transactions/recurrings/{recurring_id}/items", params=params)

    def cancel_recurring_item(self, item_id: str) -> dict[str, Any]:
        """Cancel a single item in a PIX recurring transaction."""
        return self._post(f"{self.BASE_PATH}/transactions/recurrings/items/{item_id}/cancel", json={})

    # ---- Automatic PIX ----

    def create_automatic_authorization(self, **kwargs: Any) -> dict[str, Any]:
        """Create an automatic PIX authorization.

        Args:
            **kwargs: Authorization configuration.

        Returns:
            Created authorization data.
        """
        return self._post(f"{self.BASE_PATH}/automatic/authorizations", json=kwargs)

    def list_automatic_authorizations(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        status: str | None = None,
        customer_id: str | None = None,
    ) -> PaginatedResponse:
        """List automatic PIX authorizations."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "status", status)
        _set(params, "customerId", customer_id)
        return self._list(f"{self.BASE_PATH}/automatic/authorizations", params=params)

    def get_automatic_authorization(self, authorization_id: str) -> dict[str, Any]:
        """Retrieve a single automatic PIX authorization."""
        return self._get(f"{self.BASE_PATH}/automatic/authorizations/{authorization_id}")

    def cancel_automatic_authorization(self, authorization_id: str) -> dict[str, Any]:
        """Cancel an automatic PIX authorization."""
        return self._delete(f"{self.BASE_PATH}/automatic/authorizations/{authorization_id}")

    def get_payment_instruction(self, instruction_id: str) -> dict[str, Any]:
        """Retrieve a single automatic PIX payment instruction."""
        return self._get(f"{self.BASE_PATH}/automatic/paymentInstructions/{instruction_id}")

    def list_payment_instructions(self, *, payment_id: str | None = None) -> dict[str, Any]:
        """List automatic PIX payment instructions."""
        params: dict[str, Any] = {}
        _set(params, "paymentId", payment_id)
        return self._get(f"{self.BASE_PATH}/automatic/paymentInstructions", params=params)
