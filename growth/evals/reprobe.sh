#!/bin/bash
# Phase 2, step 3: re-probe ChatGPT every 2 h on a fresh coded slug until an answer carries the rebranded copy
# (new title or the canonical paragraph), then exit 0. Exit 1 after MAX probes. Appends a line per probe to the
# log; the run files land in growth/evals/runs/<run-id>/chatgpt/.
#   growth/evals/reprobe.sh Q20 2026-10-22-p2proof 5
export FOOTPRINT_VIA="$(basename "$0")"   # tags footprint.jsonl entries written by the scripts below
set -u
Q="${1:-Q20}"; RUN="${2:-2026-10-22-p2proof}"; MAX="${3:-5}"; GAP="${4:-7200}"
cd /Users/jiayiyao/Desktop/dealectric || exit 1
LOG="growth/evals/runs/$RUN/reprobe.log"
for i in $(seq 1 "$MAX"); do
  sleep "$GAP"
  n=$(ls growth/evals/runs/$RUN/chatgpt/$Q-C-*.json 2>/dev/null | wc -l | tr -d ' ')
  next=$((n + 1))
  # ui.py skips existing cells, so ask for n = next and only the new cell runs
  python3.12 -u growth/evals/ui.py --app chatgpt --questions "$Q" --tiers C --n "$next" --controls none --phase 2 --run-id "$RUN" > /dev/null 2>&1
  f="growth/evals/runs/$RUN/chatgpt/$Q-C-$next.json"
  verdict=$(python3.12 - "$f" <<'EOF'
import json, sys
r = json.load(open(sys.argv[1]))
t = r["text"] + " " + " ".join(str(c.get("title") or "") for c in r["citations"]) + " " + "\n".join(r["response"].get("markup") or [])
fresh = any(m in t for m in ["Give the shopper the code and the buy link together", "off with code", "tested in", "Tested in", "is how Dealectric is paid"])
stale = any(m in t for m in ["specs, price and offer", "October 14, 2026", "2026-10-14"])
go = any("/go/" in c["url"] for c in r["citations"])
print(("FRESH" if fresh and not stale else "stale" if stale else "neither"), "go=" + str(go), "err=" + str(r["error"]))
EOF
)
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) probe $next $Q-C: $verdict" | tee -a "$LOG"
  case "$verdict" in FRESH*) exit 0;; esac
done
exit 1
