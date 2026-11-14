#!/bin/bash
# Combo run: every round, read Amazon prices for new listings, price-check newly applied pages, publish. Ends after the
# applier has finished and one last round has run.
cd "$(dirname "$0")/../.."
last=0
while true; do
  echo "[cycle $(date +%H:%M)] round"
  python3.12 tools/combopage.py amazon 2>&1 | tail -1 | cut -c1-160
  folders=$(python3.12 - <<'PY'
import json, glob
out = []
for f in sorted(glob.glob("growth/focus/ab/c1113-*/draft.json")):
    d = json.load(open(f))
    if (d.get("gate") or {}).get("pass") and not d.get("kit_page") and not d.get("bundle_compare"):
        out.append(f.split("/")[3])
print(" ".join(out))
PY
)
  [ -n "$folders" ] && python3.12 tools/combopage.py price $folders --pace 45 2>&1 | grep -E "lowest|flagged|captcha|stopping" | cut -c1-300
  for i in $(seq 1 20); do out=$(bash growth/combo/publish.sh 2>&1); case "$out" in *"try later"*) sleep 30;; *) echo "$out" | grep -E "pushed|indexnow|pages deploy|failed|UNRESOLVED|PUBLISH DONE" ; break;; esac; done
  [ "$last" = 1 ] && break
  if grep -q "APPLY DONE" growth/combo/apply-all3.log 2>/dev/null && ! pgrep -f "growth/combo/applyloop.py" >/dev/null; then last=1; continue; fi
  sleep 1200
done
echo "[cycle $(date +%H:%M)] CYCLE DONE"
