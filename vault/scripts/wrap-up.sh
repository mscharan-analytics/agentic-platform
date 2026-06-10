#!/bin/bash

# Persistent Brain Session Wrap-Up Script
# Usage: ./vault/scripts/wrap-up.sh [--summary]
#
# This script finalizes a session by:
#   1. Prompting for work summary
#   2. Updating execution plan status
#   3. Creating handoff note for next session
#   4. Committing changes to git
#
# Exit Codes:
#   0: Success - session wrapped and committed
#   1: Error - validation failed

set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_ROOT="$(cd "$VAULT_ROOT/.." && pwd)"
EXECUTION_PLAN="${VAULT_ROOT}/EXECUTION_PLAN.md"
HANDOFF_LOG="${VAULT_ROOT}/HANDOFF_NOTES.md"
WRAP_UP_TEMP=$(mktemp)

cleanup() {
    rm -f "$WRAP_UP_TEMP"
}
trap cleanup EXIT

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Utility functions
log_error() {
    echo -e "${RED}❌ ERROR: $1${NC}" >&2
}

log_info() {
    echo -e "${GREEN}ℹ️  $1${NC}"
}

log_section() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Check prerequisites
check_prerequisites() {
    if ! command -v git &> /dev/null; then
        log_error "git not found. Required for committing changes."
        return 1
    fi
    
    if ! git -C "$PROJECT_ROOT" rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Not a git repository: $PROJECT_ROOT"
        return 1
    fi
    
    return 0
}

# Interactive prompt collection
collect_work_summary() {
    log_section "Wrap-Up Summary"
    
    echo "What work did you complete this session?"
    echo "(Provide a brief description, then press Ctrl+D when done)"
    echo ""
    
    work_completed=$(cat)
    
    echo ""
    echo "What changed in the project? (files, decisions, status updates)"
    echo "(Press Ctrl+D when done)"
    echo ""
    
    what_changed=$(cat)
    
    echo ""
    echo "What tasks are now unblocked for the next session?"
    echo "(Press Ctrl+D when done)"
    echo ""
    
    next_unblocked=$(cat)
    
    echo ""
    echo "Any known risks or open questions?"
    echo "(Press Ctrl+D when done, or just press Ctrl+D to skip)"
    echo ""
    
    risks=$(cat)
}

# Create handoff note
create_handoff_note() {
    log_section "Creating Handoff Note"
    
    local timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    
    cat >> "$HANDOFF_LOG" << EOF

---

## Session Handoff - $timestamp

### Work Completed
$work_completed

### What Changed
$what_changed

### Next Unblocked Tasks
$next_unblocked

### Risks & Open Questions
${risks:-None identified at wrap-up}

### Session Metadata
- Wrapped by: \$(whoami)
- Hostname: \$(hostname)
- Repository: $PROJECT_ROOT

---

EOF
    
    log_info "Handoff note created"
}

# Validate execution plan before commit
validate_execution_plan() {
    log_section "Validating Execution Plan"
    
    if ! grep -q "Last Updated:" "$EXECUTION_PLAN"; then
        log_error "Execution plan missing 'Last Updated' timestamp"
        return 1
    fi
    
    log_info "Execution plan is valid"
    return 0
}

# Commit changes to git
commit_session_changes() {
    log_section "Committing Session Changes"
    
    cd "$PROJECT_ROOT"
    
    # Stage vault changes
    git add vault/ 2>/dev/null || true
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        log_info "No changes to commit"
        return 0
    fi
    
    # Create descriptive commit message
    local commit_msg="session: $timestamp - persistent brain updates

- Updated execution plan status
- Created handoff note for next session
- Vault state captured

See vault/HANDOFF_NOTES.md for session summary"
    
    git commit -m "$commit_msg" || {
        log_error "Failed to commit changes"
        return 1
    }
    
    log_info "Changes committed to git"
    return 0
}

# Display wrap-up summary
display_summary() {
    log_section "Session Wrap-Up Complete"
    
    echo "✅ Handoff note created"
    echo "✅ Execution plan updated"
    echo "✅ Changes committed to git"
    echo ""
    echo "Next session: Run ./vault/scripts/resume.sh"
    echo ""
}

# Main execution
main() {
    log_info "Wrapping up Enterprise Agent Platform session..."
    echo ""
    
    if ! check_prerequisites; then
        return 1
    fi
    
    collect_work_summary
    create_handoff_note
    
    if ! validate_execution_plan; then
        log_error "Execution plan validation failed. Aborting."
        return 1
    fi
    
    if ! commit_session_changes; then
        log_error "Git commit failed. Changes are still staged."
        echo "Review with: git diff --cached"
        echo "Commit manually: git commit -m 'session: <timestamp> - vault updates'"
        return 1
    fi
    
    display_summary
    return 0
}

main
exit_code=$?
exit $exit_code
