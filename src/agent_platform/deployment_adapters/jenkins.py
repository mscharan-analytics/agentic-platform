from __future__ import annotations

import asyncio
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class JenkinsAdapter:
    """Deployment adapter for Jenkins build triggers."""

    def __init__(self) -> None:
        self.base_url = os.getenv("JENKINS_URL", "").rstrip("/")
        self.user = os.getenv("JENKINS_USER", "")
        self.token = os.getenv("JENKINS_API_TOKEN", "")
        self.job_default = os.getenv("JENKINS_JOB", "")

    def _trigger_sync(self, job_name: str, branch: str) -> dict[str, object]:
        effective_job = self.job_default or job_name
        if not self.base_url:
            return {
                "platform": "jenkins",
                "job": effective_job,
                "branch": branch,
                "status": "simulated",
                "reason": "missing_config",
            }

        query = urlencode({"BRANCH": branch})
        url = f"{self.base_url}/job/{effective_job}/buildWithParameters?{query}"
        request = Request(url, method="POST")
        if self.user and self.token:
            import base64

            auth = base64.b64encode(f"{self.user}:{self.token}".encode("utf-8")).decode("utf-8")
            request.add_header("Authorization", f"Basic {auth}")

        with urlopen(request, timeout=15):  # noqa: S310
            return {
                "platform": "jenkins",
                "job": effective_job,
                "branch": branch,
                "status": "triggered",
            }

    async def trigger(self, job_name: str, branch: str) -> dict[str, object]:
        try:
            return await asyncio.to_thread(self._trigger_sync, job_name, branch)
        except (HTTPError, URLError, OSError):
            return {
                "platform": "jenkins",
                "job": job_name,
                "branch": branch,
                "status": "simulated",
                "reason": "dispatch_failed",
            }
