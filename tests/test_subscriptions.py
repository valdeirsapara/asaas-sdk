"""Tests for the Subscriptions resource."""

import json

import responses

from asaas import Asaas


SANDBOX_URL = "https://sandbox.asaas.com/api"


SUBSCRIPTION_RESPONSE = {
    "object": "subscription",
    "id": "sub_abc123",
    "dateCreated": "2024-07-12",
    "customer": "cus_000005401844",
    "value": 49.90,
    "billingType": "CREDIT_CARD",
    "cycle": "MONTHLY",
    "status": "ACTIVE",
    "nextDueDate": "2024-08-12",
    "description": "Monthly plan",
    "deleted": False,
}


class TestSubscriptionsCreate:
    @responses.activate
    def test_create_subscription(self, client):
        responses.add(
            responses.POST,
            f"{SANDBOX_URL}/v3/subscriptions/",
            json=SUBSCRIPTION_RESPONSE,
            status=200,
        )

        result = client.subscriptions.create(
            customer="cus_000005401844",
            billing_type="CREDIT_CARD",
            value=49.90,
            next_due_date="2024-08-12",
            cycle="MONTHLY",
            description="Monthly plan",
        )

        assert result["id"] == "sub_abc123"
        assert result["cycle"] == "MONTHLY"
        assert result["value"] == 49.90

        body = json.loads(responses.calls[0].request.body)
        assert body["customer"] == "cus_000005401844"
        assert body["billingType"] == "CREDIT_CARD"
        assert body["nextDueDate"] == "2024-08-12"
        assert body["cycle"] == "MONTHLY"


class TestSubscriptionsList:
    @responses.activate
    def test_list_subscriptions(self, client):
        list_response = {
            "object": "list",
            "hasMore": False,
            "totalCount": 1,
            "limit": 10,
            "offset": 0,
            "data": [SUBSCRIPTION_RESPONSE],
        }
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/subscriptions",
            json=list_response,
            status=200,
        )

        page = client.subscriptions.list(status="ACTIVE")
        assert page.total_count == 1
        assert page.data[0]["id"] == "sub_abc123"


class TestSubscriptionsGet:
    @responses.activate
    def test_get_subscription(self, client):
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/subscriptions/sub_abc123",
            json=SUBSCRIPTION_RESPONSE,
            status=200,
        )

        result = client.subscriptions.get("sub_abc123")
        assert result["id"] == "sub_abc123"
        assert result["status"] == "ACTIVE"


class TestSubscriptionsDelete:
    @responses.activate
    def test_delete_subscription(self, client):
        responses.add(
            responses.DELETE,
            f"{SANDBOX_URL}/v3/subscriptions/sub_abc123",
            json={"deleted": True, "id": "sub_abc123"},
            status=200,
        )

        result = client.subscriptions.delete("sub_abc123")
        assert result["deleted"] is True


class TestSubscriptionsPayments:
    @responses.activate
    def test_list_subscription_payments(self, client):
        payments_response = {
            "object": "list",
            "hasMore": False,
            "totalCount": 2,
            "limit": 10,
            "offset": 0,
            "data": [
                {"id": "pay_1", "status": "RECEIVED"},
                {"id": "pay_2", "status": "PENDING"},
            ],
        }
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/subscriptions/sub_abc123/payments",
            json=payments_response,
            status=200,
        )

        result = client.subscriptions.list_payments("sub_abc123")
        assert len(result["data"]) == 2
