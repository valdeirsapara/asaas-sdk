"""Credit Card resource -- credit card tokenization in the Asaas platform."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class CreditCard(Resource):
    """Manage credit card tokenization in the Asaas platform.

    Endpoints:
        POST /v3/creditCard/tokenizeCreditCard - Tokenize a credit card
    """

    BASE_PATH = "/v3/creditCard"

    def tokenize(
        self,
        customer: str,
        credit_card: dict[str, Any],
        credit_card_holder_info: dict[str, Any],
        remote_ip: str,
    ) -> dict[str, Any]:
        """Tokenize a credit card for future use.

        Args:
            customer: Customer ID that owns the credit card.
            credit_card: Credit card data dict containing:
                holderName, number, expiryMonth, expiryYear, ccv.
            credit_card_holder_info: Card holder info dict containing:
                name, email, cpfCnpj, postalCode, addressNumber, phone.
            remote_ip: Customer's remote IP address.

        Returns:
            Tokenized credit card data including the credit card token.
        """
        payload: dict[str, Any] = {
            "customer": customer,
            "creditCard": credit_card,
            "creditCardHolderInfo": credit_card_holder_info,
            "remoteIp": remote_ip,
        }
        return self._post(f"{self.BASE_PATH}/tokenizeCreditCard", json=payload)
