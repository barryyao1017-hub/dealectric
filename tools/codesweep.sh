#!/bin/bash
# Daily cart check of every published discount code (tools/codesweep.py), run by launchd:
#   ~/Library/LaunchAgents/com.jiayiyao.dealectric.codesweep.plist  (daily, 06:37 local)
# Starts the agent's Chrome if it is not running (agent-vault does nothing when it already is), then checks,
# merges, rebuilds, commits, pushes and redeploys the Worker when the link map changed. Log:
#   ~/Library/Logs/claude-automations/dealectric-codesweep.log
set -u
export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="${HOME:-/Users/jiayiyao}"
REPO="/Users/jiayiyao/Desktop/dealectric"
LOG_DIR="$HOME/Library/Logs/claude-automations"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/dealectric-codesweep.log"
{
  echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) codesweep start"
  if ! curl -s --max-time 5 http://localhost:9222/json/version >/dev/null; then
    echo "starting the agent's Chrome"
    uv --directory "$HOME/Desktop/agent-vault" run agent-vault browser || echo "agent-vault browser exited $?"
    for i in $(seq 1 30); do curl -s --max-time 5 http://localhost:9222/json/version >/dev/null && break; sleep 2; done
  fi
  cd "$REPO" || exit 1
  # Never run on a dirty tree the loop session is mid-edit on: the sweep commits only its own files, but a rebuild
  # would publish whatever is in src/. Uncommitted changes outside the sweep's own files mean skip today.
  if [ -n "$(git status --porcelain -- src/build.py src/content.py src/products.py src/links.json worker/src/index.js)" ]; then
    echo "src/ has uncommitted changes; skipping today's sweep so the rebuild does not publish work in progress"
    exit 0
  fi
  python3.12 "$REPO/tools/codesweep.py" "$@"
  echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) codesweep end (exit $?)"
} >>"$LOG" 2>&1
