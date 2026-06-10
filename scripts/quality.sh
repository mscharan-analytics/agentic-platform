#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

source .venv/bin/activate

echo "📊 Running linting and type checks..."
ruff check src/ tests/ --quiet || echo "⚠️  Ruff issues found (non-blocking)"
mypy src/ --ignore-missing-imports --quiet || echo "⚠️  Type issues found (non-blocking)"

echo "✅ Quality checks complete"
