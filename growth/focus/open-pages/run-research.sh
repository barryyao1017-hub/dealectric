#!/bin/bash
# Research for the open-query pages in demand order (main session 11-15: home use first, CPAP second, then the queries
# open in every chat, then the two-of-three group), two queues in parallel. Retargeted pages were prepped with
# `openpage.py prep` (their earlier research moved to history/before-open-1115), so no --force is needed.
cd "$(dirname "$0")/../../.."
P1="best-solar-generator-for-power-outages oq-pm004-starts-biggest-appliances-for-size power-station-to-run-a-pellet-stove-in-an-outage oq-pr006-fan-all-night-most-nights oq-pn010-enclosed-3d-printer-fastest-abs quietest-1000wh-power-station-while-charging oq-pp006-charge-in-freezing-weather oq-pp004-recharges-fastest-from-solar best-240v-portable-power-station oq-ps003-robot-mower-wet-grass lightest-1000wh-lifepo4-power-station-for-car-camping"
P2="power-station-for-a-cpap-week-of-camping small-power-station-to-keep-wifi-router-and-modem-on-in-an-outage 1kwh-power-station-with-1000w-solar-input-two-ports oq-pq016-power-stations-linked-together solar-generator-that-can-run-a-well-pump 1000wh-power-station-that-can-run-a-microwave oq-pp002-most-of-advertised-capacity oq-pq006-charges-fastest-from-a-car oq-pn005-3d-scanner-big-car-part"
python3.12 growth/focus/open-pages/openpage.py research $P1 --workers 3 > growth/focus/open-pages/logs/research-1.log 2>&1 &
python3.12 growth/focus/open-pages/openpage.py research $P2 --workers 3 > growth/focus/open-pages/logs/research-2.log 2>&1 &
wait
echo RESEARCH DONE >> growth/focus/open-pages/logs/research-2.log
