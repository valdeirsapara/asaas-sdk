"""Payment links resource."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class PaymentLinks(Resource):
    """Manage payment links (links de pagamento) in the Asaas platform.

    Endpoints:
        POST   /v3/paymentLinks                                       - Create link
        GET    /v3/paymentLinks                                       - List links
        GET    /v3/paymentLinks/:id                                   - Retrieve link
        PUT    /v3/paymentLinks/:id                                   - Update link
        DELETE /v3/paymentLinks/:id                                   - Delete link
        POST   /v3/paymentLinks/:id/restore                           - Restore link
        POST   /v3/paymentLinks/:id/images                            - Add image
        GET    /v3/paymentLinks/:id/images                            - List images
        GET    /v3/paymentLinks/:linkId/images/:imageId               - Get image
        PUT    /v3/paymentLinks/:linkId/images/:imageId/setAsMain     - Set main image
        DELETE /v3/paymentLinks/:linkId/images/:imageId               - Delete image
    """

    BASE_PATH = "/v3/paymentLinks"

    # ---- CRUD ----

    def create(self, **kwargs: Any) -> dict[str, Any]:
        """Create a new payment link.

        Args:
            **kwargs: Payment link fields. Commonly used keys include:
                name, description, endDate, value, billingType,
                chargeType (DETACHED, RECURRENT, INSTALLMENT),
                dueDateLimitDays, subscriptionCycle, maxInstallmentCount,
                notificationEnabled, externalReference, etc.

        Returns:
            Created payment link data.
        """
        return self._post(self.BASE_PATH, json=kwargs)

    def list(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
        active: bool | None = None,
        include_deleted: bool | None = None,
        name: str | None = None,
        external_reference: str | None = None,
    ) -> PaginatedResponse:
        """List payment links (single page).

        Args:
            offset: Page offset.
            limit: Page size.
            active: Filter by active status.
            include_deleted: Include deleted links in results.
            name: Filter by name.
            external_reference: Filter by external reference.

        Returns:
            Paginated response with payment link data.
        """
        params: dict[str, Any] = {}
        _set(params, "offset", offset)
        _set(params, "limit", limit)
        _set(params, "active", active)
        _set(params, "includeDeleted", include_deleted)
        _set(params, "name", name)
        _set(params, "externalReference", external_reference)
        return self._list(self.BASE_PATH, params=params)

    def get(self, link_id: str) -> dict[str, Any]:
        """Retrieve a single payment link by ID.

        Args:
            link_id: Payment link identifier.

        Returns:
            Payment link data.
        """
        return self._get(f"{self.BASE_PATH}/{link_id}")

    def update(self, link_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update an existing payment link.

        Args:
            link_id: Payment link identifier.
            **kwargs: Fields to update (e.g. name, description,
                endDate, value, billingType, chargeType,
                dueDateLimitDays, notificationEnabled,
                externalReference, etc.).

        Returns:
            Updated payment link data.
        """
        return self._put(f"{self.BASE_PATH}/{link_id}", json=kwargs)

    def delete(self, link_id: str) -> dict[str, Any]:
        """Delete a payment link.

        Args:
            link_id: Payment link identifier.

        Returns:
            Deletion confirmation.
        """
        return self._delete(f"{self.BASE_PATH}/{link_id}")

    # ---- Actions ----

    def restore(self, link_id: str) -> dict[str, Any]:
        """Restore a previously deleted payment link.

        Args:
            link_id: Payment link identifier.

        Returns:
            Restored payment link data.
        """
        return self._post(f"{self.BASE_PATH}/{link_id}/restore", json={})

    # ---- Images ----

    def add_image(self, link_id: str, file: Any) -> dict[str, Any]:
        """Add an image to a payment link.

        Args:
            link_id: Payment link identifier.
            file: File-like object or tuple (filename, file_obj, content_type).

        Returns:
            Uploaded image data.
        """
        files = {"file": file}
        return self._http.request(
            "POST",
            f"{self.BASE_PATH}/{link_id}/images",
            files=files,
        )

    def list_images(self, link_id: str) -> dict[str, Any]:
        """List images for a payment link.

        Args:
            link_id: Payment link identifier.

        Returns:
            Images data.
        """
        return self._get(f"{self.BASE_PATH}/{link_id}/images")

    def get_image(self, link_id: str, image_id: str) -> dict[str, Any]:
        """Retrieve a specific image from a payment link.

        Args:
            link_id: Payment link identifier.
            image_id: Image identifier.

        Returns:
            Image data.
        """
        return self._get(f"{self.BASE_PATH}/{link_id}/images/{image_id}")

    def set_main_image(self, link_id: str, image_id: str) -> dict[str, Any]:
        """Set an image as the main image for a payment link.

        Args:
            link_id: Payment link identifier.
            image_id: Image identifier.

        Returns:
            Updated image data.
        """
        return self._put(f"{self.BASE_PATH}/{link_id}/images/{image_id}/setAsMain", json={})

    def delete_image(self, link_id: str, image_id: str) -> dict[str, Any]:
        """Delete an image from a payment link.

        Args:
            link_id: Payment link identifier.
            image_id: Image identifier.

        Returns:
            Deletion confirmation.
        """
        return self._delete(f"{self.BASE_PATH}/{link_id}/images/{image_id}")
