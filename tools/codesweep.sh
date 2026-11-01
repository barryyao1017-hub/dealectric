#!/bin/bash
# Daily cart check of every published discount code (tools/codesweep.py), run by launchd:
#   ~/Library/LaunchAgents/com.jiayiyao.dealectric.codesweep.plist  (daily, 06:37 local)
# It runs from the clone at ~/code/dealectric, not the Desktop checkout: macOS denies launchd-spawned processes
# access to ~/Desktop ("Operation not permitted", seen 2026-10-22). The clone pulls main first and pushes its
# commit; pull the Desktop checkout before working there. Checks, merges, rebuilds, commits, pushes and redeploys
# the Worker when the link map changed. Log: ~/Library/Logs/claude-automations/dealectric-codesweep.log
set -u
export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="${HOME:-/Users/jiayiyao}"
REPO="$HOME/code/dealectric"
LOG_DIR="$HOME/Library/Logs/claude-automations"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/dealectric-codesweep.log"
{
  echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) codesweep start"
  # Every stop, early ones included, writes the end line with its exit code, so tools/dailyupdate.py reports a skipped
  # day as FAILED instead of "still running" (2026-10-31).
  end() { echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) codesweep end (exit $1)"; exit "$1"; }
  if ! curl -s --max-time 5 http://localhost:9222/json/version >/dev/null; then
    echo "starting the agent's Chrome"
    uv --directory "$HOME/Desktop/agent-vault" run agent-vault browser || echo "agent-vault browser exited $? (under launchd, ~/Desktop may be off limits; start it by hand)"
    for i in $(seq 1 30); do curl -s --max-time 5 http://localhost:9222/json/version >/dev/null && break; sleep 2; done
    curl -s --max-time 5 http://localhost:9222/json/version >/dev/null || { echo "no agent Chrome on localhost:9222; skipping today's sweep"; end 2; }
  fi
  cd "$REPO" || end 1
  # Local edits to tracked files made --ff-only refuse (2026-10-31: a line appended to growth/evals/footprint.jsonl
  # skipped the day). --autostash sets them aside and puts them back, .gitattributes merges the append-only logs line
  # by line, and --rebase replays a sweep commit whose push failed on an earlier run.
  if ! git pull -q --rebase --autostash origin main; then
    git rebase --abort 2>/dev/null
    echo "git pull failed; skipping today's sweep"
    end 1
  fi
  if [ -n "$(git diff --name-only --diff-filter=U)" ]; then
    echo "local changes clash with main after the pull (kept in git stash list): $(git diff --name-only --diff-filter=U | tr '\n' ' ')skipping today's sweep"
    end 1
  fi
  # Never run on a dirty tree the loop session is mid-edit on: the sweep commits only its own files, but a rebuild
  # would publish whatever is in src/. Uncommitted changes outside the sweep's own files mean skip today (exit 3, so
  # the daily update flags it).
  if [ -n "$(git status --porcelain -- src/build.py src/content.py src/products.py src/links.json worker/src/index.js)" ]; then
    echo "src/ has uncommitted changes; skipping today's sweep so the rebuild does not publish work in progress"
    end 3
  fi
  # The paced sweep can take a few hours when stores rate-limit (DLC-48); caffeinate -i keeps the Mac from idle-sleeping
  # until it ends (only for this process; no setting changes).
  /usr/bin/caffeinate -i python3.12 "$REPO/tools/codesweep.py" "$@"
  end $?
} >>"$LOG" 2>&1
