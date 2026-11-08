#!/bin/bash
# Harvest chats in priority order (Barry 11-08): today's new clusters, then group A. Each scan stops at the first
# downgraded answer (quota); research and page work continue from what's harvested, and the chain is re-run later.
cd "$(dirname "$0")/../../.."
python3.12 growth/evals/visibility_scan.py --questions growth/focus/ab-harvest-new-2026-11-08.json --run-id 2026-11-08-ab-harvest-new --n 2 --pace 30 --stop-on-limit
rc=$?; echo "new harvest exit $rc"
[ $rc -eq 3 ] && { echo "QUOTA: stopped in the new-cluster harvest"; exit 3; }
python3.12 growth/evals/visibility_scan.py --questions growth/focus/ab-harvest-A.json --run-id 2026-11-08-ab-harvest-A --n 2 --pace 30 --stop-on-limit
rc=$?; echo "A harvest exit $rc"
[ $rc -eq 3 ] && { echo "QUOTA: stopped in the group A harvest"; exit 3; }
echo "HARVEST DONE"
