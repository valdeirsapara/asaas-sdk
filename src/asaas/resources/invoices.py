"""Invoices resource."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Invoices(Resource):
    """Manage invoices (notas fiscais) in the Asaas platform.

    Endpoints:
        POST /v3/invoices              - Schedule invoice
        GET  /v3/invoices              - List invoices
        GET  /v3/invoices/:id          - Retrieve invoice
        PUT  /v3/invoices/:id          - Update invoice
        POST /v3/invoices/:id/authorize - Issue (authorize) invoice
        POST /v3/invoices/:id/cancel   - Cancel invoice
    """

    BASE_PATH = "/v3/invoices"

    # ---- CRUD ----

    def schedule(self, **kwargs: Any) -> dict[str, Any]:
        """Schedule a new invoice for issuance.

        Args:
            **kwargs: Invoice fields. Commonly used keys include:
                payment, installment, customer, serviceDescription,
                observations, externalReference, value,
                deductions, effectiveDatePeriod, municipalServiceId,
                municipalServiceCode, municipalServiceName, etc.

        Returns:
            Scheduled invoice data.
        """
        return self._post(self.BASE_PATH, json=kwargs)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        effective_date_ge: str | None = None,
        effective_date_le: str | None = None,
        payment: str | None = None,
        installment: str | None = None,
        external_reference: str | None = None,
        status: str | None = None,
        customer: str | None = None,
    ) -> PaginatedResponse:
        """List invoices (single page).

        Args:
            offset: Page offset.
            limit: Page size.
            effective_date_ge: Filter by effective date >= (YYYY-MM-DD).
            effective_date_le: Filter by effective date <= (YYYY-MM-DD).
            payment: Filter by payment ID.
            installment: Filter by installment ID.
            external_reference: Filter by external reference.
            status: Filter by status (SCHEDULED, AUTHORIZED, CANCELLED, etc.).
            customer: Filter by customer ID.

        Returns:
            Paginated response with invoice data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "effectiveDate[ge]", effective_date_ge)
        _set(params, "effectiveDate[le]", effective_date_le)
        _set(params, "payment", payment)
        _set(params, "installment", installment)
        _set(params, "externalReference", external_reference)
        _set(params, "status", status)
        _set(params, "customer", customer)
        return self._list(self.BASE_PATH, params=params)

    def get(self, invoice_id: str) -> dict[str, Any]:
        """Retrieve a single invoice by ID.

        Args:
            invoice_id: Invoice identifier.

        Returns:
            Invoice data.
        """
        return self._get(f"{self.BASE_PATH}/{invoice_id}")

    def update(self, invoice_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update an existing invoice.

        Args:
            invoice_id: Invoice identifier.
            **kwargs: Fields to update (e.g. serviceDescription,
                observations, externalReference, value, deductions,
                effectiveDatePeriod, municipalServiceId, etc.).

        Returns:
            Updated invoice data.
        """
        return self._put(f"{self.BASE_PATH}/{invoice_id}", json=kwargs)

    # ---- Actions ----

    def authorize(self, invoice_id: str) -> dict[str, Any]:
        """Issue (authorize) a scheduled invoice.

        Args:
            invoice_id: Invoice identifier.

        Returns:
            Authorized invoice data.
        """
        return self._post(f"{self.BASE_PATH}/{invoice_id}/authorize", json={})

    def cancel(self, invoice_id: str) -> dict[str, Any]:
        """Cancel an invoice.

        Args:
            invoice_id: Invoice identifier.

        Returns:
            Cancellation confirmation.
        """
        return self._post(f"{self.BASE_PATH}/{invoice_id}/cancel", json={})
