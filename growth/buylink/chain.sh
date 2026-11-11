#!/bin/zsh
# Buy-link pilot (DLC-237): ChatGPT chats one at a time, after the baseline: buy-question baseline, then new-page harvest.
cd /Users/j0y0825/code/dealectric
while ! grep -q "pilot-base exit" growth/buylink/pilot-base.log 2>/dev/null; do sleep 60; done
for i in 1 2; do python3.12 growth/evals/buylink_probe.py --targets growth/focus/buylink-buyq-targets.json --out growth/evals/runs/2026-11-11-buylink-buyq-base --suffix=-b$i --followups 0; done > growth/buylink/buyq-base.log 2>&1
echo "buyq-base exit $?" >> growth/buylink/buyq-base.log
python3.12 growth/evals/visibility_scan.py --questions growth/focus/ab-harvest-new-2026-11-11-pilot.json --run-id 2026-11-11-pilot-ab-harvest-new --n 2 --pace 30 --cooldown 2700 > growth/buylink/harvest-new.log 2>&1
echo "harvest exit $?" >> growth/buylink/harvest-new.log
