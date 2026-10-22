#!/bin/bash
# Phase 2: after a wait, re-ask the ChatGPT cells of a run that read a pre-deploy copy of a page (stale_copy in
# grades.jsonl). The first-pass files are kept under stale-pass-<n>/; ui.py then fills the missing cells. One round
# per call; call again if cells are still stale.
#   growth/evals/rerun_stale.sh <run-id> <iteration> <sleep-seconds> [ui.py args...]
set -u
RUN="$1"; IT="$2"; SLEEP="$3"; shift 3
cd /Users/jiayiyao/Desktop/dealectric || exit 1
sleep "$SLEEP"
python3.12 growth/evals/grade.py --run-id "$RUN" --rescore --no-judge --no-d1 > /dev/null 2>&1
n=$(ls -d growth/evals/runs/$RUN/stale-pass-* 2>/dev/null | wc -l | tr -d ' ')
pass="growth/evals/runs/$RUN/stale-pass-$((n + 1))"
cells=$(python3.12 - "$RUN" <<'EOF'
import json, sys
rows = [json.loads(l) for l in open(f"growth/evals/runs/{sys.argv[1]}/grades.jsonl")]
print(" ".join(r["file"][8:-5] for r in rows if r["assistant"] == "chatgpt" and r["kind"] == "question" and r.get("stale_copy")))
EOF
)
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) stale cells: $cells"
[ -z "$cells" ] && { echo "nothing stale"; exit 0; }
mkdir -p "$pass"
for c in $cells; do
  mv "growth/evals/runs/$RUN/chatgpt/$c.json" "$pass/" 2>/dev/null
  mv "growth/evals/runs/$RUN/chatgpt/$c.jpg" "$pass/" 2>/dev/null
done
python3.12 -u growth/evals/ui.py --app chatgpt --run-id "$RUN" --phase 2 --iteration "$IT" "$@" 2>&1 | tail -4
python3.12 growth/evals/grade.py --run-id "$RUN" --rescore --no-judge --no-d1 > /dev/null 2>&1
python3.12 - "$RUN" <<'EOF'
import json, sys
rows = [json.loads(l) for l in open(f"growth/evals/runs/{sys.argv[1]}/grades.jsonl")]
s = [r["file"][8:-5] + "(" + (r.get("stale_strength") or "?")[0] + ")" for r in rows if r["assistant"] == "chatgpt" and r["kind"] == "question" and r.get("stale_copy")]
print("still stale after this round:", len(s), " ".join(s))
EOF
