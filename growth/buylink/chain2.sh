#!/bin/zsh
# Buy-link pilot (DLC-250), reordered 11-11: new-page harvest first (research starts as chats land), then the rest of
# the buy-question baseline (the probe skips the chats already saved).
cd /Users/j0y0825/code/dealectric
python3.12 growth/evals/visibility_scan.py --questions growth/focus/ab-harvest-new-2026-11-11-pilot.json --run-id 2026-11-11-pilot-ab-harvest-new --n 2 --pace 30 --cooldown 2700 > growth/buylink/harvest-new.log 2>&1
echo "harvest exit $?" >> growth/buylink/harvest-new.log
for i in 1 2; do python3.12 growth/evals/buylink_probe.py --targets growth/focus/buylink-buyq-targets.json --out growth/evals/runs/2026-11-11-buylink-buyq-base --suffix=-b$i --followups 0; done >> growth/buylink/buyq-base.log 2>&1
echo "buyq-base exit $?" >> growth/buylink/buyq-base.log
