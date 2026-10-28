#!/usr/bin/env python3.12
"""DLC-55 step 3: ChatGPT asked the shopper question behind each strict-rule opening, n = 2, plus the saturated control
(wireless earbuds). Same driver as growth/evals/ui.py (agent Chrome, signed in, temporary chat, web search on). Per chat:
ChatGPT's own search queries, the result and cited domains, and how many of them are major publishers.

    python3.12 growth/evals/runs/2026-10-24-voidscan/assistant/chatgpt_check.py
"""
import json
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))   # growth/evals
import ui  # noqa: E402

PROMPTS = {
    "chair": "I need a desk chair for my home office. Which one should I buy?",
    "fit": "What are the best Fitbit watches for women?",
    "vls": "What's the best vertical laptop stand?",
    "ext": "I want an extra screen for my laptop. What should I buy?",
    "ear": "What are the best wireless earbuds right now?",   # control: saturated by major publishers
}
MAJORS = ("nytimes.com", "rtings.com", "consumerreports.org", "cnet.com", "tomsguide.com", "techradar.com", "pcmag.com",
          "theverge.com", "engadget.com", "wired.com", "zdnet.com", "soundguys.com", "whathifi.com", "reviewed.com",
          "usatoday.com", "gearlab.com", "outdoorgearlab.com", "techgearlab.com", "bestbuy.com/site/misc", "tomshardware.com",
          "businessinsider.com", "forbes.com", "cnn.com", "nbcnews.com", "goodhousekeeping.com", "popularmechanics.com")


def dom(u):
    return urlsplit(u).netloc.lower().removeprefix("www.")


def main():
    summary = {}
    for k, prompt in PROMPTS.items():
        for n in (1, 2):
            r = ui.ask_chatgpt(prompt, HERE / f"chatgpt-{k}-{n}.jpg")
            found = r.get("search_results") or (r.get("response") or {}).get("search_results") or []
            res = [x.get("url", "") for x in found if x.get("url")]
            cited = [c["url"] for c in r.get("citations") or []]
            row = {"prompt": prompt, "account": r.get("account"), "queries": r.get("queries"),
                   "result_domains": sorted({dom(u) for u in res}), "cited_domains": sorted({dom(u) for u in cited}),
                   "majors_in_results": sorted({dom(u) for u in res if any(m in u for m in MAJORS)}),
                   "majors_cited": sorted({dom(u) for u in cited if any(m in u for m in MAJORS)}),
                   "answer": (r.get("text") or "")[:1500]}
            (HERE / f"chatgpt-{k}-{n}.json").write_text(json.dumps(row, indent=1, ensure_ascii=False))
            summary[f"{k}-{n}"] = {x: row[x] for x in ("queries", "majors_in_results", "majors_cited", "cited_domains")}
            print(k, n, json.dumps(summary[f"{k}-{n}"], ensure_ascii=False)[:600], flush=True)
            time.sleep(5)
    (HERE / "chatgpt-summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
