#!/bin/bash
# New-cluster harvest for $DAY (two plain chats per cluster). Stops at the first downgraded answer (quota); research
# runs on whatever is harvested, and the script can be re-run later to finish the rest (cells already done are kept).
cd "$(dirname "$0")/../../.."
python3.12 growth/evals/visibility_scan.py --questions growth/focus/ab-harvest-new-${DAY}.json --run-id ${DAY}-ab-harvest-new --n 2 --pace 30 --stop-on-limit
rc=$?; echo "new harvest exit $rc"
[ $rc -eq 3 ] && { echo "QUOTA: stopped in the new-cluster harvest"; exit 3; }
echo "HARVEST DONE"
