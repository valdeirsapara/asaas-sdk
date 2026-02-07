"""Customers resource."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


class Customers(Resource):
    """Manage customers (clientes) in the Asaas platform.

    Endpoints:
        POST   /v3/customers              - Create customer
        GET    /v3/customers               - List customers
        GET    /v3/customers/:id           - Retrieve customer
        PUT    /v3/customers/:id           - Update customer
        DELETE /v3/customers/:id           - Remove customer
        POST   /v3/customers/:id/restore   - Restore deleted customer
        GET    /v3/customers/:id/notifications - Get customer notifications
    """

    BASE_PATH = "/v3/customers"

    def create(
        self,
        name: str,
        cpf_cnpj: str,
        *,
        email: str | None = None,
        phone: str | None = None,
        mobile_phone: str | None = None,
        address: str | None = None,
        address_number: str | None = None,
        complement: str | None = None,
        province: str | None = None,
        postal_code: str | None = None,
        external_reference: str | None = None,
        notification_disabled: bool | None = None,
        additional_emails: str | None = None,
        municipal_inscription: str | None = None,
        state_inscription: str | None = None,
        observations: str | None = None,
        group_name: str | None = None,
        company: str | None = None,
        foreign_customer: bool | None = None,
    ) -> dict[str, Any]:
        """Create a new customer.

        Args:
            name: Customer full name.
            cpf_cnpj: CPF or CNPJ (numbers only).
            email: Email address.
            phone: Phone number.
            mobile_phone: Mobile phone number.
            address: Street address.
            address_number: Address number.
            complement: Address complement.
            province: Neighborhood.
            postal_code: Postal code (CEP).
            external_reference: External reference ID.
            notification_disabled: Whether to disable notifications.
            additional_emails: Comma-separated additional emails.
            municipal_inscription: Municipal inscription number.
            state_inscription: State inscription number.
            observations: Internal observations.
            group_name: Customer group name.
            company: Company name.
            foreign_customer: Whether this is a foreign customer.

        Returns:
            Created customer data.
        """
        payload: dict[str, Any] = {"name": name, "cpfCnpj": cpf_cnpj}
        _set(payload, "email", email)
        _set(payload, "phone", phone)
        _set(payload, "mobilePhone", mobile_phone)
        _set(payload, "address", address)
        _set(payload, "addressNumber", address_number)
        _set(payload, "complement", complement)
        _set(payload, "province", province)
        _set(payload, "postalCode", postal_code)
        _set(payload, "externalReference", external_reference)
        _set(payload, "notificationDisabled", notification_disabled)
        _set(payload, "additionalEmails", additional_emails)
        _set(payload, "municipalInscription", municipal_inscription)
        _set(payload, "stateInscription", state_inscription)
        _set(payload, "observations", observations)
        _set(payload, "groupName", group_name)
        _set(payload, "company", company)
        _set(payload, "foreignCustomer", foreign_customer)
        return self._post(self.BASE_PATH, json=payload)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        name: str | None = None,
        email: str | None = None,
        cpf_cnpj: str | None = None,
        group_name: str | None = None,
        external_reference: str | None = None,
    ) -> PaginatedResponse:
        """List customers (single page).

        Args:
            offset: Page offset.
            limit: Page size.
            name: Filter by name.
            email: Filter by email.
            cpf_cnpj: Filter by CPF/CNPJ.
            group_name: Filter by group name.
            external_reference: Filter by external reference.

        Returns:
            Paginated response with customer data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "name", name)
        _set(params, "email", email)
        _set(params, "cpfCnpj", cpf_cnpj)
        _set(params, "groupName", group_name)
        _set(params, "externalReference", external_reference)
        return self._list(self.BASE_PATH, params=params)

    def list_all(
        self,
        *,
        name: str | None = None,
        email: str | None = None,
        cpf_cnpj: str | None = None,
        group_name: str | None = None,
        external_reference: str | None = None,
        limit: int = 100,
        max_items: int | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all customers.

        Args:
            name: Filter by name.
            email: Filter by email.
            cpf_cnpj: Filter by CPF/CNPJ.
            group_name: Filter by group name.
            external_reference: Filter by external reference.
            limit: Items per page.
            max_items: Max total items to return.

        Yields:
            Individual customer records.
        """
        params: dict[str, Any] = {}
        _set(params, "name", name)
        _set(params, "email", email)
        _set(params, "cpfCnpj", cpf_cnpj)
        _set(params, "groupName", group_name)
        _set(params, "externalReference", external_reference)
        return self._list_all(self.BASE_PATH, params=params, limit=limit, max_items=max_items)

    def get(self, customer_id: str) -> dict[str, Any]:
        """Retrieve a single customer by ID.

        Args:
            customer_id: Customer identifier (e.g. 'cus_000005401844').

        Returns:
            Customer data.
        """
        return self._get(f"{self.BASE_PATH}/{customer_id}")

    def update(self, customer_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update an existing customer.

        Args:
            customer_id: Customer identifier.
            **kwargs: Fields to update. Supported keys:
                name, cpf_cnpj, email, phone, mobile_phone, address,
                address_number, complement, province, postal_code,
                external_reference, notification_disabled, additional_emails,
                municipal_inscription, state_inscription, observations,
                group_name, company, foreign_customer.

        Returns:
            Updated customer data.
        """
        payload = _to_camel_payload(kwargs)
        return self._put(f"{self.BASE_PATH}/{customer_id}", json=payload)

    def delete(self, customer_id: str) -> dict[str, Any]:
        """Remove a customer.

        Args:
            customer_id: Customer identifier.

        Returns:
            Deletion confirmation.
        """
        return self._delete(f"{self.BASE_PATH}/{customer_id}")

    def restore(self, customer_id: str) -> dict[str, Any]:
        """Restore a previously deleted customer.

        Args:
            customer_id: Customer identifier.

        Returns:
            Restored customer data.
        """
        return self._post(f"{self.BASE_PATH}/{customer_id}/restore", json={})

    def get_notifications(self, customer_id: str) -> dict[str, Any]:
        """Retrieve notifications for a customer.

        Args:
            customer_id: Customer identifier.

        Returns:
            Customer notification settings.
        """
        return self._get(f"{self.BASE_PATH}/{customer_id}/notifications")


# -- Helpers --

_SNAKE_TO_CAMEL: dict[str, str] = {
    "cpf_cnpj": "cpfCnpj",
    "mobile_phone": "mobilePhone",
    "address_number": "addressNumber",
    "postal_code": "postalCode",
    "external_reference": "externalReference",
    "notification_disabled": "notificationDisabled",
    "additional_emails": "additionalEmails",
    "municipal_inscription": "municipalInscription",
    "state_inscription": "stateInscription",
    "group_name": "groupName",
    "foreign_customer": "foreignCustomer",
}


def _to_camel(key: str) -> str:
    return _SNAKE_TO_CAMEL.get(key, key)


def _to_camel_payload(kwargs: dict[str, Any]) -> dict[str, Any]:
    return {_to_camel(k): v for k, v in kwargs.items() if v is not None}


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value
