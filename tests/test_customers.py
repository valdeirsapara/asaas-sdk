"""Tests for the Customers resource."""

import json

import pytest
import responses

from asaas import Asaas


SANDBOX_URL = "https://sandbox.asaas.com/api"


CUSTOMER_RESPONSE = {
    "object": "customer",
    "id": "cus_000005401844",
    "dateCreated": "2024-07-12",
    "name": "John Doe",
    "email": "john.doe@asaas.com.br",
    "phone": "90999999999",
    "mobilePhone": "90999999999",
    "cpfCnpj": "24971563792",
    "personType": "FISICA",
    "deleted": False,
    "notificationDisabled": False,
    "foreignCustomer": False,
}


LIST_RESPONSE = {
    "object": "list",
    "hasMore": False,
    "totalCount": 1,
    "limit": 10,
    "offset": 0,
    "data": [CUSTOMER_RESPONSE],
}


class TestCustomersCreate:
    @responses.activate
    def test_create_customer(self, client):
        responses.add(
            responses.POST,
            f"{SANDBOX_URL}/v3/customers",
            json=CUSTOMER_RESPONSE,
            status=200,
        )

        result = client.customers.create(
            name="John Doe",
            cpf_cnpj="24971563792",
            email="john.doe@asaas.com.br",
        )

        assert result["id"] == "cus_000005401844"
        assert result["name"] == "John Doe"

        body = json.loads(responses.calls[0].request.body)
        assert body["name"] == "John Doe"
        assert body["cpfCnpj"] == "24971563792"
        assert body["email"] == "john.doe@asaas.com.br"

    @responses.activate
    def test_create_customer_minimal(self, client):
        responses.add(
            responses.POST,
            f"{SANDBOX_URL}/v3/customers",
            json=CUSTOMER_RESPONSE,
            status=200,
        )

        result = client.customers.create(name="John Doe", cpf_cnpj="24971563792")
        assert result["id"] == "cus_000005401844"

        body = json.loads(responses.calls[0].request.body)
        assert "email" not in body


class TestCustomersList:
    @responses.activate
    def test_list_customers(self, client):
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/customers",
            json=LIST_RESPONSE,
            status=200,
        )

        page = client.customers.list()
        assert page.total_count == 1
        assert len(page.data) == 1
        assert page.data[0]["id"] == "cus_000005401844"
        assert page.has_more is False

    @responses.activate
    def test_list_with_filters(self, client):
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/customers",
            json=LIST_RESPONSE,
            status=200,
        )

        client.customers.list(name="John", cpf_cnpj="24971563792")

        assert "name=John" in responses.calls[0].request.url
        assert "cpfCnpj=24971563792" in responses.calls[0].request.url


class TestCustomersGet:
    @responses.activate
    def test_get_customer(self, client):
        responses.add(
            responses.GET,
            f"{SANDBOX_URL}/v3/customers/cus_000005401844",
            json=CUSTOMER_RESPONSE,
            status=200,
        )

        result = client.customers.get("cus_000005401844")
        assert result["id"] == "cus_000005401844"
        assert result["name"] == "John Doe"


class TestCustomersUpdate:
    @responses.activate
    def test_update_customer(self, client):
        updated = {**CUSTOMER_RESPONSE, "name": "Jane Doe"}
        responses.add(
            responses.PUT,
            f"{SANDBOX_URL}/v3/customers/cus_000005401844",
            json=updated,
            status=200,
        )

        result = client.customers.update("cus_000005401844", name="Jane Doe")
        assert result["name"] == "Jane Doe"


class TestCustomersDelete:
    @responses.activate
    def test_delete_customer(self, client):
        responses.add(
            responses.DELETE,
            f"{SANDBOX_URL}/v3/customers/cus_000005401844",
            json={"deleted": True, "id": "cus_000005401844"},
            status=200,
        )

        result = client.customers.delete("cus_000005401844")
        assert result["deleted"] is True


class TestCustomersRestore:
    @responses.activate
    def test_restore_customer(self, client):
        responses.add(
            responses.POST,
            f"{SANDBOX_URL}/v3/customers/cus_000005401844/restore",
            json=CUSTOMER_RESPONSE,
            status=200,
        )

        result = client.customers.restore("cus_000005401844")
        assert result["id"] == "cus_000005401844"
        assert result["deleted"] is False


class TestCustomersListAll:
    @responses.activate
    def test_auto_pagination(self, client):
        page1 = {
            "object": "list",
            "hasMore": True,
            "totalCount": 3,
            "limit": 2,
            "offset": 0,
            "data": [
                {**CUSTOMER_RESPONSE, "id": "cus_1"},
                {**CUSTOMER_RESPONSE, "id": "cus_2"},
            ],
        }
        page2 = {
            "object": "list",
            "hasMore": False,
            "totalCount": 3,
            "limit": 2,
            "offset": 2,
            "data": [
                {**CUSTOMER_RESPONSE, "id": "cus_3"},
            ],
        }
        responses.add(responses.GET, f"{SANDBOX_URL}/v3/customers", json=page1, status=200)
        responses.add(responses.GET, f"{SANDBOX_URL}/v3/customers", json=page2, status=200)

        customers = list(client.customers.list_all(limit=2))
        assert len(customers) == 3
        assert customers[0]["id"] == "cus_1"
        assert customers[2]["id"] == "cus_3"

    @responses.activate
    def test_auto_pagination_with_max_items(self, client):
        page1 = {
            "object": "list",
            "hasMore": True,
            "totalCount": 10,
            "limit": 5,
            "offset": 0,
            "data": [{**CUSTOMER_RESPONSE, "id": f"cus_{i}"} for i in range(5)],
        }
        responses.add(responses.GET, f"{SANDBOX_URL}/v3/customers", json=page1, status=200)

        customers = list(client.customers.list_all(limit=5, max_items=3))
        assert len(customers) == 3
