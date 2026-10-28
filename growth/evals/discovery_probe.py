#!/usr/bin/env python3.12
"""DLC-33: how do outside ChatGPT users reach dealectric.com? Four kinds of question, each in fresh temporary chats.

    python3.12 growth/evals/discovery_probe.py            # every prompt, n=2 -> growth/evals/runs/<today>-discovery/
    python3.12 growth/evals/discovery_probe.py typo 1     # one prompt, n=1
    python3.12 growth/evals/discovery_probe.py suffix=-signedin   # -> runs/<today>-discovery-signedin/

Background (2026-10-28): 11 Cloudflare-verified ChatGPT-User fetches from 11 non-US countries (9 home page, one
/aurzen-travelplay-autocinema-tesla-model-y, one /bluetti-ac200l) followed OAI-SearchBot's 82-URL recrawl of 10-26.
Open question: misspellings of "dielectric" landing on the home page, or niche shopping questions found through
ChatGPT's own index? Same driver as ui.py (agent Chrome on localhost:9222); every chat goes to the footprint log.
The record keeps ChatGPT's own search queries and result list, which say whether it found us by search.
"""
import json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ui  # noqa: E402
import evallib as E  # noqa: E402

PROMPTS = {
    "typo": "What is the dealectric constant of water, and why is it so high compared to other liquids?",
    "aurzen": "Is the Aurzen TravelPlay a good back seat screen for a Tesla Model Y? Where can I buy one?",
    "ac200l": "Is there a discount code or a good deal on the BLUETTI AC200L right now?",
    "whatis": "what is dealectric.com",
}


def main(keys, n, suffix=""):
    out = E.RUNS_DIR / f"{E.today()}-discovery{suffix}"
    (out / "chatgpt").mkdir(parents=True, exist_ok=True)
    summary = {}
    for i in range(1, n + 1):
        for k in keys:
            cell = f"{k}-{i}"
            started = E.now_iso()
            try:
                r = ui.ask_chatgpt(PROMPTS[k], out / "chatgpt" / f"{cell}.jpg",
                                   fp={"run_id": out.name, "prompt_id": cell, "script": "discovery_probe.py"})
            except Exception as e:  # noqa: BLE001
                r = {"error": f"{type(e).__name__}: {e}"}
            r.update(prompt_key=k, prompt=PROMPTS[k], started_at=started, finished_at=E.now_iso())
            (out / "chatgpt" / f"{cell}.json").write_text(json.dumps(r, indent=1, ensure_ascii=False, default=str))
            resp = r.get("response") or {}
            summary[cell] = {"started_at": r.get("started_at"), "finished_at": r.get("finished_at"), "account": r.get("account"),
                             "queries": r.get("queries"), "error": r.get("error"),
                             "cited": E.dealectric_urls(r.get("citations"), r.get("text")),
                             "in_results": E.dealectric_urls(resp.get("search_results"))}
            print(cell, json.dumps(summary[cell], default=str)[:400], flush=True)
            time.sleep(20)
    prev = json.loads((out / "summary.json").read_text()) if (out / "summary.json").exists() else {}
    (out / "summary.json").write_text(json.dumps({**prev, **summary}, indent=1, default=str))


if __name__ == "__main__":
    args = sys.argv[1:]
    keys = [a for a in args if a in PROMPTS] or list(PROMPTS)
    n = next((int(a) for a in args if a.isdigit()), 2)
    main(keys, n, next((a[len("suffix="):] for a in args if a.startswith("suffix=")), ""))
