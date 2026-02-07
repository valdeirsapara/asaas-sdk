"""Main Asaas SDK client."""

from __future__ import annotations

import logging
from typing import Any

from .http_client import HttpClient, PRODUCTION_URL, SANDBOX_URL
from .resources import (
    Accounts,
    Anticipations,
    Bill,
    Chargebacks,
    Checkouts,
    CreditBureauReport,
    CreditCard,
    Customers,
    Escrow,
    Finance,
    FinancialTransactions,
    FiscalInfo,
    Installments,
    Invoices,
    Lean,
    MobilePhoneRecharges,
    MyAccount,
    Notifications,
    PaymentDunnings,
    PaymentLinks,
    Payments,
    Pix,
    Sandbox,
    Subscriptions,
    Transfers,
    Wallets,
    Webhooks,
)

logger = logging.getLogger("asaas")


class Asaas:
    """Asaas API client.

    Provides access to all Asaas API v3 resources through an intuitive
    interface with automatic authentication, pagination, retries, and
    error handling.

    Example:
        >>> from asaas import Asaas
        >>> client = Asaas(api_key="your_api_key", sandbox=True)
        >>> customer = client.customers.create(
        ...     name="João Silva",
        ...     cpf_cnpj="12345678901",
        ...     email="joao@example.com",
        ... )
        >>> print(customer["id"])
        cus_000005401844

    Args:
        api_key: Your Asaas API access token.
        sandbox: Use sandbox environment (default: False).
        base_url: Override the base URL (ignores sandbox flag if set).
        timeout: Request timeout in seconds (default: 30).
        max_retries: Max retry attempts for 5xx errors (default: 3).
        backoff_factor: Exponential backoff factor (default: 0.5).
    """

    def __init__(
        self,
        api_key: str,
        *,
        sandbox: bool = False,
        base_url: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")

        if base_url:
            resolved_url = base_url
        else:
            resolved_url = SANDBOX_URL if sandbox else PRODUCTION_URL

        self._http = HttpClient(
            api_key=api_key,
            base_url=resolved_url,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
        )

        # Initialize all resources
        self.accounts = Accounts(self._http)
        self.anticipations = Anticipations(self._http)
        self.bill = Bill(self._http)
        self.chargebacks = Chargebacks(self._http)
        self.checkouts = Checkouts(self._http)
        self.credit_bureau_report = CreditBureauReport(self._http)
        self.credit_card = CreditCard(self._http)
        self.customers = Customers(self._http)
        self.escrow = Escrow(self._http)
        self.finance = Finance(self._http)
        self.financial_transactions = FinancialTransactions(self._http)
        self.fiscal_info = FiscalInfo(self._http)
        self.installments = Installments(self._http)
        self.invoices = Invoices(self._http)
        self.lean = Lean(self._http)
        self.mobile_phone_recharges = MobilePhoneRecharges(self._http)
        self.my_account = MyAccount(self._http)
        self.notifications = Notifications(self._http)
        self.payment_dunnings = PaymentDunnings(self._http)
        self.payment_links = PaymentLinks(self._http)
        self.payments = Payments(self._http)
        self.pix = Pix(self._http)
        self.sandbox_utils = Sandbox(self._http)
        self.subscriptions = Subscriptions(self._http)
        self.transfers = Transfers(self._http)
        self.wallets = Wallets(self._http)
        self.webhooks = Webhooks(self._http)

    def close(self) -> None:
        """Close the HTTP session."""
        self._http.close()

    def __enter__(self) -> Asaas:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"Asaas(base_url={self._http.base_url!r})"
