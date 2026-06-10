#!/bin/bash

# Persistent Brain Session Resume Script
# Usage: ./vault/scripts/resume.sh [--verbose]
#
# This script prepares an agent to resume work on the Enterprise Agent Platform.
# It reads the execution plan and handoff notes, then outputs context for the agent.
# 
# Exit Codes:
#   0: Success - context printed to stdout
#   1: Error - missing critical files or parsing failure

set -euo pipefail

VERBOSE=${1:-}
VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXECUTION_PLAN="${VAULT_ROOT}/EXECUTION_PLAN.md"
HANDOFF_LOG="${VAULT_ROOT}/HANDOFF_NOTES.md"
TEMP_CONTEXT=$(mktemp)

cleanup() {
    rm -f "$TEMP_CONTEXT"
}
trap cleanup EXIT

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Utility functions
log_error() {
    echo -e "${RED}❌ ERROR: $1${NC}" >&2
}

log_info() {
    echo -e "${GREEN}ℹ️  $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
}

log_section() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Validate prerequisites
check_prerequisites() {
    if [[ ! -f "$EXECUTION_PLAN" ]]; then
        log_error "Execution plan not found at $EXECUTION_PLAN"
        return 1
    fi
    
    if [[ ! -d "$VAULT_ROOT" ]]; then
        log_error "Vault directory not found at $VAULT_ROOT"
        return 1
    fi
    
    return 0
}

# Extract unblocked tasks from execution plan
get_unblocked_tasks() {
    log_section "Unblocked Tasks (Ready to Start)"
    
    # Parse EXECUTION_PLAN.md for 🔲 (unblocked) status
    grep -E '^\| TASK\.[0-9]+.*🔲.*\|' "$EXECUTION_PLAN" | head -10 || true
    
    echo ""
    echo "Full task list: $EXECUTION_PLAN"
}

# Extract most recent handoff note
get_latest_handoff() {
    log_section "Latest Handoff Note"
    
    if [[ -f "$HANDOFF_LOG" ]]; then
        # Show last handoff (most recent session)
        tail -100 "$HANDOFF_LOG"
    else
        log_warn "No handoff notes found. This is the first session."
        echo ""
        echo "When you finish, run: ./vault/scripts/wrap-up.sh"
    fi
}

# Read department status
get_department_status() {
    log_section "Department Status Summary"
    
    for dept in "$VAULT_ROOT"/{01_RnD,02_Product,03_Marketing,04_Community,05_Legal,06_Operations,07_Security,08_Docs}; do
        if [[ -f "$dept/INDEX.md" ]]; then
            dept_name=$(basename "$dept")
            echo "📁 $dept_name"
            
            # Extract current state from each INDEX
            grep "^## Current State" -A 10 "$dept/INDEX.md" | head -5 | tail -4 | sed 's/^/   /'
            echo ""
        fi
    done
}

# Display session context
display_context() {
    log_section "Session Context - Enterprise Agent Platform"
    
    echo "🗓️  Session Started: $(date)"
    echo "📍 Vault Location: $VAULT_ROOT"
    echo "📊 Execution Plan: $EXECUTION_PLAN"
    echo ""
    
    # Project state
    echo -e "${BLUE}PROJECT STATE:${NC}"
    echo "  Current Phase: Phase 1 (Ready-for-Pilot, Q2 2026)"
    echo "  Foundation: ✅ Complete"
    echo "  Production Ready: 🔄 In Progress"
    echo ""
}

# Display recommendations
get_recommendations() {
    log_section "Recommended Next Steps"
    
    echo "1. Review the EXECUTION_PLAN.md to see all tasks"
    echo "2. Check department indexes for context (start with 02_Product/INDEX.md)"
    echo "3. Pick the highest-leverage unblocked task (see list above)"
    echo "4. Read relevant department docs in vault/"
    echo "5. Execute work"
    echo "6. When finished, run: ./vault/scripts/wrap-up.sh"
    echo ""
    echo "Key blocking issues:"
    echo "  • TASK.1003 (Live LLM integration) needs ModelGateway endpoint"
    echo "  • TASK.1006 (LLM data policy) is critical path for security"
    echo ""
}

# Main execution
main() {
    log_info "Resuming work on Enterprise Agent Platform..."
    echo ""
    
    if ! check_prerequisites; then
        return 1
    fi
    
    display_context
    get_unblocked_tasks
    get_department_status
    get_latest_handoff
    get_recommendations
    
    log_info "Context loaded. You're ready to start work!"
    echo ""
}

main
exit_code=$?
exit $exit_code
