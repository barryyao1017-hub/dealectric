"""Barry 2026-11-15 cut the run to two pages (home use, CPAP). Angle agents already running finish (paid work, kept in the
research library); this kills any compose / verify / fix agent for the other queries before it spends anything."""
import subprocess, time, re, os
OUT = ["which power station can run a " + "cpap for the most nights",   # its angles feed /power-station-for-cpap instead
       "which power station runs a pellet stove the longest", "which power station keeps a wifi router running the longest",
       "which power station can start the biggest appliances for its size", "which power station takes the fewest hours of sun",
       "which power stations still charge in freezing weather", "which power station gives you the most of its advertised capacity"]
JOBS = ["Your job: decide the page's angle", "Your job: verify a page before", "Your job: fix a page draft", "A buying page opens with this answer"]
while True:
    ps = subprocess.run(["ps", "-axww", "-o", "pid=,args="], capture_output=True, text=True).stdout.splitlines()
    for l in ps:
        if " -p " not in l or "claude" not in l:
            continue
        if any(j in l for j in JOBS) and any(q in l for q in OUT):
            pid = int(l.split()[0])
            print(time.strftime("%H:%M:%S"), "killed", pid, next(q for q in OUT if q in l), flush=True)
            os.kill(pid, 15)
    if not subprocess.run(["pgrep", "-f", "open-pages/run-research.sh"], capture_output=True).stdout.strip():
        break
    time.sleep(5)
