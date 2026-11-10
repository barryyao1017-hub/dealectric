"""Write growth/focus/ab-harvest-new-<DAY>.json from the queue's status-new clusters (DLC-208 method for new pages).
Each cluster's scored query is the chat prompt; page folders are n<MMDD>-<cluster>."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
day = sys.argv[1]
tag = "n" + day[5:7] + day[8:10]
q = [x for x in json.loads((ROOT / "growth/gapmine/queue.json").read_text()) if x["status"] == "new"]
out = []
for i, x in enumerate(q):
    key = re.sub(r"[^a-z0-9]+", "-", x["cluster"].lower()).strip("-")
    out.append({"qid": f"{tag}-{i:02d}-{key[:30]}--plain", "slug": f"{tag}-{key}", "cluster": x["cluster"], "level": "G2",
                "type": "gap", "mode": "natural", "search": False, "prompt": x["supply_query"]})
(ROOT / f"growth/focus/ab-harvest-new-{day}.json").write_text(json.dumps(
    {"version": day, "note": f"New gap clusters from gapmine daily {day}: each cluster's scored query typed as is, plain prompt, two chats, before research (DLC-208 method).",
     "questions": out}, indent=1))
for o in out:
    print(o["slug"], "|", o["prompt"])
