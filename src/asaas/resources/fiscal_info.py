"""Fiscal information resource."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class FiscalInfo(Resource):
    """Manage fiscal information (informações fiscais) in the Asaas platform.

    Endpoints:
        POST /v3/fiscalInfo/                      - Create or update fiscal info
        GET  /v3/fiscalInfo/                       - Retrieve fiscal info
        POST /v3/fiscalInfo/nationalPortal         - Configure national portal
        GET  /v3/fiscalInfo/municipalOptions        - List municipal options
        GET  /v3/fiscalInfo/federalServiceCodes     - List federal service codes
        GET  /v3/fiscalInfo/services                - List services
        GET  /v3/fiscalInfo/nbsCodes                - List NBS codes
        GET  /v3/fiscalInfo/operationIndicatorCodes - List operation indicator codes
        GET  /v3/fiscalInfo/taxClassificationCodes  - List tax classification codes
        GET  /v3/fiscalInfo/taxSituationCodes       - List tax situation codes
    """

    BASE_PATH = "/v3/fiscalInfo"

    # ---- CRUD ----

    def create_or_update(self, **kwargs: Any) -> dict[str, Any]:
        """Create or update fiscal information for the account.

        Args:
            **kwargs: Fiscal info fields. Refer to the Asaas API
                documentation for the full list of supported fields
                (e.g. simplesNacional, culturalProjectIncentive,
                specialTaxRegime, serviceListItem, cnae, etc.).

        Returns:
            Created or updated fiscal info data.
        """
        return self._post(f"{self.BASE_PATH}/", json=kwargs)

    def get(self) -> dict[str, Any]:
        """Retrieve the current fiscal information.

        Returns:
            Fiscal info data.
        """
        return self._get(f"{self.BASE_PATH}/")

    # ---- National Portal ----

    def configure_national_portal(self, **kwargs: Any) -> dict[str, Any]:
        """Configure the national portal for invoice issuance.

        Args:
            **kwargs: National portal configuration fields (e.g.
                login, password, etc.).

        Returns:
            National portal configuration data.
        """
        return self._post(f"{self.BASE_PATH}/nationalPortal", json=kwargs)

    # ---- Lookup Endpoints ----

    def list_municipal_options(self) -> dict[str, Any]:
        """List available municipal options for fiscal configuration.

        Returns:
            Municipal options data.
        """
        return self._get(f"{self.BASE_PATH}/municipalOptions")

    def list_federal_service_codes(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        code: str | None = None,
        description: str | None = None,
    ) -> PaginatedResponse:
        """List federal service codes.

        Args:
            offset: Page offset.
            limit: Page size.
            code: Filter by code.
            description: Filter by description.

        Returns:
            Paginated response with federal service codes.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "code", code)
        _set(params, "description", description)
        return self._list(f"{self.BASE_PATH}/federalServiceCodes", params=params)

    def list_services(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        description: str | None = None,
    ) -> PaginatedResponse:
        """List available services.

        Args:
            offset: Page offset.
            limit: Page size.
            description: Filter by description.

        Returns:
            Paginated response with services.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "description", description)
        return self._list(f"{self.BASE_PATH}/services", params=params)

    def list_nbs_codes(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        code_description: str | None = None,
    ) -> PaginatedResponse:
        """List NBS (Nomenclatura Brasileira de Servicos) codes.

        Args:
            offset: Page offset.
            limit: Page size.
            code_description: Filter by code or description.

        Returns:
            Paginated response with NBS codes.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "codeDescription", code_description)
        return self._list(f"{self.BASE_PATH}/nbsCodes", params=params)

    def list_operation_indicator_codes(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        code: str | None = None,
        description: str | None = None,
    ) -> PaginatedResponse:
        """List operation indicator codes.

        Args:
            offset: Page offset.
            limit: Page size.
            code: Filter by code.
            description: Filter by description.

        Returns:
            Paginated response with operation indicator codes.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "code", code)
        _set(params, "description", description)
        return self._list(f"{self.BASE_PATH}/operationIndicatorCodes", params=params)

    def list_tax_classification_codes(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        code: str | None = None,
        description: str | None = None,
        tax_situation_code: str | None = None,
    ) -> PaginatedResponse:
        """List tax classification codes.

        Args:
            offset: Page offset.
            limit: Page size.
            code: Filter by code.
            description: Filter by description.
            tax_situation_code: Filter by tax situation code.

        Returns:
            Paginated response with tax classification codes.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "code", code)
        _set(params, "description", description)
        _set(params, "taxSituationCode", tax_situation_code)
        return self._list(f"{self.BASE_PATH}/taxClassificationCodes", params=params)

    def list_tax_situation_codes(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        code: str | None = None,
        description: str | None = None,
    ) -> PaginatedResponse:
        """List tax situation codes.

        Args:
            offset: Page offset.
            limit: Page size.
            code: Filter by code.
            description: Filter by description.

        Returns:
            Paginated response with tax situation codes.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "code", code)
        _set(params, "description", description)
        return self._list(f"{self.BASE_PATH}/taxSituationCodes", params=params)
