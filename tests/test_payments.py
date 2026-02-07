"""Tests for the Payments resource."""

import json

import pytest
import responses

from asaas import Asaas
from asaas.exceptions import AsaasValidationError, AsaasAuthenticationError, AsaasNotFoundError


SANDBOX_URL = "https://sandbox.asaas.com/api"


PAYMENT_RESPONSE = {
    "object": "payment",
    "id": "pay_080225913252",
    "dateCreated": "2024-07-12",
    "customer": "cus_000005401844",
    "value": 100.50,
    "netValue": 97.51,
    "billingType": "BOLETO",
    "status": "PENDING",
    "dueDate": "2024-12-31",
    "description": "Test payment",
    "invoiceUrl": "https://sandbox.asaas.com/i/080225913252",
    "bankSlipUrl": "https://sandbox.asaas.com/b/pdf/080225913252",
    "deleted": False,
}


class TestPaymentsCreate:
    @responses.activate
    def test_create_boleto(self, client):
        responses.add(
            responses.POST,
            f"{SANDBOX_URL}/v3/payments/",
            json=PAYMENT_RESPONSE,
            status=200,
        )

        result = client.payments.create(
            customer="cus_000005401844",
            billing_type="BOLETO",
            value=100.50,
            due_date="2024-12-31",
            description="Test payment",
        )

        assert result["id"] == "pay_080225913252"
        assert result["billingType"] == "BOLETO"
        assert result["value"] == 100.50

        body = json.loads(responses.calls[0].request.body)
        assert body["customer"] == "cus_000005401844"
        assert body["billingType"] == "BOLETO"
        assert body["value"] == 100.50
        assert body["dueDate"] == "2024-12-31"

    @responses.activate
    def test_create_credit_card(self, client):
        cc_response = {**PAYMENT_RESPONSE, "billingType": "CREDIT_CARD"}
        responses.add(
            responses.POST,
            f"{SANDBOX_URL}/v3/payments/",
            json=cc_response,
            status=200,
        )

        result = client.payments.create(
            customer="cus_000005401844",
            billing_type="CREDIT_CARD",
            value=100.50,
            due_date="2024-12-31",
            credit_card={
                "holderName": "john doe",
                "number": "5162306219378829",
                "expiryMonth": "05",
                "expiryYear": "2025",
                "ccv": "318",
            },
            credit_card_holder_info={
                "name": "John Doe",
                "email": "john@example.com",
                "cpfCnpj": "24971563792",
                "postalCode": "89223-005",
                "phone": "4738010919",
            },
        )

        assert result["billingType"] == "CREDIT_CARD"


class TestPaymentsList:
    @responses.activate
    def test_list_payments(self, client):
        list_response = {
            "object": "list",
            "hasMore": False,
            "totalCount": 1,
            "limit": 10,
            "offset": 0,
            "data": [PAYMENT_RESPONSE],
        }
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/payments",
            json=list_response,
            status=200,
        )

        page = client.payments.list(customer="cus_000005401844")
        assert page.total_count == 1
        assert page.data[0]["id"] == "pay_080225913252"

    @responses.activate
    def test_list_with_date_filters(self, client):
        list_response = {
            "object": "list",
            "hasMore": False,
            "totalCount": 0,
            "limit": 10,
            "offset": 0,
            "data": [],
        }
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/payments",
            json=list_response,
            status=200,
        )

        client.payments.list(
            due_date_ge="2024-01-01",
            due_date_le="2024-12-31",
            status="PENDING",
        )

        url = responses.calls[0].request.url
        assert "dueDate%5Bge%5D=2024-01-01" in url
        assert "dueDate%5Ble%5D=2024-12-31" in url
        assert "status=PENDING" in url


class TestPaymentsActions:
    @responses.activate
    def test_refund(self, client):
        refund_response = {**PAYMENT_RESPONSE, "status": "REFUNDED"}
        responses.add(
            responses.POST,
            f"{SANDBOX_URL}/v3/payments/pay_080225913252/refund",
            json=refund_response,
            status=200,
        )

        result = client.payments.refund("pay_080225913252")
        assert result["status"] == "REFUNDED"

    @responses.activate
    def test_partial_refund(self, client):
        responses.add(
            responses.POST,
            f"{SANDBOX_URL}/v3/payments/pay_080225913252/refund",
            json=PAYMENT_RESPONSE,
            status=200,
        )

        client.payments.refund("pay_080225913252", value=50.0, description="Partial refund")

        body = json.loads(responses.calls[0].request.body)
        assert body["value"] == 50.0
        assert body["description"] == "Partial refund"

    @responses.activate
    def test_get_pix_qr_code(self, client):
        qr_response = {
            "encodedImage": "base64string...",
            "payload": "00020126...",
            "expirationDate": "2024-12-31 23:59:59",
        }
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/payments/pay_080225913252/pixQrCode",
            json=qr_response,
            status=200,
        )

        result = client.payments.get_pix_qr_code("pay_080225913252")
        assert "encodedImage" in result
        assert "payload" in result

    @responses.activate
    def test_get_identification_field(self, client):
        response = {"identificationField": "23793.38128 60000.000003 00000.000401 1 84340000010050"}
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/payments/pay_080225913252/identificationField",
            json=response,
            status=200,
        )

        result = client.payments.get_identification_field("pay_080225913252")
        assert "identificationField" in result

    @responses.activate
    def test_restore(self, client):
        responses.add(
            responses.POST,
            f"{SANDBOX_URL}/v3/payments/pay_080225913252/restore",
            json=PAYMENT_RESPONSE,
            status=200,
        )

        result = client.payments.restore("pay_080225913252")
        assert result["id"] == "pay_080225913252"


class TestPaymentsErrors:
    @responses.activate
    def test_validation_error_400(self, client):
        error_body = {
            "errors": [
                {"code": "invalid_value", "description": "O valor deve ser maior que zero."}
            ]
        }
        responses.add(
            responses.POST,
            f"{SANDBOX_URL}/v3/payments/",
            json=error_body,
            status=400,
        )

        with pytest.raises(AsaasValidationError) as exc_info:
            client.payments.create(
                customer="cus_000005401844",
                billing_type="BOLETO",
                value=-1,
                due_date="2024-12-31",
            )
        assert exc_info.value.status_code == 400
        assert len(exc_info.value.errors) == 1

    @responses.activate
    def test_auth_error_401(self, client):
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/payments",
            json={"errors": [{"code": "unauthorized", "description": "Invalid API Key"}]},
            status=401,
        )

        with pytest.raises(AsaasAuthenticationError):
            client.payments.list()

    @responses.activate
    def test_not_found_404(self, client):
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/payments/pay_nonexistent",
            json={"errors": [{"code": "not_found", "description": "Payment not found"}]},
            status=404,
        )

        with pytest.raises(AsaasNotFoundError):
            client.payments.get("pay_nonexistent")
