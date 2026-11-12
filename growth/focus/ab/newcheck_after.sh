#!/bin/zsh
# Waits for the reading-1b scan to finish, then runs the new-page retrieval check in the same Agent Chrome.
cd /Users/j0y0825/code/dealectric
while ! grep -q "reading1b exit" growth/focus/ab/reading1b.log 2>/dev/null; do sleep 60; done
python3.12 growth/evals/visibility_scan.py --questions growth/focus/ab-newcheck-2026-11-10.json --run-id 2026-11-10-ab-newcheck --n 1 --cooldown 2700 > growth/focus/ab/newcheck.log 2>&1
echo "newcheck exit $?" >> growth/focus/ab/newcheck.log
