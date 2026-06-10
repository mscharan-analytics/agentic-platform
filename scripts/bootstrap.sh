#!/bin/bash
set -e

echo "🚀 Enterprise Agent Platform Bootstrap"
echo "======================================"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Step 1: Check Python version
echo "✓ Checking Python 3.11+"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python version: $PYTHON_VERSION"

# Step 2: Create virtual environment
if [ ! -d ".venv" ]; then
    echo "✓ Creating virtual environment..."
    python3 -m venv .venv
fi

# Step 3: Activate venv and install
echo "✓ Installing dependencies..."
source .venv/bin/activate
pip install -e .[dev]

# Step 4: Run tests
echo "✓ Running test suite..."
pytest -q

# Step 5: Display summary
echo ""
echo "✅ Bootstrap complete!"
echo ""
echo "Next steps:"
echo "1. Activate environment: source .venv/bin/activate"
echo "2. Run CLI: agent-platform --goal 'Your objective'"
echo "3. Or run Docker: docker-compose -f deployment/docker/docker-compose.yml up"
