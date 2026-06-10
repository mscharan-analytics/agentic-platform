# Testing Guide: Authentication & WebSocket Integration

This guide provides step-by-step instructions to test the complete authentication and real-time agent execution flow.

## Prerequisites

- Docker and Docker Compose installed
- Terminal/CLI access
- Modern web browser (Chrome, Firefox, Safari, Edge)
- `curl` or Postman (optional, for API testing)

## Quick Start (Automated)

```bash
# From project root
cd deployment/docker
docker-compose up -d
```

Wait 30-60 seconds for services to start, then proceed to [Manual Testing](#manual-testing).

## Manual Testing

### 1. Verify Backend Services

Check that all services are running:

```bash
# Check API server
curl http://localhost:8000/health
# Expected: {"status":"ok","service":"agent-platform"}

# Check Ollama health
curl http://localhost:8000/api/ollama/health
# Expected: Status OK if Ollama is running

# Check agents list
curl http://localhost:8000/api/agents/list
# Expected: JSON with agents array
```

### 2. Test Authentication Endpoint

**Test login with valid credentials:**

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

**Expected Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Test login with invalid credentials:**

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrong"}'
```

**Expected Response:**
```json
{"detail":"Invalid credentials"}
```

**Available Demo Credentials:**
- Username: `admin`, Password: `admin` (Role: admin)
- Username: `user`, Password: `password` (Role: user)

### 3. Test Agent Deployment & WebSocket Flow

This is the complete end-to-end flow:

#### Step 1: Get Session via Deployment Endpoint

```bash
curl -X POST http://localhost:8000/api/agents/solver-agent/deploy \
  -H "Content-Type: application/json" \
  -d '{}' \
  -s | jq .
```

**Expected Response:**
```json
{
  "agent": "solver-agent",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "deployed",
  "message": "Agent solver-agent deployment started"
}
```

Save the `session_id` for the next steps.

#### Step 2: Connect to WebSocket and Receive Events

```bash
# Using wscat (install with: npm install -g wscat)
wscat -c ws://localhost:8000/api/events/ws/logs/550e8400-e29b-41d4-a716-446655440000
```

**Expected Output:** Events will stream in real-time:
```json
{"type":"deployment_started","timestamp":1234567890,"data":{"agent":"solver-agent","session_id":"550e8400-e29b-41d4-a716-446655440000"}}
{"type":"execution_progress","timestamp":1234567891,"data":{"message":"Initializing solver-agent...","progress":10}}
{"type":"execution_progress","timestamp":1234567892,"data":{"message":"Running solver-agent...","progress":50}}
{"type":"execution_progress","timestamp":1234567893,"data":{"message":"solver-agent complete","progress":100}}
{"type":"execution_completed","timestamp":1234567894,"data":{"agent":"solver-agent","result":"Execution successful"}}
```

#### Step 3: Get Execution Status (Polling Fallback)

```bash
curl http://localhost:8000/api/agents/solver-agent/execution/550e8400-e29b-41d4-a716-446655440000 \
  -s | jq .
```

**Expected Response:**
```json
{
  "agent": "solver-agent",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "events": [...], // Same events from WebSocket
  "event_count": 5
}
```

#### Step 4: Cancel Execution

```bash
# Note: Only works if execution is still running (status == "running")
curl -X POST \
  http://localhost:8000/api/agents/solver-agent/execution/550e8400-e29b-41d4-a716-446655440000/cancel \
  -s | jq .
```

**Expected Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "cancelled"
}
```

### 4. Test Web UI (Integrated Flow)

1. **Open the application:**
   - URL: `http://localhost:3000`
   - Should see login screen

2. **Login:**
   - Username: `admin`
   - Password: `admin`
   - Click "Sign In"
   - Should redirect to Dashboard

3. **Navigate to Agents:**
   - Click "🤖 Agents" in sidebar
   - Should see list of available agents (e.g., "solver-agent", "worker-agent")

4. **Deploy an Agent:**
   - Click "🚀 Deploy" button on any agent
   - Button should show "⏳ Deploying..." while request is pending
   - ExecutionMonitor should appear in bottom-right corner
   - Monitor should show "Connecting..." then "Connected"

5. **Watch Execution:**
   - Real-time events should appear in ExecutionMonitor
   - Progress bar should fill from 0% to 100%
   - Status should change from "⏳ running" to "✓ completed"
   - Events should show:
     - `deployment_started`
     - `execution_progress` (multiple)
     - `execution_completed`

6. **Test Execution Monitor Controls:**
   - Click "Clear Logs" to clear event list
   - Click "Cancel Execution" button (if still running) to cancel
   - Click "Close" button to close monitor
   - Click "X" button to close monitor

7. **Test Logout:**
   - Click "Logout" button in header
   - Should redirect back to login screen
   - Token should be cleared from localStorage

### 5. Test Role-Based Access

**Note:** Current implementation supports role-based tokens but route protection is optional.

#### Admin User:
- Can deploy agents
- Can cancel executions
- Full access to all features

#### Regular User:
- Can view agents (read-only deployment info)
- Token is created but with "user" role
- Future: Can be restricted to read-only operations

## Debugging

### API Issues

**"Invalid credentials" error:**
- Verify demo credentials are correct (see available credentials above)
- Check server logs: `docker logs <api-container-id>`

**"Connection refused" error:**
- Verify Docker services are running: `docker-compose ps`
- Check if port 8000 is available: `lsof -i :8000`
- Restart services: `docker-compose restart`

### WebSocket Issues

**ExecutionMonitor shows "Disconnected":**
1. Check browser console for errors (F12 Developer Tools)
2. Verify WebSocket URL: `ws://localhost:8000/api/events/ws/logs/{sessionId}`
3. Check server logs for connection errors
4. Try the `wscat` command (see [Step 2](#step-2-connect-to-websocket-and-receive-events)) to verify WebSocket endpoint

**Events not appearing:**
1. Verify deployment was successful (check session_id)
2. Check API logs for event emission errors
3. Verify WebSocket connection is open (green indicator in UI)

### React App Issues

**Blank screen or "Loading agents...":**
- Check browser console for errors (F12 Developer Tools)
- Verify API is running: `curl http://localhost:8000/health`
- Clear localStorage and reload: `localStorage.clear()` in console

**Login fails:**
- Check browser console network tab for API response
- Verify credentials are correct
- Check server logs: `docker logs <api-container-id>`

## Performance Testing

### Load Test: Multiple Concurrent Deployments

```bash
#!/bin/bash
# Test multiple deployments simultaneously
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/agents/solver-agent/deploy \
    -H "Content-Type: application/json" \
    -d '{}' &
done
wait
```

Expected: All deployments should succeed with unique session IDs.

### WebSocket Stability Test

```bash
#!/bin/bash
# Maintain multiple concurrent WebSocket connections
# Run this in separate terminals or background jobs
for i in {1..3}; do
  wscat -c ws://localhost:8000/api/events/ws/logs/test-session-$i &
done
wait
```

Expected: All connections should remain open and stable.

## Cleanup

```bash
# Stop all services
docker-compose down

# Remove volumes (if needed)
docker-compose down -v

# Stop a specific service
docker-compose stop api
docker-compose stop web-ui
docker-compose stop ollama
```

## Checklist

Use this checklist to verify all components work:

### Backend
- [ ] API server starts without errors
- [ ] `/health` endpoint returns status
- [ ] `/api/auth/login` accepts valid credentials
- [ ] `/api/auth/login` rejects invalid credentials
- [ ] `/api/agents/list` returns agent list
- [ ] `/api/agents/{name}/deploy` returns session_id
- [ ] WebSocket `ws://localhost:8000/api/events/ws/logs/{sessionId}` connects
- [ ] WebSocket receives event stream during execution
- [ ] Events include all types: `deployment_started`, `execution_progress`, `execution_completed`

### Frontend
- [ ] React app loads at `localhost:3000`
- [ ] Login form is visible
- [ ] Login with valid credentials succeeds
- [ ] Dashboard displays after login
- [ ] Agents page loads and lists agents
- [ ] Deploy button creates ExecutionMonitor
- [ ] ExecutionMonitor shows "Connecting..." then "Connected"
- [ ] Real-time events appear in ExecutionMonitor
- [ ] Progress bar updates during execution
- [ ] Status changes from "running" to "completed"
- [ ] Logout button clears token and redirects to login

### Integration
- [ ] Full flow: Login → Navigate to Agents → Deploy → Watch Monitor → Logout
- [ ] Token persists across page reloads
- [ ] Multiple concurrent executions work correctly
- [ ] WebSocket reconnects after network interruption

## Next Steps

- [ ] Add authentication middleware to protected routes
- [ ] Implement role-based access control (RBAC) enforcement
- [ ] Add user session management and token refresh
- [ ] Implement execution history and metrics
- [ ] Add error handling and retry logic
- [ ] Performance optimization and load testing
