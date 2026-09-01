"""Client for the STFC.cfd events API (https://stfc-cfd-api.fly.dev).

STFC.cfd's calendar (https://stfc.cfd) is a client-rendered React app that
loads its data from this JSON API, so this talks to the API directly
rather than scraping the frontend.
"""

from __future__ import annotations

from typing import Any, ClassVar

import requests


class Client:
    """Talks to the STFC.cfd events API over raw HTTP/JSON."""

    DEFAULT_API_URL: ClassVar[str] = "https://stfc-cfd-api.fly.dev"
    DEFAULT_TIMEOUT: ClassVar[float] = 10.0
    _EVENTS_PATH: ClassVar[str] = "/api/events"
    _USER_AGENT: ClassVar[str] = "stfcdailybot/0.1 (+https://github.com/infamous-lamer/stfcdailybot)"

    def __init__(self, base_url: str = DEFAULT_API_URL) -> None:
        self.base_url = base_url

    def fetch_events(self, *, timeout: float = DEFAULT_TIMEOUT) -> list[dict[str, Any]]:
        """Fetch the raw event list from the API as parsed JSON."""
        response = requests.get(
            f"{self.base_url}{self._EVENTS_PATH}",
            headers={"User-Agent": self._USER_AGENT},
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
