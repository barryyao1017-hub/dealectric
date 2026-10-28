#!/bin/zsh
# DLC-51 daily readings for the query-targeted comparison pages (growth/query-pages.md, step 4). Run once a day from the
# repo root with the agent's Chrome up; everything lands in growth/evals/runs/<date>-qp/.
#
#   growth/evals/querypages_daily.sh            # today
#   growth/evals/querypages_daily.sh --no-chat  # engines only (skip the 16 ChatGPT chats)
#
# Readings: (1) indexed: Bing and Brave results for site:dealectric.com and for each page URL; (2) rank: serp.py on the
# eight target queries (four built clusters, four controls), with our position; (3) cited unprompted: ChatGPT tier A on
# the eight shopper questions, n = 2 (ui.py, run id <date>-qp), graded with grade.py. claude-code tier A is run from
# run.py separately when the CLI is available.
export FOOTPRINT_VIA="$(basename "$0")"   # tags footprint.jsonl entries written by the scripts below
set -euo pipefail
cd "$(dirname "$0")/../.."
DATE=${DATE:-$(date +%F)}
RUN="$DATE-qp"
OUT="growth/evals/runs/$RUN"
mkdir -p "$OUT"

# The eight clusters: built (Q17, Q16, Q21, Q25) and controls (Q15, Q18, Q19, Q20), each with ChatGPT's own query from
# the 2026-10-23 queryprobe run and the page we built for it (empty for a control).
cat > "$OUT/clusters.json" <<'EOF'
[
 {"qid": "Q17", "built": "https://dealectric.com/lifepo4-vs-nmc-power-stations",
  "query": "portable power station LiFePO4 NMC battery chemistry manufacturer comparison 2026"},
 {"qid": "Q16", "built": "https://dealectric.com/power-station-for-cpap",
  "query": "best portable power station for CPAP machine 2026 runtime humidifier pure sine wave"},
 {"qid": "Q21", "built": "https://dealectric.com/solar-watts-to-recharge-power-station",
  "query": "how many watts solar panel to recharge 1000Wh portable power station solar charging losses peak sun hours"},
 {"qid": "Q25", "built": "https://dealectric.com/aa-aaa-nimh-battery-charger-8-bay-16-bay",
  "query": "best high capacity AA AAA NiMH battery charger 8 bay 16 bay independent channels 2026 reviews"},
 {"qid": "Q15", "built": null, "query": "portable power station refrigerator backup sizing watt hours runtime inverter surge manufacturer guide"},
 {"qid": "Q18", "built": null, "query": "best home backup power stations under $1000 2026 reviews price battery capacity"},
 {"qid": "Q19", "built": null, "query": "portable power station UPS transfer time computer manufacturer guidance EcoFlow Anker Bluetti"},
 {"qid": "Q20", "built": null, "query": "best RV portable power station solar panel combo 2026 comparison EcoFlow Bluetti Jackery specs"}
]
EOF

# Bing only: Brave meets a burst of queries with a "Verifying you're not a bot" check (2026-10-23), which we do not solve;
# Claude's Brave-backed search is read through the claude-code run below instead.
echo "== $RUN: (1) indexed"
python3.12 growth/evals/serp.py --engines bing --out "$OUT/serp-indexed.json" --pause 5 --queries "site:dealectric.com" \
  "site:dealectric.com lifepo4" "site:dealectric.com cpap" "site:dealectric.com solar" "site:dealectric.com nimh charger"

echo "== $RUN: (2) rank for the eight queries"
python3.12 - "$OUT/clusters.json" > "$OUT/queries.txt" <<'EOF'
import json, sys
for c in json.load(open(sys.argv[1])): print(c["query"])
EOF
python3.12 growth/evals/serp.py --engines bing --queries-file "$OUT/queries.txt" --out "$OUT/serp-rank.json" --pause 5

if [[ "${1:-}" != "--no-chat" ]]; then
  echo "== $RUN: (3) ChatGPT unprompted, eight questions, n=2"
  python3.12 growth/evals/ui.py --app chatgpt --tiers A --controls none --n 2 --questions Q17,Q16,Q21,Q25,Q15,Q18,Q19,Q20 \
    --run-id "$RUN" --phase 3 --iteration 0 --pause 4
  echo "== $RUN: (3b) Claude as an agent (Brave-backed search), unprompted, n=1"
  python3.12 growth/evals/run.py --assistants claude-code --tiers A --controls none --n 1 --questions Q17,Q16,Q21,Q25,Q15,Q18,Q19,Q20 \
    --run-id "$RUN" --phase 3 --iteration 0 || echo "claude-code run skipped: $?"
fi

python3.12 - "$OUT" <<'EOF'
import json, sys, glob, os
out = sys.argv[1]
clusters = json.load(open(f"{out}/clusters.json"))
rank = json.load(open(f"{out}/serp-rank.json"))
idx = json.load(open(f"{out}/serp-indexed.json"))
site = idx["site:dealectric.com"]["bing"]
print("\nsite:dealectric.com on Bing ->", [r["url"].split("dealectric.com")[-1] for r in site if r.get("rank")])

def cited(files, built):
    us = page = 0
    for f in files:
        d = json.load(open(f))
        urls = set(d.get("all_urls", [])) | {x["url"] for x in (d.get("response") or {}).get("search_results", [])} | set(d.get("consulted") or [])
        if any("dealectric.com" in u for u in urls): us += 1
        if built and any(built.split("//")[-1] in u for u in urls): page += 1
    return f"{us}/{len(files)} ({page})"

print(f"{'qid':4} {'built':5} {'bing rank':>9}  chatgpt-A cites us/n (page)  claude-code-A cites us/n (page)")
for c in clusters:
    r = rank.get(c["query"], {}).get("dealectric_rank", {})
    print(f"{c['qid']:4} {'yes' if c['built'] else 'ctrl':5} {str(r.get('bing')):>9}  {cited(sorted(glob.glob(f'{out}/chatgpt/{c['qid']}-A-*.json')), c['built']):>22}  "
          f"{cited(sorted(glob.glob(f'{out}/claude-code/{c['qid']}-A-*.json')), c['built']):>22}")
EOF
