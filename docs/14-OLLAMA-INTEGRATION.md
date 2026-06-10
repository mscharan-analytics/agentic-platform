# Ollama Integration Guide

## Overview

The Enterprise Agent Platform integrates **Ollama** as a local-first model inference service, with graceful fallback to optional cloud providers (OpenAI, Claude, etc.).

**Key design principles:**
- ✅ **Local-first** — Prioritize local Ollama deployment
- ✅ **Optional** — Ollama not required for the platform to run
- ✅ **Graceful degradation** — If Ollama unavailable, platform continues with fallback
- ✅ **Docker-friendly** — docker-compose orchestrates Ollama alongside the platform

---

## Installation

### Option A: With Ollama Support (Recommended)

```bash
# Install platform with Ollama integration
pip install enterprise-agent-platform[ollama]

# Or install all optional features
pip install enterprise-agent-platform[all]
```

**What this installs:**
- `ollama>=0.1.0` — Python client for Ollama API
- `httpx>=0.24.0` — Async HTTP client for service checks
- `enterprise-agent-platform` core

### Option B: Without Ollama (Minimal)

```bash
# Install just the core platform
pip install enterprise-agent-platform

# Platform will run but cannot connect to Ollama
# You must configure a cloud provider as fallback
```

**When to use:**
- You're deploying to a cloud-only environment (AWS, Azure, GCP)
- You want to use only cloud LLM providers (OpenAI, Claude, etc.)
- You have a separate Ollama deployment not accessible from the platform

---

## Docker Deployment

### Quick Start with docker-compose

```bash
cd enterprise-agent-platform/deployment/docker
docker-compose up
```

**What this does:**
1. Builds the platform Docker image (includes ollama dependency)
2. Pulls the `ollama/ollama:latest` image
3. Starts both services
4. Platform waits for Ollama to be healthy before starting
5. Loads `llama2` model into Ollama (configured in OLLAMA_MODELS env var)

**docker-compose.yml highlights:**
```yaml
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"  # Ollama API endpoint
    healthcheck:       # Ensures Ollama ready before platform starts
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]

  agent-platform:
    depends_on:
      ollama:
        condition: service_healthy  # Wait for health check
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
```

### Custom Configuration

Set environment variables before `docker-compose up`:

```bash
# Specify which models to pull into Ollama
export OLLAMA_MODELS=llama2,mistral,neural-chat

# Keep models in memory for 1 hour
export OLLAMA_KEEP_ALIVE=1h

# Limit Ollama memory usage (Docker)
export OLLAMA_MEMORY_LIMIT=8GB

# Disable GPU (useful for CPU-only machines)
export OLLAMA_GPU_ENABLED=false

docker-compose up
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama service endpoint (docker-compose uses `http://ollama:11434`) |
| `OLLAMA_MODELS` | `llama2` | Comma-separated list of models to pull on startup |
| `OLLAMA_KEEP_ALIVE` | `30m` | How long to keep models in memory (30m, 1h, etc.) |
| `OLLAMA_GPU_ENABLED` | `true` | Enable GPU acceleration if available |
| `OLLAMA_MEMORY_LIMIT` | `none` | Max memory for Ollama process (e.g., "8GB") |

### Python Configuration

```python
from agent_platform.deployment_adapters import OllamaDeploymentAdapter, OllamaConfig

# Custom configuration
config = OllamaConfig(
    base_url="http://localhost:11434",
    models=["llama2", "mistral", "neural-chat"],
    keep_alive="1h",
    gpu_enabled=True,
)

adapter = OllamaDeploymentAdapter(config)
await adapter.initialize()
```

---

## Model Management

### Available MCP Tools

Agents can query and manage Ollama via MCP tools:

```python
from agent_platform.mcp.client import get_mcp_client

mcp = get_mcp_client()

# List all downloaded models
models = await mcp.call_tool("ollama_list_models")

# Check if a specific model is available
status = await mcp.call_tool("ollama_check_model", model_name="mistral")

# Get Ollama service health
health = await mcp.call_tool("ollama_health")

# Get service configuration
info = await mcp.call_tool("ollama_info")
```

### Pulling New Models

Pull models directly into your Ollama instance:

```bash
# From command line
ollama pull llama2
ollama pull mistral
ollama pull neural-chat

# Or via Python
from agent_platform.deployment_adapters import OllamaDeploymentAdapter

adapter = OllamaDeploymentAdapter()
await adapter.initialize()
results = await adapter.pull_models()
```

---

## Graceful Fallback Behavior

### What Happens If Ollama Is Unavailable

The platform does **not fail**. Instead:

1. **Detection** — Platform checks Ollama availability at startup and on first use
2. **Logging** — Warnings logged to help you debug:
   ```
   ✗ Cannot connect to Ollama at http://localhost:11434
   Platform will use fallback LLM routing (degraded mode)
   ```
3. **Fallback routing** — In priority order:
   - ✅ If cloud provider configured → use it (OpenAI, Claude, etc.)
   - ⚠️ Otherwise → return stub responses (degraded mode)

### Example Response in Degraded Mode

```python
from agent_platform.model_gateway import get_model_gateway

gateway = get_model_gateway()

# If Ollama unavailable and no cloud provider configured:
response = await gateway.invoke("What is AI?")

print(response.content)
# Output: "[DEGRADED MODE] Ollama unavailable. Prompt: What is AI? 
#          (Deploy Ollama or configure cloud provider)"
```

### Configuring Cloud Provider Fallback

```python
from agent_platform.model_gateway import get_model_gateway, ModelProvider

gateway = get_model_gateway()

# Register cloud fallback
gateway.set_cloud_provider(
    provider=ModelProvider.OPENAI,
    api_key="sk-..."
)

# Now if Ollama unavailable, platform uses OpenAI
response = await gateway.invoke("What is AI?")
```

---

## Performance Tuning

### Model Selection

**For CPU-only machines:**
```bash
export OLLAMA_MODELS=phi,orca-mini
docker-compose up
```

**For machines with 16GB+ RAM:**
```bash
export OLLAMA_MODELS=llama2,mistral,neural-chat,dolphin-mixtral
docker-compose up
```

### Memory Management

```yaml
# In docker-compose.yml
ollama:
  mem_limit: 8GB
  memswap_limit: 8GB
```

### Keep Alive Tuning

- `30m` (default) — Good for development, keeps models ready
- `5m` — Production with frequent model switching
- `1h` — Production with stable model usage
- `0` — Unload models immediately after use (save memory)

---

## Troubleshooting

### Problem: "Ollama not available"

**Check service is running:**
```bash
curl http://localhost:11434/api/tags
# Should return: {"models": [...]}
```

**In docker-compose:**
```bash
docker-compose logs ollama
docker-compose ps  # Check if service is running
```

### Problem: Model takes too long to pull

**Models are large (~7GB for llama2).** First pull may take 5-15 minutes:

```bash
# Watch the pull
ollama pull llama2

# Check progress in docker
docker-compose logs -f ollama
```

### Problem: Out of memory errors

**Reduce models or memory allocation:**
```bash
# Option 1: Fewer models
export OLLAMA_MODELS=llama2
docker-compose up

# Option 2: Increase docker memory
export OLLAMA_MEMORY_LIMIT=16GB
docker-compose up
```

### Problem: GPU not detected

**Check Ollama GPU support:**
```bash
ollama ls  # Should list models with their compute device
```

**If GPU not used:**
```bash
export OLLAMA_GPU_ENABLED=false  # Fall back to CPU
docker-compose up
```

---

## Advanced: Custom Deployment

### Kubernetes Deployment

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: agent-platform
spec:
  containers:
  - name: ollama
    image: ollama/ollama:latest
    ports:
    - containerPort: 11434
    resources:
      requests:
        memory: "8Gi"
        nvidia.com/gpu: "1"  # Optional: request GPU

  - name: platform
    image: enterprise-agent-platform:latest
    env:
    - name: OLLAMA_BASE_URL
      value: "http://localhost:11434"
    depends_on:
    - ollama
```

### Systemd Service

```ini
[Unit]
Description=Enterprise Agent Platform
After=ollama.service

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/agent-platform
Environment="OLLAMA_BASE_URL=http://localhost:11434"
ExecStart=/usr/bin/python -m agent_platform.main

[Install]
WantedBy=multi-user.target
```

---

## Integration with Agents

### Using Models in an Agent

```python
from agent_platform.model_gateway import get_model_gateway

async def my_agent_task():
    gateway = get_model_gateway()
    
    # Ollama handles model routing automatically
    response = await gateway.invoke(
        prompt="Analyze this code and suggest optimizations",
        model="llama2"  # Uses Ollama if available
    )
    
    if "DEGRADED MODE" in response.content:
        logger.warning("Running in degraded mode; consider deploying Ollama")
    
    return response.content
```

### Checking Service Health

```python
from agent_platform.mcp.client import get_mcp_client

async def precheck():
    mcp = get_mcp_client()
    health = await mcp.call_tool("ollama_health")
    
    if not health.get("service_available"):
        logger.warning("Ollama service not ready; using fallback provider")
```

---

## Summary

| Scenario | Installation | Behavior |
|----------|--------------|----------|
| **Local dev + Ollama** | `pip install [ollama]` + docker-compose | ✅ Uses local Ollama |
| **Cloud deployment** | `pip install` (no ollama) | Falls back to cloud provider |
| **Hybrid** | `pip install [ollama]` + cloud config | ✅ Tries Ollama, falls back to cloud |
| **Degraded mode** | Any install, no Ollama running | ⚠️ Stub responses, warnings logged |

**Key takeaway:** The platform is **not dependent** on Ollama but **designed to use it** when available. You can:
- ✅ `pip install` without Ollama dependency — platform still works
- ✅ Deploy Ollama separately (local, docker-compose, Kubernetes)
- ✅ Mix Ollama + cloud providers
- ✅ Scale from single machine to distributed setup without code changes
