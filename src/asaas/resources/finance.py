"""Finance resource -- financial information and statistics in the Asaas platform."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Finance(Resource):
    """Retrieve financial information and statistics from the Asaas platform.

    Endpoints:
        GET /v3/finance/balance              - Get account balance
        GET /v3/finance/payment/statistics   - Get payment statistics
        GET /v3/finance/split/statistics     - Get split statistics
    """

    BASE_PATH = "/v3/finance"

    def get_balance(self) -> dict[str, Any]:
        """Retrieve the current account balance.

        Returns:
            Account balance data including totalBalance, currentBalance,
            and availableBalance.
        """
        return self._get(f"{self.BASE_PATH}/balance")

    def get_payment_statistics(
        self,
        *,
        customer: str | None = None,
        billing_type: str | None = None,
        status: str | None = None,
        anticipated: bool | None = None,
        date_created_ge: str | None = None,
        date_created_le: str | None = None,
        payment_date_ge: str | None = None,
        payment_date_le: str | None = None,
        estimated_credit_date_ge: str | None = None,
        estimated_credit_date_le: str | None = None,
        due_date_ge: str | None = None,
        due_date_le: str | None = None,
        external_reference: str | None = None,
    ) -> dict[str, Any]:
        """Retrieve payment statistics for the account.

        Args:
            customer: Filter by customer ID.
            billing_type: Filter by billing type (BOLETO, CREDIT_CARD, PIX, etc.).
            status: Filter by payment status.
            anticipated: Filter by anticipated payments.
            date_created_ge: Filter by creation date greater than or equal (YYYY-MM-DD).
            date_created_le: Filter by creation date less than or equal (YYYY-MM-DD).
            payment_date_ge: Filter by payment date greater than or equal (YYYY-MM-DD).
            payment_date_le: Filter by payment date less than or equal (YYYY-MM-DD).
            estimated_credit_date_ge: Filter by estimated credit date >= (YYYY-MM-DD).
            estimated_credit_date_le: Filter by estimated credit date <= (YYYY-MM-DD).
            due_date_ge: Filter by due date greater than or equal (YYYY-MM-DD).
            due_date_le: Filter by due date less than or equal (YYYY-MM-DD).
            external_reference: Filter by external reference.

        Returns:
            Payment statistics data.
        """
        params: dict[str, Any] = {}
        _set(params, "customer", customer)
        _set(params, "billingType", billing_type)
        _set(params, "status", status)
        _set(params, "anticipated", anticipated)
        _set(params, "dateCreated[ge]", date_created_ge)
        _set(params, "dateCreated[le]", date_created_le)
        _set(params, "paymentDate[ge]", payment_date_ge)
        _set(params, "paymentDate[le]", payment_date_le)
        _set(params, "estimatedCreditDate[ge]", estimated_credit_date_ge)
        _set(params, "estimatedCreditDate[le]", estimated_credit_date_le)
        _set(params, "dueDate[ge]", due_date_ge)
        _set(params, "dueDate[le]", due_date_le)
        _set(params, "externalReference", external_reference)
        return self._get(f"{self.BASE_PATH}/payment/statistics", params=params)

    def get_split_statistics(self) -> dict[str, Any]:
        """Retrieve split payment statistics for the account.

        Returns:
            Split statistics data.
        """
        return self._get(f"{self.BASE_PATH}/split/statistics")
