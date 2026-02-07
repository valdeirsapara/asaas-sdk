"""Chargebacks resource -- manage chargebacks (estornos) in the Asaas platform."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Chargebacks(Resource):
    """Manage chargebacks (estornos) in the Asaas platform.

    Endpoints:
        GET  /v3/chargebacks/              - List chargebacks
        POST /v3/chargebacks/:id/dispute   - Create a dispute for a chargeback
    """

    BASE_PATH = "/v3/chargebacks"

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        credit_card_brand: str | None = None,
        status: str | None = None,
        origin_dispute_date_le: str | None = None,
        origin_dispute_date_ge: str | None = None,
        origin_transaction_date_le: str | None = None,
        origin_transaction_date_ge: str | None = None,
    ) -> PaginatedResponse:
        """List chargebacks (single page).

        Args:
            offset: Page offset.
            limit: Page size.
            credit_card_brand: Filter by credit card brand.
            status: Filter by chargeback status.
            origin_dispute_date_le: Filter by dispute date less than or equal (YYYY-MM-DD).
            origin_dispute_date_ge: Filter by dispute date greater than or equal (YYYY-MM-DD).
            origin_transaction_date_le: Filter by transaction date less than or equal (YYYY-MM-DD).
            origin_transaction_date_ge: Filter by transaction date greater than or equal (YYYY-MM-DD).

        Returns:
            Paginated response with chargeback data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "creditCardBrand", credit_card_brand)
        _set(params, "status", status)
        _set(params, "originDisputeDate[le]", origin_dispute_date_le)
        _set(params, "originDisputeDate[ge]", origin_dispute_date_ge)
        _set(params, "originTransactionDate[le]", origin_transaction_date_le)
        _set(params, "originTransactionDate[ge]", origin_transaction_date_ge)
        return self._list(f"{self.BASE_PATH}/", params=params)

    def list_all(
        self,
        *,
        credit_card_brand: str | None = None,
        status: str | None = None,
        origin_dispute_date_le: str | None = None,
        origin_dispute_date_ge: str | None = None,
        origin_transaction_date_le: str | None = None,
        origin_transaction_date_ge: str | None = None,
        limit: int = 100,
        max_items: int | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all chargebacks.

        Args:
            credit_card_brand: Filter by credit card brand.
            status: Filter by chargeback status.
            origin_dispute_date_le: Filter by dispute date less than or equal (YYYY-MM-DD).
            origin_dispute_date_ge: Filter by dispute date greater than or equal (YYYY-MM-DD).
            origin_transaction_date_le: Filter by transaction date less than or equal (YYYY-MM-DD).
            origin_transaction_date_ge: Filter by transaction date greater than or equal (YYYY-MM-DD).
            limit: Items per page.
            max_items: Max total items to return.

        Yields:
            Individual chargeback records.
        """
        params: dict[str, Any] = {}
        _set(params, "creditCardBrand", credit_card_brand)
        _set(params, "status", status)
        _set(params, "originDisputeDate[le]", origin_dispute_date_le)
        _set(params, "originDisputeDate[ge]", origin_dispute_date_ge)
        _set(params, "originTransactionDate[le]", origin_transaction_date_le)
        _set(params, "originTransactionDate[ge]", origin_transaction_date_ge)
        return self._list_all(f"{self.BASE_PATH}/", params=params, limit=limit, max_items=max_items)

    def create_dispute(
        self,
        chargeback_id: str,
        *,
        documents: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a dispute for a chargeback.

        Args:
            chargeback_id: Chargeback identifier.
            documents: List of dispute documents.
            **kwargs: Additional dispute fields.

        Returns:
            Created dispute data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "documents", documents)
        payload.update(kwargs)
        return self._post(f"{self.BASE_PATH}/{chargeback_id}/dispute", json=payload)
