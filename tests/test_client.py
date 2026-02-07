"""Tests for the main Asaas client."""

import pytest

from asaas import Asaas
from asaas.http_client import PRODUCTION_URL, SANDBOX_URL


class TestClientInit:
    def test_sandbox_mode(self):
        client = Asaas(api_key="test_key", sandbox=True)
        assert client._http.base_url == SANDBOX_URL

    def test_production_mode(self):
        client = Asaas(api_key="test_key", sandbox=False)
        assert client._http.base_url == PRODUCTION_URL

    def test_custom_base_url(self):
        client = Asaas(api_key="test_key", base_url="https://custom.api.com")
        assert client._http.base_url == "https://custom.api.com"

    def test_empty_api_key_raises(self):
        with pytest.raises(ValueError, match="api_key is required"):
            Asaas(api_key="")

    def test_context_manager(self):
        with Asaas(api_key="test_key", sandbox=True) as client:
            assert client._http.base_url == SANDBOX_URL

    def test_repr(self):
        client = Asaas(api_key="test_key", sandbox=True)
        assert "sandbox.asaas.com" in repr(client)

    def test_all_resources_initialized(self):
        client = Asaas(api_key="test_key", sandbox=True)
        assert client.customers is not None
        assert client.payments is not None
        assert client.subscriptions is not None
        assert client.accounts is not None
        assert client.anticipations is not None
        assert client.bill is not None
        assert client.chargebacks is not None
        assert client.checkouts is not None
        assert client.credit_bureau_report is not None
        assert client.credit_card is not None
        assert client.escrow is not None
        assert client.finance is not None
        assert client.financial_transactions is not None
        assert client.fiscal_info is not None
        assert client.installments is not None
        assert client.invoices is not None
        assert client.lean is not None
        assert client.mobile_phone_recharges is not None
        assert client.my_account is not None
        assert client.notifications is not None
        assert client.payment_dunnings is not None
        assert client.payment_links is not None
        assert client.pix is not None
        assert client.sandbox_utils is not None
        assert client.transfers is not None
        assert client.wallets is not None
        assert client.webhooks is not None

    def test_auth_header_set(self):
        client = Asaas(api_key="my_secret_key", sandbox=True)
        assert client._http._session.headers["access_token"] == "my_secret_key"
