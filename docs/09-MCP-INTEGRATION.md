# MCP Integration Guide

## Overview

The enterprise-agent-platform uses **Model Context Protocol (MCP)** as the abstraction layer for all external integrations. This provides:

- Clean separation between agents and external service APIs
- Centralized tool registry and lifecycle management  
- Consistent error handling and fallback strategies
- Natural extension point for new integrations
- FastMCP-compatible tooling for Claude/other clients

## Architecture

### Client/Server Pattern

```
Agent ──calls──> MCPClient ──routes──> Tool Implementation ──calls──> External Service
                                                       └──fallback──> Simulation
```

### Registered Tools

#### Integration Tools (Requirements Intake)
- `fetch_jira_stories(project_key, max_items)` — Fetch stories from Jira project
- `fetch_figma_spec(file_key)` — Fetch design spec from Figma file
- `fetch_lucid_diagram(doc_id)` — Fetch architecture diagram from Lucid

#### Validation Tools (Go/No-Go)
- `run_static_analysis(tools)` — Execute ruff/mypy/eslint and return findings

#### Deployment Tools (CI/CD)
- `trigger_github_actions(workflow, ref)` — Dispatch GitHub Actions workflow
- `trigger_azure_devops(pipeline, branch)` — Trigger Azure DevOps pipeline run
- `trigger_jenkins(job_name, branch)` — Trigger Jenkins build

## Usage in Agents

All agents use MCP tools through the client:

```python
from agent_platform.mcp.client import get_mcp_client

class MyAgent(BaseAgent):
    async def run(self, task: Task, context=None) -> AgentResult:
        mcp = get_mcp_client()
        
        # Call any registered tool
        result = await mcp.call_tool("fetch_jira_stories", 
                                    project_key="DEMO", 
                                    max_items=10)
        
        return AgentResult(status="ok", data=result)
```

## Environment Configuration

Each tool respects environment variables for API configuration:

### Jira
- `JIRA_BASE_URL` — Base URL (default: https://example.atlassian.net)
- `JIRA_PROJECT_KEY` — Project key (default: DEMO)
- `JIRA_API_TOKEN` — API token for auth

### Figma
- `FIGMA_API_TOKEN` — Personal access token
- `FIGMA_FILE_KEY` — File key (can override per-call)

### Lucid
- `LUCID_API_TOKEN` — API token
- `LUCID_DOC_ID` — Document ID (can override per-call)

### GitHub Actions
- `GITHUB_REPOSITORY` — Format: owner/repo
- `GITHUB_TOKEN` — Personal access token
- `GITHUB_API_BASE` — API base URL (default: https://api.github.com)

### Azure DevOps
- `AZDO_ORG_URL` — Organization URL
- `AZDO_PROJECT` — Project name
- `AZDO_PIPELINE_ID` — Pipeline ID
- `AZDO_PAT` — Personal access token

### Jenkins
- `JENKINS_URL` — Base URL
- `JENKINS_USER` — Username
- `JENKINS_API_TOKEN` — API token
- `JENKINS_JOB` — Default job name

## Fallback Behavior

All tools gracefully degrade when credentials/config are missing or API calls fail:

- **Integrations**: Return simulated sample data (Jira stories, Figma specs, Lucid diagrams)
- **Validation**: Return `tool_missing` or `unknown_tool` status  
- **Deployment**: Return `simulated` status instead of actual trigger

This enables local development and testing without requiring external service access.

## FastMCP Server Registration

Tools are also registered with the FastMCP server for Claude/other client integration:

```python
mcp = FastMCP("enterprise-agent-platform")

@mcp.tool(name="fetch_jira_stories")
async def fetch_jira_stories(project_key: str, max_items: int = 20):
    return await IntegrationTools.fetch_jira_stories(project_key, max_items)

# ... similar for all other tools
```

Run the server with:
```bash
python -m agent_platform.mcp.server
```

## Adding New Tools

To add a new integration tool:

1. Create a static method in `integrations.py`, `validation_deployment.py`, or a new MCP module
2. Register it in `mcp/__init__.py` with `client.register_tool()`
3. Add the FastMCP decorator in `mcp/server.py`
4. Use it in agents via `get_mcp_client().call_tool()`

Example:

```python
# In mcp/integrations.py
@staticmethod
async def fetch_slack_messages(channel: str) -> dict[str, object]:
    """Fetch recent messages from Slack channel."""
    # Implementation
    pass

# In mcp/__init__.py
client.register_tool("fetch_slack_messages", IntegrationTools.fetch_slack_messages)

# In mcp/server.py
@mcp.tool(name="fetch_slack_messages")
async def fetch_slack_messages(channel: str) -> dict[str, object]:
    return await IntegrationTools.fetch_slack_messages(channel)

# In any agent
result = await mcp.call_tool("fetch_slack_messages", channel="general")
```
