import asyncio

from agent_platform.deployment_adapters import AzureDevOpsAdapter, GitHubActionsAdapter, JenkinsAdapter
from agent_platform.validation import StaticAnalysisAdapter


def test_static_analysis_unknown_tool() -> None:
    adapter = StaticAnalysisAdapter()
    result = asyncio.run(adapter.run(["unknown-tool"]))

    assert len(result) == 1
    assert result[0].status == "unknown_tool"


def test_github_actions_simulated_without_config() -> None:
    adapter = GitHubActionsAdapter()
    result = asyncio.run(adapter.trigger("release.yml", "main"))

    assert result["platform"] == "github_actions"
    assert result["status"] == "simulated"


def test_azure_devops_simulated_without_config() -> None:
    adapter = AzureDevOpsAdapter()
    result = asyncio.run(adapter.trigger("release-pipeline", "main"))

    assert result["platform"] == "azure_devops"
    assert result["status"] == "simulated"


def test_jenkins_simulated_without_config() -> None:
    adapter = JenkinsAdapter()
    result = asyncio.run(adapter.trigger("release-job", "main"))

    assert result["platform"] == "jenkins"
    assert result["status"] == "simulated"
