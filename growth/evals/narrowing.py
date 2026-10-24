#!/usr/bin/env python3.12
"""Does narrowing the query make Dealectric surface? (DLC-51, 2026-10-24.) For four products whose pages ChatGPT's index
already holds, ask unprompted (Dealectric never named) a ladder of four questions from broad to narrow and record, per
chat, ChatGPT's own search queries, the result list it was shown and its citations (ui.ask_chatgpt). Then
`serp.py --engines bing --from-run <run>` ranks each issued query on Bing, and the summary below gives, per rung, how
often dealectric.com was retrieved (in the result list) and cited.

    python3.12 growth/evals/narrowing.py --run-id 2026-10-24-narrowing --n 2
    python3.12 growth/evals/narrowing.py --run-id 2026-10-24-narrowing --summary
"""
from __future__ import annotations

import argparse, glob, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import ui  # noqa: E402

# rung 1 category, 2 spec-narrowed category, 3 exact model, 4 exact model + a code that works at checkout
LADDERS = {
    "ac180": ["What's the best portable power station?",
              "What's the best 1,000 Wh LiFePO4 portable power station under $500?",
              "BLUETTI AC180: what's the current price and the key specs?",
              "Is there a BLUETTI AC180 discount code that actually works at checkout right now?"],
    "picogo": ["What's the best magnetic power bank for an iPhone?",
               "What's the best Qi2.2 25W magnetic power bank with 10,000 mAh?",
               "Baseus PicoGo AM52: what's the current price and the key specs?",
               "Is there a Baseus PicoGo AM52 discount code that actually works at checkout right now?"],
    "spaceone": ["What are the best noise-cancelling headphones?",
                 "What are the best noise-cancelling headphones under $100?",
                 "Soundcore Space One: what's the current price and battery life?",
                 "Is there a Soundcore Space One discount code that actually works at checkout right now?"],
    "r4000": ["What's the best power station for home backup?",
              "What's the best power station over 3,000 Wh with 3,600 W output for home backup?",
              "ALLPOWERS R4000: what's the current price and the key specs?",
              "Is there an ALLPOWERS R4000 discount code that actually works at checkout right now?"],
}


def ours(urls):
    return any("dealectric.com" in (u or "") for u in urls)


def summary(run_id):
    rd = E.run_dir(run_id)
    serp = json.load(open(rd / "serp.json")) if (rd / "serp.json").exists() else {}
    print(f"{'rung':4} {'chats':>5} {'retrieved':>9} {'cited':>6} {'go-link':>7}  bing rank of ChatGPT's queries (ours)")
    for rung in range(1, 5):
        files = [f for k in LADDERS for f in glob.glob(str(rd / "chatgpt" / f"{k}-{rung}-*.json"))]
        ret = cit = go = 0; ranks = []
        for f in files:
            d = json.load(open(f))
            res = [x["url"] for x in (d.get("response") or {}).get("search_results", [])]
            ret += ours(res); cit += ours(d.get("all_urls", [])); go += any("/go/" in u for u in d.get("all_urls", []))
            for q in d.get("queries") or []:
                ranks.append((serp.get(q, {}).get("dealectric_rank") or {}).get("bing"))
        print(f"{rung:4} {len(files):5} {ret:9} {cit:6} {go:7}  {ranks}")
    print("\nper product:")
    for k in LADDERS:
        cells = []
        for rung in range(1, 5):
            fs = sorted(glob.glob(str(rd / "chatgpt" / f"{k}-{rung}-*.json")))
            r = sum(ours([x["url"] for x in (json.load(open(f)).get("response") or {}).get("search_results", [])]) for f in fs)
            c = sum(ours(json.load(open(f)).get("all_urls", [])) for f in fs)
            cells.append(f"r{rung} {r}/{c}/{len(fs)}")
        print(f"  {k:9} " + "   ".join(cells) + "   (retrieved/cited/n)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True); ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--summary", action="store_true"); ap.add_argument("--pause", type=float, default=4)
    a = ap.parse_args()
    if a.summary:
        return summary(a.run_id)
    for i in range(1, a.n + 1):
        for k, ladder in LADDERS.items():
            for rung, prompt in enumerate(ladder, 1):
                out = E.run_dir(a.run_id) / "chatgpt" / f"{k}-{rung}-{i}.json"
                if out.exists():
                    continue
                rec = {"run_id": a.run_id, "assistant": "chatgpt", "qid": f"{k}-{rung}", "tier": "A", "n": i, "prompt": prompt,
                       "started_at": E.now_iso()}
                for attempt in range(4):
                    try:
                        rec.update(ui.ask_chatgpt(prompt, out.with_suffix(".jpg"))); rec["error"] = None; break
                    except ui.Throttled as t:
                        print(f"throttled, waiting {t.wait_s + 30}s", flush=True); time.sleep(t.wait_s + 30)
                    except Exception as e:  # noqa: BLE001
                        rec.update({"error": f"{type(e).__name__}: {e}", "queries": [], "all_urls": [], "response": None}); break
                rec["all_urls"] = sorted({c["url"] for c in rec.get("citations", [])})
                rec["finished_at"] = E.now_iso()
                E.write_json(out, rec)
                print(f"{k}-{rung}-{i}: queries={rec.get('queries')} ours_retrieved={ours([x['url'] for x in (rec.get('response') or {}).get('search_results', [])])} "
                      f"ours_cited={ours(rec['all_urls'])} err={rec.get('error')}", flush=True)
                time.sleep(a.pause)


if __name__ == "__main__":
    main()
