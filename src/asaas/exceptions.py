"""Custom exceptions for the Asaas SDK."""

from __future__ import annotations

from typing import Any


class AsaasError(Exception):
    """Base exception for the Asaas SDK."""

    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(self.message)


class AsaasAPIError(AsaasError):
    """Exception raised when the Asaas API returns an error response."""

    def __init__(
        self,
        message: str = "",
        status_code: int | None = None,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        self.status_code = status_code
        self.errors = errors or []
        if not message and self.errors:
            message = "; ".join(
                f"[{e.get('code', 'unknown')}] {e.get('description', '')}"
                for e in self.errors
            )
        super().__init__(message)


class AsaasAuthenticationError(AsaasAPIError):
    """Raised on 401 Unauthorized responses."""


class AsaasNotFoundError(AsaasAPIError):
    """Raised on 404 Not Found responses."""


class AsaasValidationError(AsaasAPIError):
    """Raised on 400 Bad Request responses (validation errors)."""


class AsaasRateLimitError(AsaasAPIError):
    """Raised on 429 Too Many Requests responses."""


class AsaasTimeoutError(AsaasError):
    """Raised when a request times out."""


class AsaasConnectionError(AsaasError):
    """Raised when a connection error occurs."""


_STATUS_CODE_MAP: dict[int, type[AsaasAPIError]] = {
    400: AsaasValidationError,
    401: AsaasAuthenticationError,
    404: AsaasNotFoundError,
    429: AsaasRateLimitError,
}


def raise_for_status(status_code: int, body: dict[str, Any] | None = None) -> None:
    """Raise the appropriate exception based on HTTP status code."""
    if 200 <= status_code < 300:
        return

    errors = (body or {}).get("errors", [])
    message = ""
    if errors:
        message = "; ".join(
            f"[{e.get('code', 'unknown')}] {e.get('description', '')}"
            for e in errors
        )
    else:
        message = f"HTTP {status_code}"

    exc_class = _STATUS_CODE_MAP.get(status_code, AsaasAPIError)
    raise exc_class(message=message, status_code=status_code, errors=errors)
