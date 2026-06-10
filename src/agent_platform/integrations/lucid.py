from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(slots=True)
class LucidDiagram:
    doc_id: str
    components: list[str]


class LucidConnector:
    """Lucid architecture intake with API-first behavior and simulation fallback."""

    def __init__(self, base_url: str = "https://api.lucid.co", token_ref: str = "") -> None:
        self.base_url = base_url.rstrip("/")
        self.token_ref = token_ref or "LUCID_API_TOKEN"

    def _simulate(self, doc_id: str) -> LucidDiagram:
        return LucidDiagram(doc_id=doc_id, components=["frontend", "backend", "database"])

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        token = os.getenv(self.token_ref, "")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _fetch_diagram_sync(self, doc_id: str) -> LucidDiagram:
        request = Request(f"{self.base_url}/documents/{doc_id}", headers=self._headers(), method="GET")
        with urlopen(request, timeout=15) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))

        shapes = payload.get("shapes", [])
        components = []
        if isinstance(shapes, list):
            components = [str(shape.get("name", "")).strip() for shape in shapes if shape.get("name")]
        if not components:
            components = ["frontend", "backend", "database"]
        return LucidDiagram(doc_id=doc_id, components=components)

    async def fetch_diagram(self, doc_id: str) -> LucidDiagram:
        try:
            return await asyncio.to_thread(self._fetch_diagram_sync, doc_id)
        except (HTTPError, URLError, OSError, TimeoutError, json.JSONDecodeError):
            return self._simulate(doc_id)
