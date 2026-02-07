"""My account resource."""

from __future__ import annotations

from typing import Any

from .base import Resource
from ..pagination import PaginatedResponse


def _set(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


class MyAccount(Resource):
    """Manage account settings (minha conta) in the Asaas platform.

    Endpoints:
        GET    /v3/myAccount/commercialInfo/          - Get commercial info
        POST   /v3/myAccount/commercialInfo/          - Update commercial info
        POST   /v3/myAccount/paymentCheckoutConfig/   - Save checkout config
        GET    /v3/myAccount/paymentCheckoutConfig/   - Get checkout config
        GET    /v3/myAccount/accountNumber             - Get account number
        GET    /v3/myAccount/fees/                     - Get fees
        GET    /v3/myAccount/status/                   - Get account status
        POST   /v3/myAccount/documents/:id             - Upload document
        GET    /v3/myAccount/documents                 - List pending documents
        GET    /v3/myAccount/documents/files/:id       - Get document file
        POST   /v3/myAccount/documents/files/:id       - Update document file
        DELETE /v3/myAccount/documents/files/:id       - Delete document file
        DELETE /v3/myAccount/                          - Delete account
    """

    BASE_PATH = "/v3/myAccount"

    # ---- Commercial Info ----

    def get_commercial_info(self) -> dict[str, Any]:
        """Retrieve commercial information for the account.

        Returns:
            Commercial info data.
        """
        return self._get(f"{self.BASE_PATH}/commercialInfo/")

    def update_commercial_info(self, **kwargs: Any) -> dict[str, Any]:
        """Update commercial information for the account.

        Args:
            **kwargs: Commercial info fields (e.g. personType, cpfCnpj,
                companyName, email, phone, mobilePhone, site, address,
                addressNumber, complement, province, postalCode, etc.).

        Returns:
            Updated commercial info data.
        """
        return self._post(f"{self.BASE_PATH}/commercialInfo/", json=kwargs)

    # ---- Payment Checkout Config ----

    def save_checkout_config(self, **kwargs: Any) -> dict[str, Any]:
        """Save payment checkout configuration.

        Args:
            **kwargs: Checkout config fields (e.g. logoBackgroundColor,
                infoBackgroundColor, fontColor, enabled, logoFile, etc.).

        Returns:
            Saved checkout configuration data.
        """
        return self._post(f"{self.BASE_PATH}/paymentCheckoutConfig/", json=kwargs)

    def get_checkout_config(self) -> dict[str, Any]:
        """Retrieve payment checkout configuration.

        Returns:
            Checkout configuration data.
        """
        return self._get(f"{self.BASE_PATH}/paymentCheckoutConfig/")

    # ---- Account Info ----

    def get_account_number(self) -> dict[str, Any]:
        """Retrieve the account number.

        Returns:
            Account number data.
        """
        return self._get(f"{self.BASE_PATH}/accountNumber")

    def get_fees(self) -> dict[str, Any]:
        """Retrieve the account fee schedule.

        Returns:
            Fee data.
        """
        return self._get(f"{self.BASE_PATH}/fees/")

    def get_status(self) -> dict[str, Any]:
        """Retrieve the account status.

        Returns:
            Account status data.
        """
        return self._get(f"{self.BASE_PATH}/status/")

    # ---- Documents ----

    def upload_document(self, document_id: str, file: Any) -> dict[str, Any]:
        """Upload a document to the account.

        Args:
            document_id: Document group identifier.
            file: File-like object or tuple (filename, file_obj, content_type).

        Returns:
            Uploaded document data.
        """
        files = {"file": file}
        return self._http.request(
            "POST",
            f"{self.BASE_PATH}/documents/{document_id}",
            files=files,
        )

    def list_pending_documents(self) -> dict[str, Any]:
        """List pending documents for the account.

        Returns:
            Pending documents data.
        """
        return self._get(f"{self.BASE_PATH}/documents")

    def get_document_file(self, file_id: str) -> dict[str, Any]:
        """Retrieve a specific document file by ID.

        Args:
            file_id: Document file identifier.

        Returns:
            Document file data.
        """
        return self._get(f"{self.BASE_PATH}/documents/files/{file_id}")

    def update_document_file(self, file_id: str, file: Any) -> dict[str, Any]:
        """Update (replace) an existing document file.

        Args:
            file_id: Document file identifier.
            file: File-like object or tuple (filename, file_obj, content_type).

        Returns:
            Updated document file data.
        """
        files = {"file": file}
        return self._http.request(
            "POST",
            f"{self.BASE_PATH}/documents/files/{file_id}",
            files=files,
        )

    def delete_document_file(self, file_id: str) -> dict[str, Any]:
        """Delete a document file.

        Args:
            file_id: Document file identifier.

        Returns:
            Deletion confirmation.
        """
        return self._delete(f"{self.BASE_PATH}/documents/files/{file_id}")

    # ---- Account Deletion ----

    def delete_account(self, remove_reason: str) -> dict[str, Any]:
        """Delete the account.

        Args:
            remove_reason: Reason for deleting the account.

        Returns:
            Deletion confirmation.
        """
        params: dict[str, Any] = {"removeReason": remove_reason}
        return self._delete(f"{self.BASE_PATH}/", params=params)
