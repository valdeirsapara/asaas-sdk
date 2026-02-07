"""Pagination utilities for the Asaas SDK."""

from __future__ import annotations

from typing import Any, Generator, TYPE_CHECKING

if TYPE_CHECKING:
    from .http_client import HttpClient


class PaginatedResponse:
    """Wraps a paginated list response from the Asaas API.

    Attributes:
        has_more: Whether there are more pages available.
        total_count: Total number of records matching the query.
        limit: Number of records per page.
        offset: Current offset.
        data: List of records in the current page.
    """

    def __init__(self, raw: dict[str, Any]) -> None:
        self.has_more: bool = raw.get("hasMore", False)
        self.total_count: int = raw.get("totalCount", 0)
        self.limit: int = raw.get("limit", 10)
        self.offset: int = raw.get("offset", 0)
        self.data: list[dict[str, Any]] = raw.get("data", [])

    def __repr__(self) -> str:
        return (
            f"PaginatedResponse(total_count={self.total_count}, "
            f"offset={self.offset}, limit={self.limit}, "
            f"has_more={self.has_more}, items={len(self.data)})"
        )


def paginate(
    http: HttpClient,
    path: str,
    params: dict[str, Any] | None = None,
    limit: int = 100,
    max_items: int | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Auto-paginate through all pages of a list endpoint.

    Args:
        http: The HTTP client instance.
        path: API endpoint path.
        params: Additional query parameters.
        limit: Number of items per page.
        max_items: Maximum total items to return. None for all.

    Yields:
        Individual records from the API.
    """
    offset = 0
    yielded = 0
    base_params = dict(params or {})

    while True:
        page_params = {**base_params, "offset": offset, "limit": limit}
        response = http.get(path, params=page_params)
        page = PaginatedResponse(response)

        for item in page.data:
            yield item
            yielded += 1
            if max_items is not None and yielded >= max_items:
                return

        if not page.has_more:
            return

        offset += page.limit
