#!/usr/bin/env bash
# Enhanced beads helper with automatic Larsson alignment measurement
# Integrates prediction, measurement, and review of Larsson fidelity metrics

set -e

# Ensure Go bin is in PATH (where bd is installed)
export PATH="$HOME/go/bin:$PATH"

# Verify bd is available (only for bd commands, not for our custom commands)
check_bd() {
    if ! command -v bd &> /dev/null; then
        echo "Error: 'bd' command not found" >&2
        echo "Install beads: GOTOOLCHAIN=auto go install github.com/steveyegge/beads/cmd/bd@latest" >&2
        echo "Ensure \$HOME/go/bin is in your PATH" >&2
        return 1
    fi
    return 0
}

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORTS_DIR="${PROJECT_ROOT}/reports"
PREDICTIONS_DIR="${REPORTS_DIR}/predictions"
BEADS_HELPERS="${PROJECT_ROOT}/.claude/beads-helpers.sh"

# Ensure directories exist
mkdir -p "$REPORTS_DIR" "$PREDICTIONS_DIR"

# Get current git hash (short)
get_git_hash() {
    git -C "$PROJECT_ROOT" rev-parse --short HEAD 2>/dev/null || echo "unknown"
}

# Get timestamp
get_timestamp() {
    date +"%Y-%m-%d_%H%M%S"
}

# Generate fidelity report with timestamp and git hash
generate_report() {
    local label=$1  # "baseline" or "final"
    local task_id=$2
    local timestamp=$(get_timestamp)
    local git_hash=$(get_git_hash)

    local filename="${task_id}_${label}_${timestamp}_${git_hash}"
    local txt_path="${REPORTS_DIR}/${filename}.txt"
    local json_path="${REPORTS_DIR}/${filename}.json"

    echo "Generating Larsson fidelity report: ${label}"

    # Generate both text and JSON reports
    python "${PROJECT_ROOT}/scripts/generate_fidelity_report.py" \
        --output "$txt_path" 2>/dev/null || {
        echo "Error: Failed to generate text report"
        return 1
    }

    python "${PROJECT_ROOT}/scripts/generate_fidelity_report.py" \
        --json --output "$json_path" 2>/dev/null || {
        echo "Error: Failed to generate JSON report"
        return 1
    }

    echo "  Text: ${txt_path}"
    echo "  JSON: ${json_path}"
    echo ""

    # Return paths for later use
    echo "$txt_path|$json_path"
}

# Extract overall score from JSON report
get_score() {
    local json_path=$1
    python -c "import json; data=json.load(open('$json_path')); print(f\"{data['overall_score']:.1f}\")"
}

# Record prediction
record_prediction() {
    local task_id=$1
    local prediction=$2
    local timestamp=$(get_timestamp)
    local git_hash=$(get_git_hash)
    local baseline_json=$3

    local pred_file="${PREDICTIONS_DIR}/${task_id}_prediction_${timestamp}_${git_hash}.txt"

    local baseline_score=$(get_score "$baseline_json")

    cat > "$pred_file" <<EOF
Task ID: ${task_id}
Timestamp: ${timestamp}
Git Hash: ${git_hash}
Baseline Score: ${baseline_score}

PREDICTION:
${prediction}

EOF

    echo "$pred_file"
}

# Generate review comparing baseline and final
generate_review() {
    local task_id=$1
    local baseline_json=$2
    local final_json=$3
    local prediction_file=$4
    local timestamp=$(get_timestamp)
    local git_hash=$(get_git_hash)

    local review_file="${REPORTS_DIR}/${task_id}_review_${timestamp}_${git_hash}.txt"

    local baseline_score=$(get_score "$baseline_json")
    local final_score=$(get_score "$final_json")
    local delta=$(python -c "print(f'{${final_score} - ${baseline_score}:.1f}')")

    cat > "$review_file" <<EOF
================================================================================
LARSSON ALIGNMENT REVIEW
================================================================================
Task ID: ${task_id}
Completed: ${timestamp}
Git Hash: ${git_hash}

SCORE SUMMARY:
  Baseline: ${baseline_score}/100
  Final:    ${final_score}/100
  Delta:    ${delta}

EOF

    if [ -f "$prediction_file" ]; then
        echo "PREDICTION:" >> "$review_file"
        tail -n +6 "$prediction_file" >> "$review_file"
        echo "" >> "$review_file"
    fi

    echo "DETAILED COMPARISON:" >> "$review_file"
    echo "See baseline: $(basename $baseline_json)" >> "$review_file"
    echo "See final: $(basename $final_json)" >> "$review_file"
    echo "" >> "$review_file"

    # Component-level comparison
    python - "$baseline_json" "$final_json" >> "$review_file" <<'PYTHON'
import sys
import json

baseline = json.load(open(sys.argv[1]))
final = json.load(open(sys.argv[2]))

print("Component Changes:")
print("-" * 80)

for component in baseline['components']:
    b_score = baseline['components'][component]['score']
    f_score = final['components'][component]['score']
    delta = f_score - b_score

    status = "↑" if delta > 0 else "↓" if delta < 0 else "→"
    name = baseline['components'][component]['name']

    print(f"  {status} {name:30s} {b_score:5.1f} → {f_score:5.1f} ({delta:+.1f})")

print()
PYTHON

    echo "================================================================================\n" >> "$review_file"

    echo "Review saved: $review_file"
    cat "$review_file"
}

# Enhanced start command with prediction
start() {
    local task_id=$1

    if [ -z "$task_id" ]; then
        echo "Usage: start <task-id>"
        return 1
    fi

    echo "========================================="
    echo "Starting Task: ${task_id}"
    echo "========================================="
    echo ""

    # Generate baseline report
    echo "Step 1: Generating baseline Larsson fidelity report..."
    local reports=$(generate_report "baseline" "$task_id")
    local baseline_txt=$(echo "$reports" | cut -d'|' -f1)
    local baseline_json=$(echo "$reports" | cut -d'|' -f2)

    local baseline_score=$(get_score "$baseline_json")
    echo "Current Larsson Fidelity Score: ${baseline_score}/100"
    echo ""

    # Prompt for prediction
    echo "Step 2: Prediction"
    echo "How will this task affect Larsson alignment?"
    echo "Consider which components will change and why:"
    echo "  - Architectural Compliance (25%)"
    echo "  - Information State Structure (25%)"
    echo "  - Semantic Operations Coverage (20%)"
    echo "  - Rules Coverage (20%)"
    echo "  - Domain Independence (10%)"
    echo ""
    echo "Enter prediction (end with Ctrl+D or empty line):"

    local prediction=""
    local line
    while IFS= read -r line; do
        [ -z "$line" ] && break
        prediction="${prediction}${line}\n"
    done

    # Record prediction
    local pred_file=$(record_prediction "$task_id" "$prediction" "$baseline_json")
    echo "Prediction recorded: $pred_file"
    echo ""

    # Store baseline and prediction paths for later
    local state_file="${PREDICTIONS_DIR}/${task_id}_state.txt"
    cat > "$state_file" <<EOF
baseline_json=$baseline_json
baseline_txt=$baseline_txt
prediction_file=$pred_file
EOF

    # Start the beads task
    echo "Step 3: Starting beads task..."
    bash "$BEADS_HELPERS" start "$task_id"
    echo ""
    echo "========================================="
    echo "Task started. Work on: ${task_id}"
    echo "When done, run: complete ${task_id}"
    echo "========================================="
}

# Enhanced complete command with review
complete() {
    local task_id=$1
    local reason=${2:-"Implemented"}

    if [ -z "$task_id" ]; then
        echo "Usage: complete <task-id> [reason]"
        return 1
    fi

    local state_file="${PREDICTIONS_DIR}/${task_id}_state.txt"
    if [ ! -f "$state_file" ]; then
        echo "Warning: No baseline found for ${task_id}"
        echo "Generating final report without comparison..."
        generate_report "final" "$task_id"
        bash "$BEADS_HELPERS" complete "$task_id" "$reason"
        return 0
    fi

    # Load state
    source "$state_file"

    echo "========================================="
    echo "Completing Task: ${task_id}"
    echo "========================================="
    echo ""

    # Generate final report
    echo "Step 1: Generating final Larsson fidelity report..."
    local reports=$(generate_report "final" "$task_id")
    local final_txt=$(echo "$reports" | cut -d'|' -f1)
    local final_json=$(echo "$reports" | cut -d'|' -f2)
    echo ""

    # Generate review
    echo "Step 2: Generating review (prediction vs actual)..."
    generate_review "$task_id" "$baseline_json" "$final_json" "$prediction_file"
    echo ""

    # Complete the beads task
    echo "Step 3: Completing beads task..."
    bash "$BEADS_HELPERS" complete "$task_id" "$reason"
    echo ""

    # Cleanup state file
    rm -f "$state_file"

    echo "========================================="
    echo "Task completed: ${task_id}"
    echo "Review your predictions vs actual results above"
    echo "========================================="
}

# Quick measurement without task context
measure() {
    local label=${1:-"measurement"}
    local timestamp=$(get_timestamp)
    local git_hash=$(get_git_hash)

    echo "Generating Larsson fidelity measurement..."
    python "${PROJECT_ROOT}/scripts/generate_fidelity_report.py" \
        --output "${REPORTS_DIR}/${label}_${timestamp}_${git_hash}.txt"

    python "${PROJECT_ROOT}/scripts/generate_fidelity_report.py" \
        --json --output "${REPORTS_DIR}/${label}_${timestamp}_${git_hash}.json"
}

# Delegate to original beads-helpers for other commands
delegate() {
    bash "$BEADS_HELPERS" "$@"
}

# Show help
help() {
    echo "Enhanced Beads + Larsson Alignment Tracking"
    echo ""
    echo "Larsson-Tracked Commands:"
    echo "  start <task-id>           - Start task with baseline measurement & prediction"
    echo "  complete <task-id> [msg]  - Complete task with final measurement & review"
    echo "  measure [label]           - Quick fidelity measurement"
    echo ""
    echo "Standard Beads Commands (delegated):"
    echo "  ready                     - Show ready tasks"
    echo "  current                   - Show in-progress tasks"
    echo "  phase <N>                 - Show phase N tasks"
    echo "  progress <N>              - Show phase N progress"
    echo "  urgent                    - Show high-priority tasks"
    echo "  summary                   - Project summary"
    echo "  discover <title>          - Create discovered task"
    echo ""
    echo "Examples:"
    echo "  start ibdm-123                    # Start with prediction prompt"
    echo "  complete ibdm-123 'Fixed rules'   # Complete with review"
    echo "  measure before-refactor           # Quick measurement"
}

# Main command dispatcher
if [ $# -eq 0 ]; then
    help
else
    cmd=$1
    shift

    case "$cmd" in
        start|complete|measure|help)
            $cmd "$@"
            ;;
        *)
            # Delegate to original beads-helpers
            delegate "$cmd" "$@"
            ;;
    esac
fi
