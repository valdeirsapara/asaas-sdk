"""Accounts resource -- manage subaccounts (contas filhas) in the Asaas platform."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Accounts(Resource):
    """Manage subaccounts (contas filhas) in the Asaas platform.

    Endpoints:
        POST   /v3/accounts                                      - Create subaccount
        GET    /v3/accounts                                       - List subaccounts
        GET    /v3/accounts/:id                                   - Retrieve subaccount
        POST   /v3/accounts/:id/accessTokens                     - Create access token
        GET    /v3/accounts/:id/accessTokens                     - List access tokens
        PUT    /v3/accounts/:id/accessTokens/:accessTokenId      - Update access token
        DELETE /v3/accounts/:id/accessTokens/:accessTokenId      - Delete access token
        POST   /v3/accounts/:id/escrow                           - Save escrow for subaccount
        GET    /v3/accounts/:id/escrow                           - Get escrow for subaccount
        POST   /v3/accounts/escrow                               - Create default escrow
        GET    /v3/accounts/escrow                               - Get default escrow
    """

    BASE_PATH = "/v3/accounts"

    # ---- Subaccount CRUD ----

    def create(
        self,
        name: str,
        cpf_cnpj: str,
        company_type: str | None = None,
        *,
        email: str | None = None,
        login_email: str | None = None,
        phone: str | None = None,
        mobile_phone: str | None = None,
        address: str | None = None,
        address_number: str | None = None,
        complement: str | None = None,
        province: str | None = None,
        postal_code: str | None = None,
        site: str | None = None,
        income_value: float | None = None,
        birth_date: str | None = None,
        webhooks: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Create a new subaccount.

        Args:
            name: Subaccount name or company name.
            cpf_cnpj: CPF or CNPJ (numbers only).
            company_type: Company type (MEI, LIMITED, INDIVIDUAL, ASSOCIATION).
            email: Email address.
            login_email: Login email for the subaccount.
            phone: Phone number.
            mobile_phone: Mobile phone number.
            address: Street address.
            address_number: Address number.
            complement: Address complement.
            province: Neighborhood.
            postal_code: Postal code (CEP).
            site: Website URL.
            income_value: Monthly income value.
            birth_date: Birth date (YYYY-MM-DD).
            webhooks: List of webhook configurations.

        Returns:
            Created subaccount data.
        """
        payload: dict[str, Any] = {"name": name, "cpfCnpj": cpf_cnpj}
        _set(payload, "companyType", company_type)
        _set(payload, "email", email)
        _set(payload, "loginEmail", login_email)
        _set(payload, "phone", phone)
        _set(payload, "mobilePhone", mobile_phone)
        _set(payload, "address", address)
        _set(payload, "addressNumber", address_number)
        _set(payload, "complement", complement)
        _set(payload, "province", province)
        _set(payload, "postalCode", postal_code)
        _set(payload, "site", site)
        _set(payload, "incomeValue", income_value)
        _set(payload, "birthDate", birth_date)
        _set(payload, "webhooks", webhooks)
        return self._post(self.BASE_PATH, json=payload)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        cpf_cnpj: str | None = None,
        email: str | None = None,
        name: str | None = None,
        wallet_id: str | None = None,
    ) -> PaginatedResponse:
        """List subaccounts (single page).

        Args:
            offset: Page offset.
            limit: Page size.
            cpf_cnpj: Filter by CPF/CNPJ.
            email: Filter by email.
            name: Filter by name.
            wallet_id: Filter by wallet ID.

        Returns:
            Paginated response with subaccount data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "cpfCnpj", cpf_cnpj)
        _set(params, "email", email)
        _set(params, "name", name)
        _set(params, "walletId", wallet_id)
        return self._list(self.BASE_PATH, params=params)

    def list_all(
        self,
        *,
        cpf_cnpj: str | None = None,
        email: str | None = None,
        name: str | None = None,
        wallet_id: str | None = None,
        limit: int = 100,
        max_items: int | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all subaccounts.

        Args:
            cpf_cnpj: Filter by CPF/CNPJ.
            email: Filter by email.
            name: Filter by name.
            wallet_id: Filter by wallet ID.
            limit: Items per page.
            max_items: Max total items to return.

        Yields:
            Individual subaccount records.
        """
        params: dict[str, Any] = {}
        _set(params, "cpfCnpj", cpf_cnpj)
        _set(params, "email", email)
        _set(params, "name", name)
        _set(params, "walletId", wallet_id)
        return self._list_all(self.BASE_PATH, params=params, limit=limit, max_items=max_items)

    def get(self, account_id: str) -> dict[str, Any]:
        """Retrieve a single subaccount by ID.

        Args:
            account_id: Subaccount identifier.

        Returns:
            Subaccount data.
        """
        return self._get(f"{self.BASE_PATH}/{account_id}")

    # ---- Access Tokens ----

    def create_access_token(self, account_id: str) -> dict[str, Any]:
        """Create a new access token for a subaccount.

        Args:
            account_id: Subaccount identifier.

        Returns:
            Created access token data.
        """
        return self._post(f"{self.BASE_PATH}/{account_id}/accessTokens", json={})

    def list_access_tokens(self, account_id: str) -> dict[str, Any]:
        """List access tokens for a subaccount.

        Args:
            account_id: Subaccount identifier.

        Returns:
            List of access tokens.
        """
        return self._get(f"{self.BASE_PATH}/{account_id}/accessTokens")

    def update_access_token(self, account_id: str, token_id: str) -> dict[str, Any]:
        """Update an access token for a subaccount.

        Args:
            account_id: Subaccount identifier.
            token_id: Access token identifier.

        Returns:
            Updated access token data.
        """
        return self._put(f"{self.BASE_PATH}/{account_id}/accessTokens/{token_id}", json={})

    def delete_access_token(self, account_id: str, token_id: str) -> dict[str, Any]:
        """Delete an access token for a subaccount.

        Args:
            account_id: Subaccount identifier.
            token_id: Access token identifier.

        Returns:
            Deletion confirmation.
        """
        return self._delete(f"{self.BASE_PATH}/{account_id}/accessTokens/{token_id}")

    # ---- Escrow (per subaccount) ----

    def save_escrow(
        self,
        account_id: str,
        *,
        description: str | None = None,
        expiration_date: str | None = None,
        responsible_name: str | None = None,
        responsible_cpf_cnpj: str | None = None,
        responsible_phone: str | None = None,
        responsible_email: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Save escrow configuration for a subaccount.

        Args:
            account_id: Subaccount identifier.
            description: Escrow description.
            expiration_date: Escrow expiration date (YYYY-MM-DD).
            responsible_name: Name of the responsible person.
            responsible_cpf_cnpj: CPF/CNPJ of the responsible person.
            responsible_phone: Phone of the responsible person.
            responsible_email: Email of the responsible person.
            **kwargs: Additional escrow fields.

        Returns:
            Escrow data.
        """
        payload: dict[str, Any] = {}
        _set(payload, "description", description)
        _set(payload, "expirationDate", expiration_date)
        _set(payload, "responsibleName", responsible_name)
        _set(payload, "responsibleCpfCnpj", responsible_cpf_cnpj)
        _set(payload, "responsiblePhone", responsible_phone)
        _set(payload, "responsibleEmail", responsible_email)
        payload.update(kwargs)
        return self._post(f"{self.BASE_PATH}/{account_id}/escrow", json=payload)

    def get_escrow(self, account_id: str) -> dict[str, Any]:
        """Retrieve escrow configuration for a subaccount.

        Args:
            account_id: Subaccount identifier.

        Returns:
            Escrow data.
        """
        return self._get(f"{self.BASE_PATH}/{account_id}/escrow")

    # ---- Default Escrow ----

    def create_default_escrow(self, **kwargs: Any) -> dict[str, Any]:
        """Create the default escrow configuration.

        Args:
            **kwargs: Escrow configuration fields.

        Returns:
            Default escrow data.
        """
        return self._post(f"{self.BASE_PATH}/escrow", json=kwargs)

    def get_default_escrow(self) -> dict[str, Any]:
        """Retrieve the default escrow configuration.

        Returns:
            Default escrow data.
        """
        return self._get(f"{self.BASE_PATH}/escrow")
