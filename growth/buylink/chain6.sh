# plain-question reading 1 (retrofit + new pilot pages re-fetched by OAI-SearchBot since their change; untreated controls)
cd "$(dirname "$0")/../.."
for i in 1 2; do python3.12 growth/evals/buylink_probe.py --targets growth/focus/buylink-pilot-targets-r1.json --out growth/evals/runs/2026-11-13-buylink-pilot-r1 --suffix=-r$i --followups 0; done > growth/buylink/pilot-r1.log 2>&1
echo "chain6 done" >> growth/buylink/pilot-r1.log
