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
  # The commit guard (tools/githooks/pre-commit, DLC-267) is a per-clone git setting: keep it on in this clone.
  git config core.hooksPath tools/githooks
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
  rc=$?
  # Daily $0 gap mining and page drafts (DLC-168/175, Barry's yes 2026-11-05; growth/gapmine/daily-plan.md). Runs only
  # after a clean sweep on a clean src/ and docs/ (gappage.py refuses a dirty tree; since DLC-267 its undo reverts only
  # its own insert). Drafts only, unless growth/gapmine/AUTOPUBLISH exists (Barry turns that on). Its own exit codes are
  # logged on the "gapmine" lines; the end line keeps the sweep's code for tools/dailyupdate.py.
  if [ "$rc" -eq 0 ] && [ -z "$(git status --porcelain -- src docs worker/src)" ]; then
    echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) gapmine start"
    /usr/bin/caffeinate -i python3.12 "$REPO/growth/evals/gapmine.py" daily; g1=$?
    if [ -f "$REPO/growth/gapmine/AUTOPUBLISH" ]; then
      /usr/bin/caffeinate -i python3.12 "$REPO/tools/gappage.py" next --publish; g2=$?
    else
      /usr/bin/caffeinate -i python3.12 "$REPO/tools/gappage.py" next; g2=$?
    fi
    # Commit the run's own records (queue, ledger, daily log, drafts, pool) so the other checkout sees them.
    git add -- growth/gapmine growth/evals/runs/fastloop 2>/dev/null
    if ! git diff --cached --quiet; then
      git commit -q -m "gapmine: daily run $(date +%Y-%m-%d)" && { git push -q origin HEAD:main || echo "gapmine push failed (next run retries)"; }
    fi
    echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) gapmine end (daily exit $g1, page exit $g2)"
  else
    echo "gapmine skipped: sweep exit $rc or src/docs not clean"
  fi
  end $rc
} >>"$LOG" 2>&1
