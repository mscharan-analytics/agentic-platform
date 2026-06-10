from __future__ import annotations

import asyncio
import base64
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class AzureDevOpsAdapter:
    """Deployment adapter for Azure DevOps pipeline runs."""

    def __init__(self) -> None:
        self.org_url = os.getenv("AZDO_ORG_URL", "").rstrip("/")
        self.project = os.getenv("AZDO_PROJECT", "")
        self.pipeline_id = os.getenv("AZDO_PIPELINE_ID", "")
        self.pat = os.getenv("AZDO_PAT", "")

    def _trigger_sync(self, pipeline: str, branch: str) -> dict[str, object]:
        effective_pipeline = self.pipeline_id or pipeline
        if not self.org_url or not self.project or not self.pat:
            return {
                "platform": "azure_devops",
                "pipeline": effective_pipeline,
                "branch": branch,
                "status": "simulated",
                "reason": "missing_config",
            }

        url = (
            f"{self.org_url}/{self.project}/_apis/pipelines/{effective_pipeline}/runs"
            f"?api-version=7.1-preview.1"
        )
        auth = base64.b64encode(f":{self.pat}".encode("utf-8")).decode("utf-8")
        payload = json.dumps({"resources": {"repositories": {"self": {"refName": f"refs/heads/{branch}"}}}}).encode(
            "utf-8"
        )
        request = Request(
            url,
            data=payload,
            headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=20):  # noqa: S310
            return {
                "platform": "azure_devops",
                "pipeline": effective_pipeline,
                "branch": branch,
                "status": "triggered",
            }

    async def trigger(self, pipeline: str, branch: str) -> dict[str, object]:
        try:
            return await asyncio.to_thread(self._trigger_sync, pipeline, branch)
        except (HTTPError, URLError, OSError):
            return {
                "platform": "azure_devops",
                "pipeline": pipeline,
                "branch": branch,
                "status": "simulated",
                "reason": "dispatch_failed",
            }
