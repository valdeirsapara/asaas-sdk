"""Webhooks resource."""

from __future__ import annotations

from typing import Any, Generator

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Webhooks(Resource):
    """Manage webhooks in the Asaas platform."""

    BASE_PATH = "/v3/webhooks"

    def create(
        self,
        url: str,
        email: str,
        *,
        enabled: bool | None = None,
        interrupted: bool | None = None,
        api_version: int | None = None,
        auth_token: str | None = None,
        events: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a new webhook.

        Args:
            url: Webhook URL to receive events.
            email: Contact email for webhook issues.
            enabled: Whether the webhook is enabled.
            interrupted: Whether the webhook is interrupted.
            api_version: API version for event payloads.
            auth_token: Authentication token for webhook validation.
            events: List of event types to subscribe to.

        Returns:
            Created webhook data.
        """
        payload: dict[str, Any] = {"url": url, "email": email}
        _set(payload, "enabled", enabled)
        _set(payload, "interrupted", interrupted)
        _set(payload, "apiVersion", api_version)
        _set(payload, "authToken", auth_token)
        _set(payload, "events", events)
        return self._post(self.BASE_PATH, json=payload)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> PaginatedResponse:
        """List webhooks."""
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        return self._list(self.BASE_PATH, params=params)

    def get(self, webhook_id: str) -> dict[str, Any]:
        """Retrieve a single webhook."""
        return self._get(f"{self.BASE_PATH}/{webhook_id}")

    def update(self, webhook_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update an existing webhook.

        Args:
            webhook_id: Webhook identifier.
            **kwargs: Fields to update (url, email, enabled, interrupted,
                      apiVersion, authToken, events).

        Returns:
            Updated webhook data.
        """
        return self._put(f"{self.BASE_PATH}/{webhook_id}", json=kwargs)

    def delete(self, webhook_id: str) -> dict[str, Any]:
        """Remove a webhook."""
        return self._delete(f"{self.BASE_PATH}/{webhook_id}")

    def remove_backoff(self, webhook_id: str) -> dict[str, Any]:
        """Remove penalty/backoff from a webhook."""
        return self._post(f"{self.BASE_PATH}/{webhook_id}/removeBackoff", json={})
