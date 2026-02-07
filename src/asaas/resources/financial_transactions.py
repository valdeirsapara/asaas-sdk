"""Financial Transactions resource -- list financial transactions (extrato) in the Asaas platform."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class FinancialTransactions(Resource):
    """List financial transactions (extrato) in the Asaas platform.

    Endpoints:
        GET /v3/financialTransactions - List financial transactions
    """

    BASE_PATH = "/v3/financialTransactions"

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        start_date: str | None = None,
        finish_date: str | None = None,
        order: str | None = None,
    ) -> PaginatedResponse:
        """List financial transactions (single page).

        Args:
            offset: Page offset.
            limit: Page size.
            start_date: Filter by start date (YYYY-MM-DD).
            finish_date: Filter by end date (YYYY-MM-DD).
            order: Sort order (asc or desc).

        Returns:
            Paginated response with financial transaction data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "startDate", start_date)
        _set(params, "finishDate", finish_date)
        _set(params, "order", order)
        return self._list(self.BASE_PATH, params=params)

    def list_all(
        self,
        *,
        start_date: str | None = None,
        finish_date: str | None = None,
        order: str | None = None,
        limit: int = 100,
        max_items: int | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all financial transactions.

        Args:
            start_date: Filter by start date (YYYY-MM-DD).
            finish_date: Filter by end date (YYYY-MM-DD).
            order: Sort order (asc or desc).
            limit: Items per page.
            max_items: Max total items to return.

        Yields:
            Individual financial transaction records.
        """
        params: dict[str, Any] = {}
        _set(params, "startDate", start_date)
        _set(params, "finishDate", finish_date)
        _set(params, "order", order)
        return self._list_all(self.BASE_PATH, params=params, limit=limit, max_items=max_items)
