"""Credit Bureau Report resource -- manage credit bureau reports (consultas Serasa) in the Asaas platform."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class CreditBureauReport(Resource):
    """Manage credit bureau reports (consultas Serasa) in the Asaas platform.

    Endpoints:
        POST /v3/creditBureauReport       - Run a credit bureau report
        GET  /v3/creditBureauReport       - List credit bureau reports
        GET  /v3/creditBureauReport/:id   - Retrieve a credit bureau report
    """

    BASE_PATH = "/v3/creditBureauReport"

    def create(
        self,
        *,
        customer: str | None = None,
        cpf_cnpj: str | None = None,
        state: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Run a new credit bureau report.

        Args:
            customer: Customer ID to run the report for.
            cpf_cnpj: CPF or CNPJ to query (numbers only).
            state: State abbreviation (UF) for the query.
            **kwargs: Additional report fields.

        Returns:
            Created credit bureau report data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "customer", customer)
        _set(payload, "cpfCnpj", cpf_cnpj)
        _set(payload, "state", state)
        payload.update(kwargs)
        return self._post(self.BASE_PATH, json=payload)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> PaginatedResponse:
        """List credit bureau reports (single page).

        Args:
            offset: Page offset.
            limit: Page size.
            start_date: Filter by start date (YYYY-MM-DD).
            end_date: Filter by end date (YYYY-MM-DD).

        Returns:
            Paginated response with credit bureau report data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "startDate", start_date)
        _set(params, "endDate", end_date)
        return self._list(self.BASE_PATH, params=params)

    def list_all(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int = 100,
        max_items: int | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all credit bureau reports.

        Args:
            start_date: Filter by start date (YYYY-MM-DD).
            end_date: Filter by end date (YYYY-MM-DD).
            limit: Items per page.
            max_items: Max total items to return.

        Yields:
            Individual credit bureau report records.
        """
        params: dict[str, Any] = {}
        _set(params, "startDate", start_date)
        _set(params, "endDate", end_date)
        return self._list_all(self.BASE_PATH, params=params, limit=limit, max_items=max_items)

    def get(self, report_id: str) -> dict[str, Any]:
        """Retrieve a single credit bureau report by ID.

        Args:
            report_id: Credit bureau report identifier.

        Returns:
            Credit bureau report data.
        """
        return self._get(f"{self.BASE_PATH}/{report_id}")
