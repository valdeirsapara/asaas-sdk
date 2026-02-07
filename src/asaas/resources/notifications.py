"""Notifications resource."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class Notifications(Resource):
    """Manage notifications (notificacoes) in the Asaas platform.

    Endpoints:
        PUT /v3/notifications/:id   - Update a notification
        PUT /v3/notifications/batch - Update notifications in batch
    """

    BASE_PATH = "/v3/notifications"

    def update(self, notification_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update a single notification.

        Args:
            notification_id: Notification identifier.
            **kwargs: Notification fields to update (e.g. enabled,
                emailEnabledForProvider, smsEnabledForProvider,
                emailEnabledForCustomer, smsEnabledForCustomer,
                phoneCallEnabledForCustomer, whatsappEnabledForCustomer,
                scheduleOffset, etc.).

        Returns:
            Updated notification data.
        """
        return self._put(f"{self.BASE_PATH}/{notification_id}", json=kwargs)

    def update_batch(self, notifications: list[dict[str, Any]]) -> dict[str, Any]:
        """Update multiple notifications in batch.

        Args:
            notifications: List of notification dicts, each containing
                at minimum an ``id`` field along with the fields to update
                (e.g. enabled, emailEnabledForProvider, etc.).

        Returns:
            Batch update result data.
        """
        return self._put(f"{self.BASE_PATH}/batch", json=notifications)
