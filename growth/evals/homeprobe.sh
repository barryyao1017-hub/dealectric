#!/bin/bash
# Phase 2, iteration 4 (DLC-50): watch for ChatGPT's index copy of the HOME page turning over. Every GAP seconds ask
# the tier-E question of one coded product (default Q22, BLUETTI AC180) in a fresh temporary chat; the answer is
# "stale" while it quotes the pre-rebrand home-page sentence ("verified October 14, 2026"), FRESH once it quotes a
# 2026-10-2x cart-test date or the /go/ link without that sentence. Exit 0 on FRESH, 1 after MAX probes. One line per
# probe in growth/evals/runs/<run-id>/homeprobe.log; run files under growth/evals/runs/<run-id>/chatgpt/.
#   nohup growth/evals/homeprobe.sh Q22 2026-10-23-p2homeprobe 12 14400 &
set -u
Q="${1:-Q22}"; RUN="${2:-2026-10-23-p2homeprobe}"; MAX="${3:-12}"; GAP="${4:-14400}"
cd /Users/jiayiyao/Desktop/dealectric || exit 1
mkdir -p "growth/evals/runs/$RUN"
LOG="growth/evals/runs/$RUN/homeprobe.log"
for i in $(seq 1 "$MAX"); do
  [ "$i" -gt 1 ] && sleep "$GAP"
  if ! curl -s --max-time 3 localhost:9222/json/version > /dev/null; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) probe $i skipped: agent Chrome not running" | tee -a "$LOG"; continue
  fi
  n=$(ls growth/evals/runs/$RUN/chatgpt/$Q-E-*.json 2>/dev/null | wc -l | tr -d ' ')
  next=$((n + 1))
  python3.12 -u growth/evals/ui.py --app chatgpt --questions "$Q" --tiers E --n "$next" --controls none --phase 2 --run-id "$RUN" > /dev/null 2>&1
  f="growth/evals/runs/$RUN/chatgpt/$Q-E-$next.json"
  verdict=$(python3.12 - "$f" <<'PY'
import json, re, sys
try:
    r = json.load(open(sys.argv[1]))
except Exception as e:  # noqa: BLE001
    print("error", str(e)[:80]); sys.exit()
if r.get("error"):
    print("error", str(r["error"])[:80]); sys.exit()
t = r["text"] + " " + "\n".join(r["response"].get("markup") or [])
stale = "october 14, 2026" in t.lower() or "2026-10-14" in t
dated = bool(re.search(r"(?:Oct(?:ober)?\.? ?2\d, 2026|2026-10-2\d)", t))
go = any("/go/" in c["url"] for c in r["citations"])
print(("FRESH" if not stale and (dated or go) else "stale" if stale else "neither"), f"dated={dated} go={go}")
PY
)
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) probe $next $Q-E: $verdict" | tee -a "$LOG"
  case "$verdict" in FRESH*) exit 0;; esac
done
exit 1
