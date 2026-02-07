"""Base resource class."""

from __future__ import annotations

from typing import Any, Generator

from ..http_client import HttpClient
from ..pagination import PaginatedResponse, paginate


class Resource:
    """Base class for all API resources."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def _get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        return self._http.get(path, **kwargs)

    def _post(self, path: str, **kwargs: Any) -> dict[str, Any]:
        return self._http.post(path, **kwargs)

    def _put(self, path: str, **kwargs: Any) -> dict[str, Any]:
        return self._http.put(path, **kwargs)

    def _delete(self, path: str, **kwargs: Any) -> dict[str, Any]:
        return self._http.delete(path, **kwargs)

    def _list(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> PaginatedResponse:
        """Fetch a single page of results."""
        raw = self._http.get(path, params=params)
        return PaginatedResponse(raw)

    def _list_all(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        limit: int = 100,
        max_items: int | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Auto-paginate through all results."""
        return paginate(self._http, path, params=params, limit=limit, max_items=max_items)
