#!/usr/bin/env python3.12
"""How thin is a search query on the engines behind the assistants? Opens the query on Bing (feeds ChatGPT search) and
Brave (feeds Claude's web search) in the agent's Chrome, in background tabs, and records the organic results (rank,
title, URL, domain) for each. DLC-51: picks the queries worth a comparison page (few pages whose title answers the
query) and later shows whether a built page ranks for its query.

    python3.12 growth/evals/serp.py --queries "Qi2.2 25W power bank certified list" "portable power station UPS switchover time 10ms"
    python3.12 growth/evals/serp.py --from-run 2026-10-23-queryprobe        # every ChatGPT query recorded in that run
    python3.12 growth/evals/serp.py --from-run 2026-10-23-queryprobe --out growth/evals/runs/2026-10-23-queryprobe/serp.json

Writes one JSON: {query: {"bing": [{rank, title, url, domain}], "brave": [...], "dealectric_rank": {bing, brave}}}.
A query already in the file is fetched again only on the engines that returned nothing, so a re-run fills the gaps.

Brave: after about ten queries in a row Brave serves a "Verifying you're not a bot" check instead of results, and it is
still there an hour later even at one query per 8 s; we do not solve it. The record then holds a single row with
rank 0 and a `note` quoting the page. For the daily readings Brave is left to the Claude-as-agent run (its search is
Brave-backed) and only Bing is scraped here (`--engines bing`); ask Brave by hand, a few queries a day at most.
Start the browser first: uv --directory ~/Desktop/agent-vault run agent-vault browser
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import ui  # noqa: E402

ENGINES = {
    "bing": {"url": "https://www.bing.com/search?q={q}&setlang=en&cc=US",
             "js": r"""JSON.stringify([...document.querySelectorAll('#b_results > li.b_algo')].map(li => {
                 const h = li.querySelector('h2'); const a = h && h.querySelector('a[href]');
                 return a ? {title: (h.textContent || a.getAttribute('aria-label') || '').replace(/\s+/g, ' ').trim(), url: a.href} : null; }).filter(Boolean))"""},
    "brave": {"url": "https://search.brave.com/search?q={q}&source=web",
              "js": r"""JSON.stringify([...document.querySelectorAll('[data-type="web"]')].map(s => {
                  const a = s.querySelector('a[href^="http"]'); const t = s.querySelector('.title, .snippet-title, h3, [class*="title"]');
                  return a ? {title: (t ? t.innerText : a.innerText.split('\n').pop()).trim().slice(0, 200), url: a.href} : null; }).filter(Boolean))"""},
}
SETTLE_S = 4


def unwrap_bing(url: str) -> str:
    """Bing wraps every organic result in https://www.bing.com/ck/a?...&u=a1<urlsafe base64 of the target>...;
    returns the target, or the input when it is not such a wrapper."""
    try:
        p = urllib.parse.urlsplit(url)
        if not p.netloc.endswith("bing.com") or not p.path.startswith("/ck/"):
            return url
        u = urllib.parse.parse_qs(p.query).get("u", [""])[0]
        if u.startswith("a1"):
            u = u[2:]
        return base64.urlsafe_b64decode(u + "=" * (-len(u) % 4)).decode("utf-8", "replace") or url
    except Exception:  # noqa: BLE001
        return url


def fetch(engine: str, query: str) -> list[dict]:
    spec = ENGINES[engine]
    tab = ui.Tab("about:blank")
    try:
        tab.navigate(spec["url"].format(q=urllib.parse.quote(query, safe="")))
        time.sleep(SETTLE_S)
        rows, seen = [], set()
        for _ in range(3):
            try:
                rows = json.loads(tab.eval(spec["js"]) or "[]")
            except Exception:  # noqa: BLE001
                rows = []
            if rows:
                break
            time.sleep(2)
        if not rows:
            # Brave answers a burst of queries with an empty result list (seen 2026-10-23 after ~10 queries in a row;
            # fine again minutes later); keep what the page said so the run can tell a block from a real zero.
            try:
                note = (tab.eval("document.title") or "")[:80] + " :: " + (tab.eval("document.body.innerText.slice(0,160)") or "").replace("\n", " ")
            except Exception:  # noqa: BLE001
                note = "unreadable"
            return [{"rank": 0, "title": "", "url": "", "domain": "", "note": f"no results parsed; page: {note}"}]
        out = []
        for r in rows:
            u = E.strip_tracking(unwrap_bing(r["url"]) if engine == "bing" else r["url"])
            host = urllib.parse.urlsplit(u).netloc
            if u in seen or not u.startswith("http") or host.endswith(("bing.com", "brave.com")):   # image cards, engine pages
                continue
            seen.add(u)
            out.append({"rank": len(out) + 1, "title": r["title"], "url": u, "domain": urllib.parse.urlsplit(u).netloc.removeprefix("www.")})
        return out
    finally:
        tab.close()


def queries_from_run(run_id: str) -> list[str]:
    qs: dict[str, None] = {}
    for f in sorted((E.run_dir(run_id) / "chatgpt").glob("*.json")):
        for q in json.load(open(f)).get("queries") or []:
            qs.setdefault(q)
    return list(qs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--queries", nargs="*", default=[])
    ap.add_argument("--queries-file", default=None, help="one query per line")
    ap.add_argument("--from-run", default=None)
    ap.add_argument("--engines", default="bing,brave")
    ap.add_argument("--out", default=None)
    ap.add_argument("--pause", type=float, default=3.0)
    a = ap.parse_args()
    if not ui.browser_ok():
        sys.exit("agent Chrome not reachable on localhost:9222")
    queries = list(a.queries) + (queries_from_run(a.from_run) if a.from_run else [])
    if a.queries_file:
        queries += [l.strip() for l in open(a.queries_file) if l.strip() and not l.startswith("#")]
    queries = list(dict.fromkeys(queries))
    if not queries:
        sys.exit("no queries")
    out_path = Path(a.out) if a.out else (E.run_dir(a.from_run) / "serp.json" if a.from_run else None)
    result = json.load(open(out_path)) if out_path and out_path.exists() else {}
    engines = a.engines.split(",")
    for i, q in enumerate(queries, 1):
        # A query already in the output file is fetched again only on the engines that gave no real results (a block
        # or an empty page), so a re-run repairs the gaps without repeating the rest.
        row = result.get(q, {})
        todo = [e for e in engines if not any(r.get("rank") for r in row.get(e) or [])]
        if not todo:
            continue
        for eng in todo:
            row[eng] = fetch(eng, q)
            time.sleep(a.pause)
        row["dealectric_rank"] = {eng: next((r["rank"] for r in row[eng] if r["domain"].endswith("dealectric.com")), None) for eng in row if eng != "dealectric_rank"}
        result[q] = row
        print(f"[{i}/{len(queries)}] {q!r}: " + ", ".join(f"{e} {sum(1 for r in row[e] if r.get('rank'))}" for e in row if e != "dealectric_rank")
              + f"; dealectric {row['dealectric_rank']}")
        if out_path:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            E.write_json(out_path, result)
    if not out_path:
        print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
