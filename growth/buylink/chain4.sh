# where-to-buy baseline for the third batch of cheapest-link products (before their product pages change)
cd "$(dirname "$0")/../.."
for i in 1 2; do python3.12 growth/evals/buylink_probe.py --targets growth/focus/buylink-buyq-targets-3.json --out growth/evals/runs/2026-11-11-buylink-buyq3-base --suffix=-b$i --followups 0; done > growth/buylink/buyq3-base.log 2>&1
echo "chain4 done" >> growth/buylink/buyq3-base.log
