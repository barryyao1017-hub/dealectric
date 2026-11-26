"""Between batches of the parked-queue run: score what has been asked, list the questions that came back open and
still need a second chat, and list the ones open in both chats that have not been sent for pages yet.
    python3.12 growth/focus/open-queries/cycle.py            # prints the state, writes parked-confirm-queue.jsonl
State files: report/parked-results.json, report/parked-confirm-results.json, parked-sent.json (qids sent for pages)."""
import json, subprocess, sys, collections
from pathlib import Path
H = Path(__file__).resolve().parent
def score(run, out):
    subprocess.run([sys.executable, str(H / "shortlist_score.py"), run, str(H / "parked-queue.jsonl"), out, "--quiet"], capture_output=True, text=True)
    p = H / "report" / out
    return {x["qid"]: x for x in json.loads(p.read_text())} if p.exists() else {}
first = score("2026-11-15-parked", "parked-results.json")
conf = score("2026-11-15-parked-confirm", "parked-confirm-results.json") if (H.parent.parent / "evals/runs/2026-11-15-parked-confirm/panels.jsonl").exists() else {}
sent = set(json.loads((H / "parked-sent.json").read_text())) if (H / "parked-sent.json").exists() else set()
q = {json.loads(l)["qid"]: json.loads(l) for l in (H / "parked-queue.jsonl").read_text().splitlines() if l.strip()}
opens = [k for k, x in first.items() if x["verdict"] == "open"]
need = [k for k in opens if k not in conf]
both = [k for k in opens if k in conf and conf[k]["verdict"] == "open"]
flip = [k for k in opens if k in conf and conf[k]["verdict"] != "open"]
(H / "parked-confirm-queue.jsonl").write_text("".join(json.dumps(q[k], ensure_ascii=False) + "\n" for k in opens if k in q))   # panelprobe skips the ones already done
print("asked", len(first), dict(collections.Counter(x["verdict"] for x in first.values())))
print("open on first chat", len(opens), "| awaiting second chat", len(need), "| open in both", len(both), "| not open on second", len(flip), "| already sent", len(sent & set(both)))
for k in both:
    if k not in sent:
        a, b = first[k], conf[k]
        print("  TO SEND", k[:5], "|", a["prompt"], "| free:", sorted(set(a["free"] + b["free"]))[:5], "| cited:", sorted(set(a["cited"] + b["cited"]))[:5])
for k in need:
    print("  needs 2nd chat", k[:5], "|", first[k]["prompt"][:90])
json.dump({"both": both, "need": need, "flip": flip}, open(H / "parked-state.json", "w"), indent=1)
