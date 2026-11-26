"""Question-shaped autocomplete for the open-query discovery (2026-11-14, Barry): real suggestions only.
Seeds x question stems -> Google and Bing autocomplete (gapmine.ac, same pacing) -> pool-qstems.json (resumes)."""
import json, sys
from pathlib import Path
sys.path.insert(0, 'growth/evals')
import gapmine as G
OUT = Path('growth/focus/open-queries/pool-qstems.json')
SOLAR = ["solar generator", "portable power station", "power station", "solar generator kit", "home battery backup", "battery backup for home"]
OTHER = ["3d scanner", "portable air conditioner", "tent air conditioner", "robot lawn mower", "projector screen", "golf cart lithium battery",
         "lifepo4 battery", "crawl space dehumidifier", "3d printer", "trolling motor battery", "rv lithium battery", "solar inverter"]
STEMS = ["can a {s} run", "can a {s} power", "can a {s} charge", "can i use a {s}", "will a {s} run", "how long will a {s}", "how long does a {s}",
         "what size {s} do i need", "what size {s} for", "how big of a {s}", "how many watts {s}", "do i need a {s}", "which {s} for", "which {s} should i",
         "what {s} should i", "what can a {s}", "what is the best {s} for", "{s} to run", "{s} to power", "{s} that can", "{s} big enough", "{s} for a",
         "{s} for my", "{s} or", "what do i need for a {s}", "how to choose a {s}", "is a {s} enough", "why does my {s}", "should i buy a {s}", "{s} worth it for"]
res = json.loads(OUT.read_text()) if OUT.exists() else {}
for group, seeds in (("solar", SOLAR), ("other", OTHER)):
    for s in seeds:
        for t in STEMS:
            p = t.format(s=s)
            for eng in ("google", "bing"):
                k = f"{eng}|{p}"
                if k in res: continue
                r = G.ac(eng, p)
                res[k] = {"group": group, "seed": s, "stem": t, "sug": r}
        OUT.write_text(json.dumps(res, indent=0))
        print(group, s, sum(len(v["sug"] or []) for v in res.values() if v["seed"] == s), flush=True)
