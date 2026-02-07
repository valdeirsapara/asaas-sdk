"""Shared test fixtures."""

import pytest
import responses

from asaas import Asaas


SANDBOX_URL = "https://sandbox.asaas.com/api"


@pytest.fixture
def client():
    """Create a sandbox Asaas client for testing."""
    return Asaas(api_key="test_api_key_123", sandbox=True)


@pytest.fixture
def mocked_responses():
    """Activate the responses mock."""
    with responses.RequestsMock() as rsps:
        yield rsps
