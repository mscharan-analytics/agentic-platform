from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


@dataclass(slots=True)
class JiraStory:
    key: str
    summary: str
    acceptance_criteria: list[str]


class JiraConnector:
    """Jira story intake with API-first behavior and simulation fallback."""

    def __init__(self, base_url: str, project_key: str, token_ref: str = "") -> None:
        self.base_url = base_url.rstrip("/")
        self.project_key = project_key
        self.token_ref = token_ref or "JIRA_API_TOKEN"

    def _headers(self) -> dict[str, str]:
        token = os.getenv(self.token_ref, "")
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _simulate(self, max_items: int) -> list[JiraStory]:
        return [
            JiraStory(
                key=f"{self.project_key}-1",
                summary="Sample story from Jira",
                acceptance_criteria=["AC1", "AC2"],
            )
        ][:max_items]

    @staticmethod
    def _extract_acceptance_criteria(item: dict[str, Any]) -> list[str]:
        fields = item.get("fields", {})
        candidates = [
            fields.get("customfield_acceptance_criteria"),
            fields.get("acceptanceCriteria"),
            fields.get("description"),
        ]
        for candidate in candidates:
            if isinstance(candidate, list):
                criteria = [str(c).strip() for c in candidate if str(c).strip()]
                if criteria:
                    return criteria
            if isinstance(candidate, str) and candidate.strip():
                return [line.strip() for line in candidate.splitlines() if line.strip()][:5]
        return []

    def _fetch_stories_sync(self, max_items: int) -> list[JiraStory]:
        jql = quote(f"project={self.project_key} ORDER BY updated DESC")
        url = f"{self.base_url}/rest/api/3/search?jql={jql}&maxResults={max_items}"
        request = Request(url, headers=self._headers(), method="GET")

        with urlopen(request, timeout=15) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))

        issues = payload.get("issues", [])
        stories: list[JiraStory] = []
        for issue in issues:
            fields = issue.get("fields", {})
            stories.append(
                JiraStory(
                    key=str(issue.get("key", "")),
                    summary=str(fields.get("summary", "")).strip() or "Untitled",
                    acceptance_criteria=self._extract_acceptance_criteria(issue),
                )
            )
        return stories

    async def fetch_stories(self, max_items: int = 20) -> list[JiraStory]:
        try:
            stories = await asyncio.to_thread(self._fetch_stories_sync, max_items)
            if stories:
                return stories
        except (HTTPError, URLError, OSError, TimeoutError, json.JSONDecodeError):
            pass

        return self._simulate(max_items)
