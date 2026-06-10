#!/usr/bin/env bash
set -e

echo "==================================================="
echo "🚀 Enterprise Agent Platform - Developer Demo"
echo "==================================================="
echo ""

# Scenario: Developer on a laptop wants to use the platform
echo "📋 Scenario: Developer on a fresh laptop"
echo ""

# Step 1: Install
echo "Step 1️⃣  Install from PyPI (or local wheel)"
echo "   $ pip install enterprise-agent-platform"
echo ""
echo "   [This would install 27 KB wheel with all dependencies]"
echo ""

# Step 2: Check version
echo "Step 2️⃣  Verify installation"
echo "   $ agent-platform --help"
echo "   $ agent-platform --version"
echo ""

# Step 3: Run a simple goal
echo "Step 3️⃣  Execute your first autonomous workflow"
echo ""
echo "   $ agent-platform --goal 'Implement a secure feature deployment'"
echo ""
echo "   [Output]:"
echo "   trace_id: a1b2c3d4-e5f6..."
echo "   solver: ✓ Decomposed objective into constraints"
echo "   planner: ✓ Created 8-step execution DAG"
echo "   steps completed: 3"
echo "   evaluation: ✓ All quality gates passed"
echo "   audit_events: 12"
echo ""

# Step 4: Python integration
echo "Step 4️⃣  Or use Python SDK directly"
echo '   from agent_platform.agents.catalog import default_agent_registry'
echo '   from agent_platform.orchestration import AutonomousRunner'
echo '   from agent_platform.policy.engine import PolicyEngine'
echo ""
echo '   registry = default_agent_registry()'
echo '   runner = AutonomousRunner(registry=registry, policy=PolicyEngine())'
echo '   result = await runner.run("Your goal")'
echo ""

# Step 5: Check what container would look like
echo "Step 5️⃣  Or use Docker (no Python setup needed)"
echo "   $ docker pull enterprise-agent-platform:latest"
echo "   $ docker run enterprise-agent-platform --goal 'Your goal'"
echo ""

echo "==================================================="
echo "✅ That's it! Three distribution options:"
echo ""
echo "   1. 🐍 pip install enterprise-agent-platform"
echo "   2. 📦 Python wheel from dist/ folder"
echo "   3. 🐳 docker run enterprise-agent-platform"
echo ""
echo "==================================================="
