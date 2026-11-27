#!/bin/bash
# Daily cart check of every published discount code (tools/codesweep.py), run by launchd:
#   ~/Library/LaunchAgents/com.jiayiyao.dealectric.codesweep.plist  (daily, 06:37 local)
# It runs from the clone at ~/code/dealectric, not the Desktop checkout: macOS denies launchd-spawned processes
# access to ~/Desktop ("Operation not permitted", seen 2026-10-22). The clone is the sweep's alone: each run resets it
# to origin/main, then pushes its commit; pull the Desktop checkout before working there. Checks, merges, rebuilds, commits, pushes and redeploys
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
  # A paced sweep can outlast a day's gap (a hand run at 03:30 was still going at 06:37 on 11-26). The reset below
  # would pull the clone out from under it, so a run that finds another sweep or its gap-mining tail still going
  # stops here.
  if pgrep -f "tools/codesweep.py|growth/evals/gapmine.py daily|tools/gappage.py next|tools/upkeep/run.py" >/dev/null; then
    echo "another sweep is still running; skipping this run so the reset does not touch its clone"
    end 4
  fi
  if ! curl -s --max-time 5 http://localhost:9222/json/version >/dev/null; then
    echo "starting the agent's Chrome"
    uv --directory "$HOME/Desktop/agent-vault" run agent-vault browser || echo "agent-vault browser exited $? (under launchd, ~/Desktop may be off limits; start it by hand)"
    for i in $(seq 1 30); do curl -s --max-time 5 http://localhost:9222/json/version >/dev/null && break; sleep 2; done
    curl -s --max-time 5 http://localhost:9222/json/version >/dev/null || { echo "no agent Chrome on localhost:9222; skipping today's sweep"; end 2; }
  fi
  cd "$REPO" || end 1
  # The commit guard (tools/githooks/pre-commit, DLC-267) is a per-clone git setting: keep it on in this clone.
  git config core.hooksPath tools/githooks
  # This clone belongs to the sweep alone (Barry, 2026-11-26): sessions work in ~/Desktop/dealectric, and nothing else
  # edits here. So each run throws away whatever the clone holds and takes GitHub's main outright. Merging instead
  # jammed the sweep from 11-04 to 11-26 on a coupons.json conflict. All that can be lost is an earlier run's unpushed
  # result, which this run re-tests anyway; it is logged below. A missed day shows in the daily update.
  git rebase --abort 2>/dev/null; git merge --abort 2>/dev/null
  if ! git fetch -q origin main; then
    echo "git fetch failed; skipping today's sweep"
    end 1
  fi
  unpushed="$(git log --oneline origin/main..HEAD 2>/dev/null)"
  dirty="$(git status --porcelain --untracked-files=all | wc -l | tr -d ' ')"
  [ -n "$unpushed" ] && echo "discarding unpushed commits: $(echo "$unpushed" | tr '\n' ';')"
  [ "$dirty" != "0" ] && echo "discarding $dirty uncommitted or untracked path(s) left by an earlier run"
  git reset -q --hard origin/main && git clean -fdq && git stash clear || { echo "reset to origin/main failed; skipping today's sweep"; end 1; }
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
  # Weekly catalog upkeep for every brand (Barry 2026-11-27; growth/stock/README.md): on Sundays, after the code tests,
  # read every listed product, update records and every page that mentions a changed one, keep alternatives right,
  # rebuild, commit, push, deploy and check links. A long job (hours); caffeinate keeps the Mac awake. Off while
  # growth/stock/UPKEEP_OFF exists. It starts from GitHub's main so it includes the sweep's and gapmine's pushes.
  if [ "$(date +%u)" = "7" ] && [ ! -f "$REPO/growth/stock/UPKEEP_OFF" ] && [ "$rc" -eq 0 ]; then
    echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) upkeep start"
    if git fetch -q origin main && git reset -q --hard origin/main; then
      /usr/bin/caffeinate -i python3.12 "$REPO/tools/upkeep/run.py"; u=$?
    else
      u=9; echo "upkeep: could not take origin/main"
    fi
    echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) upkeep end (exit $u)"
  fi
  end $rc
} >>"$LOG" 2>&1
