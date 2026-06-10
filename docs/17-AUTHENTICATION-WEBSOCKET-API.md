# API Reference: Authentication & WebSocket Events

This document provides detailed API documentation for authentication and real-time event streaming.

## Table of Contents

1. [Authentication](#authentication)
2. [WebSocket Event Streaming](#websocket-event-streaming)
3. [Error Handling](#error-handling)
4. [Examples](#examples)

## Authentication

### Login Endpoint

**Endpoint:** `POST /api/auth/login`

**Description:** Authenticate a user and receive a JWT access token.

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6IjIwMjQtMDEtMTVUMTI6MDA6MDAifQ...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Invalid credentials"
}
```

**Available Demo Credentials:**

| Username | Password | Role |
|----------|----------|------|
| admin | admin | admin |
| user | password | user |

**Token Format:**

The `access_token` is a JWT with the following payload structure:

```json
{
  "sub": "username",
  "role": "admin|user",
  "exp": 1234567890
}
```

**Usage:**

Include the token in the `Authorization` header for protected endpoints:

```
Authorization: Bearer <access_token>
```

Example with curl:

```bash
curl -X GET http://localhost:8000/api/agents/list \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**Token Expiration:**

- Default expiration: 60 minutes
- After expiration, user must login again to receive a new token
- Token is stored in browser's `localStorage` under key `auth_token`

### Token Validation

Tokens are automatically validated using the following process:

1. Extract token from `Authorization` header (format: `Bearer <token>`)
2. Decode JWT using `HS256` algorithm
3. Verify signature using `JWT_SECRET_KEY` environment variable
4. Check token expiration time (`exp` claim)
5. Return username (`sub`) and role (`role`) for use in route handlers

**Errors:**

- **Invalid Signature:** Token was tampered with
- **Expired:** Token's `exp` time is in the past
- **Malformed:** Token is not valid JWT format
- **Missing:** No token provided in Authorization header

## WebSocket Event Streaming

### Event Stream Endpoint

**Endpoint:** `ws://localhost:8000/api/events/ws/logs/{session_id}`

**Description:** Real-time event streaming for agent executions via WebSocket.

**Connection:**

```javascript
const ws = new WebSocket(`ws://localhost:8000/api/events/ws/logs/${sessionId}`);

ws.onopen = () => console.log('Connected');
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Event:', message);
};
ws.onerror = (error) => console.error('Error:', error);
ws.onclose = () => console.log('Disconnected');
```

### Event Message Format

All events follow this format:

```json
{
  "type": "event_type",
  "timestamp": 1234567890.123,
  "data": {
    "key": "value"
  }
}
```

### Event Types

#### 1. deployment_started

Emitted when agent deployment begins.

```json
{
  "type": "deployment_started",
  "timestamp": 1234567890,
  "data": {
    "agent": "solver-agent",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

#### 2. execution_progress

Emitted periodically during execution to show progress.

```json
{
  "type": "execution_progress",
  "timestamp": 1234567891,
  "data": {
    "message": "Processing input data...",
    "progress": 25
  }
}
```

**Data Fields:**
- `message` (string): Human-readable status message
- `progress` (integer 0-100): Execution progress percentage

#### 3. execution_completed

Emitted when execution completes successfully.

```json
{
  "type": "execution_completed",
  "timestamp": 1234567895,
  "data": {
    "agent": "solver-agent",
    "result": "Execution successful"
  }
}
```

#### 4. execution_failed

Emitted when execution encounters an error.

```json
{
  "type": "execution_failed",
  "timestamp": 1234567895,
  "data": {
    "error": "Configuration not found"
  }
}
```

#### 5. execution_cancelled

Emitted when execution is explicitly cancelled.

```json
{
  "type": "execution_cancelled",
  "timestamp": 1234567895,
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### Event Session Management

**Session Creation:**

Sessions are created automatically when an agent is deployed:

```bash
POST /api/agents/{agent_name}/deploy
```

Response includes `session_id`:

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Session Retrieval:**

Get all events for a session (polling fallback):

```bash
GET /api/events/events/{session_id}
```

Response:

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "events": [...],
  "count": 5
}
```

## Error Handling

### HTTP Status Codes

| Status | Meaning | Example |
|--------|---------|---------|
| 200 | Success | Login accepted, events retrieved |
| 400 | Bad Request | Invalid JSON body |
| 401 | Unauthorized | Invalid credentials or expired token |
| 404 | Not Found | Session not found, agent not found |
| 500 | Server Error | Unexpected server error |

### Error Response Format

```json
{
  "detail": "Error description"
}
```

### WebSocket Error Handling

**Connection Errors:**

```javascript
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
  // Implement reconnection logic
};
```

**Common Issues:**

1. **Invalid session_id:** WebSocket connects but no events received
   - Verify session_id from deployment response
   - Check if execution is still running

2. **Connection refused:** WebSocket endpoint not reachable
   - Verify API server is running
   - Check firewall/network settings

3. **Session expired:** Old events not appearing
   - Sessions are stored in memory and cleared on server restart
   - Events are available while server is running

## Examples

### Complete Flow: Login → Deploy → Stream Events

#### 1. Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

Response:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### 2. Deploy Agent

```bash
curl -X POST http://localhost:8000/api/agents/solver-agent/deploy \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:

```json
{
  "agent": "solver-agent",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "deployed",
  "message": "Agent solver-agent deployment started"
}
```

#### 3. Connect to WebSocket

```bash
# Using Node.js ws library
const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:8000/api/events/ws/logs/550e8400-e29b-41d4-a716-446655440000');

ws.on('open', () => {
  console.log('Connected to event stream');
});

ws.on('message', (data) => {
  const event = JSON.parse(data);
  console.log(`[${event.type}] ${event.data.message || event.data.result}`);
});
```

Output:

```
Connected to event stream
[deployment_started] undefined
[execution_progress] Initializing solver-agent...
[execution_progress] Running solver-agent...
[execution_progress] solver-agent complete
[execution_completed] Execution successful
```

### React Hook: useExecutionStream

```typescript
import { useEffect, useState } from 'react';

interface ExecutionEvent {
  type: string;
  timestamp: number;
  data: Record<string, any>;
}

export function useExecutionStream(sessionId: string) {
  const [events, setEvents] = useState<ExecutionEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) return;

    const ws = new WebSocket(
      `ws://localhost:8000/api/events/ws/logs/${sessionId}`
    );

    ws.onopen = () => {
      setConnected(true);
      setError(null);
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data) as ExecutionEvent;
        setEvents(prev => [...prev, message]);
      } catch (err) {
        setError(`Failed to parse event: ${err}`);
      }
    };

    ws.onerror = () => {
      setError('WebSocket connection error');
      setConnected(false);
    };

    ws.onclose = () => {
      setConnected(false);
    };

    return () => ws.close();
  }, [sessionId]);

  return { events, connected, error };
}
```

### TypeScript SDK Example

```typescript
import { AgentClient, APIClient } from '@enterprise-agent-platform/sdk';

async function deployAndMonitor() {
  const client = new AgentClient('http://localhost:8000');
  
  // Deploy agent
  const deployment = await client.deploy('solver-agent', { goal: 'Solve problem X' });
  console.log('Session ID:', deployment.sessionId);
  
  // Stream events
  const ws = new WebSocket(
    `ws://localhost:8000/api/events/ws/logs/${deployment.sessionId}`
  );
  
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    console.log(`Progress: ${msg.data.progress}%`);
  };
}

deployAndMonitor();
```

## Environment Variables

**JWT Configuration:**

```bash
# Set custom JWT secret (recommended for production)
JWT_SECRET_KEY=your-secret-key-here

# Token expiration (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Security Considerations

1. **Secret Key:** Change `JWT_SECRET_KEY` in production
2. **HTTPS:** Always use `wss://` for WebSocket in production
3. **CORS:** Configure allowed origins in `CORSMiddleware`
4. **Token Storage:** Consider using secure cookies instead of localStorage
5. **Refresh Tokens:** Implement refresh token rotation for better security

## Related Documentation

- [Testing Guide](./16-TESTING-GUIDE.md) - Comprehensive testing instructions
- [SDK Integration](./15-SDK-API-INTEGRATION.md) - API and SDK usage
- [Architecture Overview](./01-ARCHITECTURE.md) - System design
