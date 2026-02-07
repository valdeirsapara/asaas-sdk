"""Asaas SDK - Python SDK for the Asaas payment platform API v3."""

from .client import Asaas
from .exceptions import (
    AsaasAPIError,
    AsaasAuthenticationError,
    AsaasConnectionError,
    AsaasError,
    AsaasNotFoundError,
    AsaasRateLimitError,
    AsaasTimeoutError,
    AsaasValidationError,
)
from .pagination import PaginatedResponse

__version__ = "1.0.0"

__all__ = [
    "Asaas",
    "AsaasAPIError",
    "AsaasAuthenticationError",
    "AsaasConnectionError",
    "AsaasError",
    "AsaasNotFoundError",
    "AsaasRateLimitError",
    "AsaasTimeoutError",
    "AsaasValidationError",
    "PaginatedResponse",
]
