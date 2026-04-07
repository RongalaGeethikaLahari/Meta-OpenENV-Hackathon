#!/usr/bin/env bash
#
# validate-submission.sh — OpenEnv Submission Validator
#

set -uo pipefail

DOCKER_BUILD_TIMEOUT=600

if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' BOLD='' NC=''
fi

run_with_timeout() {
  local secs="$1"; shift
  if command -v timeout &>/dev/null; then
    timeout "$secs" "$@"
  elif command -v gtimeout &>/dev/null; then
    gtimeout "$secs" "$@"
  else
    "$@" &
    local pid=$!
    ( sleep "$secs" && kill "$pid" 2>/dev/null ) &
    local watcher=$!
    wait "$pid" 2>/dev/null
    local rc=$?
    kill "$watcher" 2>/dev/null
    wait "$watcher" 2>/dev/null
    return $rc
  fi
}

portable_mktemp() {
  local prefix="${1:-validate}"
  mktemp "${TMPDIR:-/tmp}/${prefix}-XXXXXX" 2>/dev/null || mktemp
}

CLEANUP_FILES=()
cleanup() { rm -f "${CLEANUP_FILES[@]+"${CLEANUP_FILES[@]}"}"; }
trap cleanup EXIT

PING_URL="${1:-}"
REPO_DIR="${2:-.}"

if [ -z "$PING_URL" ]; then
  echo "Usage: $0 <ping_url> [repo_dir]"
  exit 1
fi

REPO_DIR="$(cd "$REPO_DIR" && pwd)"
PING_URL="${PING_URL%/}"

PASS=0

log()  { echo "[$(date -u +%H:%M:%S)] $*"; }
pass() { log "PASSED -- $1"; PASS=$((PASS + 1)); }
fail() { log "FAILED -- $1"; }

echo "========================================"
echo "  OpenEnv Submission Validator"
echo "========================================"
log "Repo:     $REPO_DIR"
log "Ping URL: $PING_URL"

# ---------------- STEP 1 ----------------

log "Step 1/3: Checking HF Space..."

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" -d '{}' \
  "$PING_URL/reset")

if [ "$HTTP_CODE" = "200" ]; then
  pass "HF Space responds correctly"
else
  fail "HF Space failed (HTTP $HTTP_CODE)"
  exit 1
fi

# ---------------- STEP 2 ----------------

log "Step 2/3: Building Docker..."

if [ ! -f "$REPO_DIR/Dockerfile" ]; then
  fail "No Dockerfile found"
  exit 1
fi

if run_with_timeout "$DOCKER_BUILD_TIMEOUT" docker build "$REPO_DIR" > /dev/null 2>&1; then
  pass "Docker build succeeded"
else
  fail "Docker build failed"
  exit 1
fi

# ---------------- STEP 3 ----------------

log "Step 3/3: Running openenv validate..."

if ! command -v openenv &>/dev/null; then
  echo "Install openenv-core: pip install openenv-core"
  exit 1
fi

if cd "$REPO_DIR" && openenv validate; then
  pass "OpenEnv validation passed"
else
  fail "OpenEnv validation failed"
  exit 1
fi

# ---------------- DONE ----------------

echo "========================================"
echo "  ALL CHECKS PASSED!"
echo "========================================"