"""Wallets resource."""

from __future__ import annotations

from typing import Any

from .base import Resource


class Wallets(Resource):
    """Retrieve wallet information from the Asaas platform."""

    BASE_PATH = "/v3/wallets"

    def get(self) -> dict[str, Any]:
        """Retrieve the wallet ID for the current account.

        Returns:
            Wallet data including walletId.
        """
        return self._get(self.BASE_PATH + "/")
