#!/bin/bash

# Start Enterprise Agent Platform with SDK/UI
# Usage: ./start-dev.sh [api|ui|ollama|all]

set -e

MODE=${1:-all}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

echo "🚀 Starting Enterprise Agent Platform..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

start_api() {
  echo -e "${GREEN}Starting API server...${NC}"
  cd "$PROJECT_ROOT"
  pip install -e ".[api,ollama]" >/dev/null 2>&1 || true
  python -m agent_platform.api.server &
  API_PID=$!
  echo -e "${GREEN}✓ API server started (PID: $API_PID)${NC}"
  echo "  📚 Swagger: http://localhost:8000/docs"
  echo "  📖 ReDoc: http://localhost:8000/redoc"
}

start_ui() {
  echo -e "${GREEN}Starting Web UI...${NC}"
  cd "$PROJECT_ROOT/src/web-ui"
  npm install >/dev/null 2>&1 || true
  npm run dev &
  UI_PID=$!
  echo -e "${GREEN}✓ Web UI started (PID: $UI_PID)${NC}"
  echo "  🌐 Dashboard: http://localhost:3000"
}

start_ollama() {
  echo -e "${GREEN}Checking Ollama...${NC}"
  if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Ollama not running. Starting Docker container...${NC}"
    docker run -d -p 11434:11434 ollama/ollama --name ollama >/dev/null 2>&1 || true
    sleep 2
    echo -e "${GREEN}✓ Ollama started${NC}"
    echo "  🧠 Ollama API: http://localhost:11434"
  else
    echo -e "${GREEN}✓ Ollama already running${NC}"
  fi
}

# Handle interrupts
trap 'kill $API_PID $UI_PID 2>/dev/null; echo -e "${YELLOW}Stopped${NC}"; exit 0' INT

case "$MODE" in
  api)
    start_api
    wait $API_PID
    ;;
  ui)
    start_ui
    wait $UI_PID
    ;;
  ollama)
    start_ollama
    ;;
  all)
    start_ollama
    start_api
    start_ui
    echo -e "${GREEN}✓ All services started!${NC}"
    echo ""
    echo "  Web UI: http://localhost:3000"
    echo "  API: http://localhost:8000"
    echo "  Ollama: http://localhost:11434"
    echo ""
    echo "Press Ctrl+C to stop all services"
    wait
    ;;
  *)
    echo "Usage: $0 [api|ui|ollama|all]"
    exit 1
    ;;
esac
