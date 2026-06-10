from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(slots=True)
class FigmaSpec:
    file_key: str
    screen_count: int
    notes: list[str]


class FigmaConnector:
    """Figma requirements intake with API-first behavior and simulation fallback."""

    def __init__(self, base_url: str = "https://api.figma.com", token_ref: str = "") -> None:
        self.base_url = base_url.rstrip("/")
        self.token_ref = token_ref or "FIGMA_API_TOKEN"

    def _simulate(self, file_key: str) -> FigmaSpec:
        return FigmaSpec(file_key=file_key, screen_count=3, notes=["Primary user flow", "Validation states"])

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        token = os.getenv(self.token_ref, "")
        if token:
            headers["X-Figma-Token"] = token
        return headers

    def _fetch_spec_sync(self, file_key: str) -> FigmaSpec:
        request = Request(f"{self.base_url}/v1/files/{file_key}", headers=self._headers(), method="GET")
        with urlopen(request, timeout=15) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))

        document = payload.get("document", {})
        children = document.get("children", []) if isinstance(document, dict) else []
        screen_count = len(children)
        notes = [f"Figma file: {payload.get('name', file_key)}", f"Top-level frames: {screen_count}"]
        return FigmaSpec(file_key=file_key, screen_count=screen_count, notes=notes)

    async def fetch_spec(self, file_key: str) -> FigmaSpec:
        try:
            return await asyncio.to_thread(self._fetch_spec_sync, file_key)
        except (HTTPError, URLError, OSError, TimeoutError, json.JSONDecodeError):
            return self._simulate(file_key)
