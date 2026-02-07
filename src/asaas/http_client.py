"""Low-level HTTP client with retry, logging, and error handling."""

from __future__ import annotations

import logging
import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    AsaasConnectionError,
    AsaasTimeoutError,
    raise_for_status,
)

logger = logging.getLogger("asaas")

PRODUCTION_URL = "https://api.asaas.com"
SANDBOX_URL = "https://sandbox.asaas.com/api"


class HttpClient:
    """HTTP transport layer for the Asaas SDK."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self._session = requests.Session()
        self._session.headers.update(
            {
                "access_token": self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "asaas-python-sdk/1.0.0",
            }
        )

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "PUT", "DELETE", "HEAD", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: Any = None,
        files: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Execute an HTTP request and return parsed JSON."""
        url = f"{self.base_url}{path}"

        req_headers = {}
        if headers:
            req_headers.update(headers)

        # For file uploads, remove Content-Type so requests sets multipart boundary
        if files:
            req_headers["Content-Type"] = None  # type: ignore[assignment]

        logger.debug("%s %s params=%s json=%s", method, url, params, json)
        start = time.monotonic()

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=_clean_params(params),
                json=json if not files else None,
                data=data,
                files=files,
                headers=req_headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout as exc:
            raise AsaasTimeoutError(f"Request timed out: {exc}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise AsaasConnectionError(f"Connection error: {exc}") from exc

        elapsed = time.monotonic() - start
        logger.debug(
            "%s %s -> %s (%.2fs)", method, url, response.status_code, elapsed
        )

        body: dict[str, Any] = {}
        if response.content:
            try:
                body = response.json()
            except ValueError:
                body = {"raw": response.text}

        raise_for_status(response.status_code, body)
        return body

    def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> dict[str, Any]:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> dict[str, Any]:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> dict[str, Any]:
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        self._session.close()


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    """Remove None values from query parameters."""
    if params is None:
        return None
    return {k: v for k, v in params.items() if v is not None}
