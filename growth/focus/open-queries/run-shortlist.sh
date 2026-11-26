#!/bin/bash
# Ask the 66 demand-shortlisted questions with the panel probe, AFTER the fork's two probes are done with the ChatGPT
# account (Barry 2026-11-15: "Yes, ask them"). One ChatGPT driver at a time.
cd /Users/j0y0825/code/dealectric
L=growth/focus/open-queries/shortlist-run.log
busy() { pgrep -f "panelprobe.py|openscan.py run|visibility_scan.py|followup_probe.py|buylink_probe.py|cardprobe.py" >/dev/null; }
idle=0
while true; do
  if busy; then idle=0
  else
    idle=$((idle+1))
    # the fork's product probe ends with qid prod14; otherwise go ahead once the account has been idle 20 minutes
    if grep -lq '"qid": "prod14"' growth/evals/runs/*/panels.jsonl 2>/dev/null && [ $idle -ge 4 ]; then break; fi
    if [ $idle -ge 40 ]; then break; fi
  fi
  sleep 30
done
echo "$(date -u +%FT%TZ) start shortlist" >> $L
for i in 1 2 3 4 5 6; do
  python3.12 growth/evals/panelprobe.py --run-id 2026-11-15-shortlist --queries growth/focus/open-queries/shortlist-queue.jsonl --max-clicks 4 >> $L 2>&1
  rc=$?
  echo "$(date -u +%FT%TZ) panelprobe exit $rc (pass $i)" >> $L
  if [ $rc -eq 0 ] || [ $rc -eq 3 ]; then break; fi
  sleep 90
done
echo "$(date -u +%FT%TZ) DONE rc=$rc" >> $L
