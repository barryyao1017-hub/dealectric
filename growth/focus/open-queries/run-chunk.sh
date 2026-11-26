#!/bin/bash
# The parked-queue run (Barry 2026-11-15: "Continue the process here"), one step: for each "<queries.jsonl> <run id>"
# pair given, ask those questions with the panel probe, in order. Before every pass it checks that ChatGPT is signed in
# and signs back in with Google if not (chatgpt_login.py). When the quota runs out (panelprobe exit 3) it sleeps 80
# minutes and tries again.
#   run-chunk.sh <queries> <run id> [<queries> <run id> ...]
cd /Users/j0y0825/code/dealectric
L=growth/focus/open-queries/parked-run.log
busy() { pgrep -f "panelprobe.py|openscan.py run|visibility_scan.py|followup_probe.py|buylink_probe.py|cardprobe.py" >/dev/null; }
probe() {   # $1 queries, $2 run id
  [ -s "$1" ] || return 0
  fails=0
  for i in $(seq 1 40); do
    while busy; do sleep 30; done
    python3.12 growth/focus/open-queries/chatgpt_login.py >> $L 2>&1; lrc=$?
    if [ $lrc -eq 2 ]; then echo "$(date -u +%FT%TZ) LOGIN NEEDS BARRY" >> $L; return 2; fi
    if [ $lrc -ne 0 ]; then echo "$(date -u +%FT%TZ) login failed, retry in 5 min" >> $L; sleep 300; continue; fi
    python3.12 growth/evals/panelprobe.py --run-id "$2" --queries "$1" --max-clicks 4 >> $L 2>&1
    rc=$?
    echo "$(date -u +%FT%TZ) panelprobe $2 exit $rc (pass $i)" >> $L
    [ $rc -eq 0 ] && return 0
    if [ $rc -eq 3 ]; then echo "$(date -u +%FT%TZ) quota: sleeping 80 min" >> $L; sleep 4800; fails=0
    else fails=$((fails+1)); [ $fails -ge 6 ] && { echo "$(date -u +%FT%TZ) six failures in a row, stopping" >> $L; return 1; }; sleep 90; fi
  done
  return 1
}
echo "$(date -u +%FT%TZ) STEP start $*" >> $L
rc=0
while [ $# -ge 2 ]; do probe "$1" "$2" || { rc=$?; break; }; shift 2; done
echo "$(date -u +%FT%TZ) STEP DONE rc=$rc" >> $L
