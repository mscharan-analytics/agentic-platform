# Agent Platform SDK & Web API Guide

## Overview

The Enterprise Agent Platform now includes:

1. **FastAPI Backend** — REST API exposing all platform capabilities
2. **React Web UI** — Dashboard for developers to interact with the platform
3. **TypeScript SDK** — Client library for programmatic access
4. **Docker Compose** — One-command setup for complete stack

---

## Architecture

```
┌─────────────────────────────────────────┐
│  Web UI (React @ localhost:3000)        │
└────────────────┬────────────────────────┘
                 │ HTTP/REST
┌────────────────▼────────────────────────┐
│  API Server (FastAPI @ localhost:8000)  │  ← /api/health, /api/agents, /api/tools, etc.
└────────────────┬────────────────────────┘
                 │ Python imports
┌────────────────▼────────────────────────┐
│  Agent Platform Core                    │  ← Orchestrator, MCP, Model Gateway, Ollama
└─────────────────────────────────────────┘
```

---

## Quick Start

### Option 1: Docker Compose (Easiest)

```bash
cd deployment/docker
docker-compose up
```

This starts:
- ✅ Ollama service (port 11434)
- ✅ Agent Platform API (port 8000)
- ✅ Web UI (port 3000)

**Access:**
- Web UI: http://localhost:3000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Option 2: Manual Setup

```bash
# Terminal 1: Start Python backend
pip install enterprise-agent-platform[api,ollama]
python -m agent_platform.api.server

# Terminal 2: Start Ollama (if not running)
docker run -d -p 11434:11434 ollama/ollama
ollama pull llama2

# Terminal 3: Start React frontend
cd src/web-ui
npm install
npm run dev
```

---

## API Endpoints

### Health & Status

```bash
GET /health
# Response: { "status": "ok", "service": "agent-platform", "version": "0.1.0" }

GET /api/health/status
GET /api/health/ready
```

### Agents

```bash
GET /api/agents/list
# List all available agents

GET /api/agents/{agent_name}
# Get agent details

POST /api/agents/{agent_name}/execute
# Execute an agent

GET /api/agents/{agent_name}/status
# Get execution status
```

### MCP Tools

```bash
GET /api/tools/list
# List all MCP tools

POST /api/tools/{tool_name}/invoke
# Invoke a tool

GET /api/tools/{tool_name}/info
# Get tool info
```

### Models

```bash
GET /api/models/providers
# List available model providers

POST /api/models/invoke
# Invoke a model with a prompt
# Body: { "prompt": "...", "model": "llama2" }

GET /api/models/status
# Get model provider status
```

### Ollama

```bash
GET /api/ollama/health
# Get Ollama service health

GET /api/ollama/models
# List all Ollama models

GET /api/ollama/models/{model_name}/check
# Check if model available

GET /api/ollama/info
# Get Ollama configuration
```

---

## TypeScript SDK Usage

### Installation

```bash
cd src/sdk
npm install
npm run build
```

### Basic Usage

```typescript
import {
  AgentClient,
  ToolsClient,
  ModelsClient,
  OllamaClient,
} from '@agent-platform/sdk'

// Create clients
const agents = new AgentClient({ baseUrl: 'http://localhost:8000' })
const tools = new ToolsClient()
const models = new ModelsClient()
const ollama = new OllamaClient()

// List agents
const agentList = await agents.list()
console.log(agentList)

// List tools
const toolList = await tools.list()

// Invoke a tool
const result = await tools.invoke('ollama_list_models')
console.log(result)

// Invoke model
const response = await models.invoke('What is AI?', 'llama2')
console.log(response)

// Check Ollama health
const health = await ollama.getHealth()
console.log(health)
```

### Agents SDK

```typescript
import { AgentClient } from '@agent-platform/sdk'

const agents = new AgentClient()

// List all agents
const list = await agents.list()

// Get agent info
const agent = await agents.get('solver-agent')

// Execute an agent
await agents.execute('solver-agent', {
  problem: 'Implement feature X',
  context: 'Use TypeScript',
})

// Get execution status
const status = await agents.getStatus('solver-agent')
```

### Tools SDK

```typescript
import { ToolsClient } from '@agent-platform/sdk'

const tools = new ToolsClient()

// List all tools
const list = await tools.list()
// Returns: ['ollama_list_models', 'ollama_check_model', 'ollama_health', ...]

// Invoke a tool
const result = await tools.invoke('ollama_list_models')

// Invoke with parameters
const modelStatus = await tools.invoke('ollama_check_model', {
  model_name: 'llama2',
})
```

### Models SDK

```typescript
import { ModelsClient } from '@agent-platform/sdk'

const models = new ModelsClient()

// Get available providers
const providers = await models.getProviders()

// Invoke model for inference
const response = await models.invoke(
  'Summarize this: Lorem ipsum...',
  'llama2'
)

// Get status
const status = await models.getStatus()
// Returns: { ollama_available: true, cloud_provider_configured: false }
```

### Ollama SDK

```typescript
import { OllamaClient } from '@agent-platform/sdk'

const ollama = new OllamaClient()

// Get health
const health = await ollama.getHealth()

// List models
const models = await ollama.listModels()

// Check specific model
const check = await ollama.checkModel('llama2')

// Get Ollama info
const info = await ollama.getInfo()
```

---

## Web UI Features

### Dashboard
- Platform health status
- Ollama service status
- Model provider status
- Quick links to API docs

### Agents
- Browse all available agents
- View agent descriptions
- Deploy agents (UI ready, backend implementation pending)

### Tools
- Search and filter MCP tools
- Invoke tools directly from UI
- View tool results in real-time

### Ollama Settings
- Service health check
- List downloaded models
- Model size and info
- Configuration reference

---

## Running the API Server

### Standalone

```bash
pip install enterprise-agent-platform[api,ollama]
python -m agent_platform.api.server
```

The server will:
- Start FastAPI on port 8000
- Load all MCP tools automatically
- Connect to Ollama at `http://localhost:11434`
- Serve OpenAPI docs at `/docs` and ReDoc at `/redoc`

### With Custom Port

```bash
python -m agent_platform.api.server --port 9000
```

### With Environment Variables

```bash
OLLAMA_BASE_URL=http://my-ollama:11434 \
LOG_LEVEL=DEBUG \
python -m agent_platform.api.server
```

---

## Building the Web UI

### Development

```bash
cd src/web-ui
npm install
npm run dev
# Opens http://localhost:5173
```

The dev server includes a proxy to the API:
```
http://localhost:5173/api/* → http://localhost:8000/api/*
```

### Production Build

```bash
npm run build
npm run preview
```

---

## SDK Development

### Build SDK

```bash
cd src/sdk
npm install
npm run build
```

This generates:
- `dist/index.js` — CommonJS bundle
- `dist/index.d.ts` — TypeScript declarations

### Using SDK in Your Project

```bash
# If publishing to npm
npm install @agent-platform/sdk

# Or locally
npm install ../sdk
```

```typescript
import {
  AgentClient,
  ToolsClient,
  ModelsClient,
  OllamaClient,
} from '@agent-platform/sdk'
```

---

## Environment Variables

### API Server

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama service endpoint |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `CORS_ORIGINS` | `localhost:3000,localhost:5173` | CORS allowed origins |

### Web UI (Vite)

| Variable | Default | Description |
| `VITE_API_URL` | `http://localhost:8000` | Backend API URL |

---

## Troubleshooting

### "Cannot connect to API"

```bash
# Check if API server is running
curl http://localhost:8000/health

# If not, start it
python -m agent_platform.api.server
```

### "Ollama not available"

```bash
# Check Ollama service
curl http://localhost:11434/api/tags

# If not running, start it
docker run -d -p 11434:11434 ollama/ollama
ollama pull llama2
```

### "Web UI cannot reach API"

If running web-ui on different machine:
```bash
# Update API URL in env
VITE_API_URL=http://api-server:8000 npm run build
```

### CORS errors in browser

API CORS is configured for:
- `http://localhost:3000` (docker-compose)
- `http://localhost:5173` (dev server)

To add more origins, update `src/agent_platform/api/server.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["your-origin:port"],  # ← Add here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Next Steps

1. **Extend the API** — Add WebSocket support for real-time agent logs
2. **Extend the UI** — Add agent deployment workflow, custom dashboards
3. **Add authentication** — JWT tokens, role-based access control
4. **Add testing** — API integration tests, SDK unit tests
5. **Package for distribution** — npm publish SDK, Docker registry for images

---

## Architecture Summary

| Component | Technology | Port | Purpose |
|-----------|-----------|------|---------|
| **API** | FastAPI | 8000 | REST API for all platform operations |
| **Web UI** | React + Vite | 3000 | Developer dashboard |
| **SDK** | TypeScript | — | Client library for programmatic access |
| **Ollama** | Container | 11434 | Local LLM inference |

**Key principle:** Everything goes through the API layer. This enables:
- ✅ Multi-client support (web, mobile, CLI, etc.)
- ✅ Separation of concerns
- ✅ Easy testing and mocking
- ✅ Scalability (API can be deployed independently)
