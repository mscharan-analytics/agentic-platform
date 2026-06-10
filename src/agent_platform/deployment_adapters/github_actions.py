from __future__ import annotations

import asyncio
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class GitHubActionsAdapter:
    """Deployment adapter for GitHub Actions workflow dispatch."""

    def __init__(self) -> None:
        self.api_base = os.getenv("GITHUB_API_BASE", "https://api.github.com").rstrip("/")
        self.repo = os.getenv("GITHUB_REPOSITORY", "")
        self.token = os.getenv("GITHUB_TOKEN", "")

    def _dispatch_sync(self, workflow: str, ref: str) -> dict[str, object]:
        if not self.repo or not self.token:
            return {
                "platform": "github_actions",
                "workflow": workflow,
                "ref": ref,
                "status": "simulated",
                "reason": "missing_config",
            }

        url = f"{self.api_base}/repos/{self.repo}/actions/workflows/{workflow}/dispatches"
        payload = json.dumps({"ref": ref}).encode("utf-8")
        request = Request(
            url,
            data=payload,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urlopen(request, timeout=15):  # noqa: S310
            return {
                "platform": "github_actions",
                "workflow": workflow,
                "ref": ref,
                "status": "triggered",
            }

    async def trigger(self, workflow: str, ref: str) -> dict[str, object]:
        try:
            return await asyncio.to_thread(self._dispatch_sync, workflow, ref)
        except (HTTPError, URLError, OSError):
            return {
                "platform": "github_actions",
                "workflow": workflow,
                "ref": ref,
                "status": "simulated",
                "reason": "dispatch_failed",
            }
