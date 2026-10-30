#!/usr/bin/env python3.12
"""Supply test (Barry, 2026-10-30): besides our page, how much useful, buyable product help does ChatGPT find?

For each category question ChatGPT answered (solar questions vs the focus products' category questions):
1. Sources: the top six non-Dealectric pages ChatGPT was shown. Each is judged for whether it names models to buy,
   gives a price stated as current (September or October 2026, or "today"/"now"), and gives a discount code; its raw
   HTML is checked for outbound buy links (stores, marketplaces, affiliate redirects). A source is ACTIONABLE when it
   names models, has a current price and links out to buy.
2. Answers: ChatGPT's reply. A judge lists every product it recommends with the source label shown next to it
   ("Dealectric", "Trek4Tech", ...), and the buttons/links in the reply are counted by destination.

    python3.12 growth/evals/supply.py            # judge what's missing, print the summary
    python3.12 growth/evals/supply.py --report
"""
import argparse
import json
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import focusgap as F  # noqa: E402
import gapexp as G  # noqa: E402

OUT = F.ROOT / "growth" / "focus" / "supply"
FOCUS = ["bluetti-ac200l", "allpowers-r4000-3456wh", "allpowers-sp037-400w-solar-panel", "allpowers-p1800-1024wh",
         "allpowers-s2000-pro-sp037-solar-kit", "aurzen-travelplay-autocinema-tesla-model-y"]
CELLS = ([("solar", F.GVF / f"gap-solar--{p}-{n}.json") for p in ("best", "budget", "camping") for n in (1, 2)]
         + [("solar", f) for f in sorted(F.GVF.glob("solar-general--*-1.json"))]
         + [("focus", F.GVF / f"focus-{p}--category-{n}.json") for p in ("p1800", "sp037", "r4000", "ac200l") for n in (1, 2)]
         + [("focus", F.W1 / f"{s}--best-1.json") for s in FOCUS]
         + [(f.stem.split("--")[0], f) for f in F.VOID_CELLS])

BUY = re.compile(r"href=[\"'](https?://[^\"']+)", re.I)
STORE = re.compile(r"amazon\.|amzn\.to|walmart\.|bestbuy\.|homedepot\.|lowes\.|costco\.|target\.com|ebay\.|"
                   r"ecoflow\.com|jackery\.com|bluettipower\.com|ankersolix\.com|iallpowers\.com|goalzero\.com|renogy\.com|"
                   r"dji\.com|pecron|oukitel|vtoman|aurzen\.com|tesla\.com|"
                   r"awin1\.com|tkqlhce|anrdoezrs|jdoqocy|dpbolvw|kqzyfj|shareasale|sjv\.io|pxf\.io|go\.skimresources|"
                   r"howl\.me|linksynergy|avantlink|/go/|/out/|/recommends/", re.I)

SRC_SCHEMA = {"type": "object", "properties": {"sources": {"type": "array", "items": {"type": "object", "properties": {
    "n": {"type": "integer"}, "names_models": {"type": "boolean"}, "current_price": {"type": "boolean"},
    "code": {"type": "boolean"}, "why": {"type": "string"}}, "required": ["n", "names_models", "current_price", "code", "why"]}}},
    "required": ["sources"]}
SRC_SYSTEM = """Today is 2026-10-30. For each numbered web page a shopper might read, say:
- names_models: it recommends specific products by model name that a shopper could go and buy.
- current_price: it gives a price for at least one named model and presents it as current: dated September or
  October 2026, or worded as today's/now/current price. An undated list price or an old review price is false.
- code: it gives a discount or coupon code for at least one named model.
- why: one short phrase.
Return one entry per page number."""

ANS_SCHEMA = {"type": "object", "properties": {"products": {"type": "array", "items": {"type": "object", "properties": {
    "product": {"type": "string"}, "price_shown": {"type": "boolean"}, "source": {"type": "string"}},
    "required": ["product", "price_shown", "source"]}}}, "required": ["products"]}
ANS_SYSTEM = """You read a ChatGPT shopping answer as plain text. Source labels appear as a site name on its own
line next to a claim (for example "Dealectric", "Trek4Tech", "ALLPOWERS US"), sometimes followed by "+1".
List every product the answer recommends or presents as an option to buy (not products only mentioned in passing).
For each: product (short name), price_shown (the answer shows a price for it), source (the label shown with that
product's price or recommendation; "none" if no label). Return them in the order they appear."""


def raw_html(url: str) -> str:
    try:
        import ssl, certifi
        req = urllib.request.Request(url, headers={"User-Agent": G.UA, "Accept-Language": "en-US,en"})
        ctx = ssl.create_default_context(cafile=certifi.where())
        raw = urllib.request.urlopen(req, timeout=20, context=ctx).read(3_000_000).decode("utf-8", "ignore")
        if len(raw) > 5000:
            return raw
    except Exception:  # noqa: BLE001
        pass
    try:   # bot-walled pages: the agent's Chrome, as gapexp.fetch_text does
        import time, ui
        tab = ui.Tab("about:blank")
        try:
            tab.navigate(url)
            time.sleep(6)
            return tab.eval("document.documentElement.outerHTML") or ""
        finally:
            tab.close()
    except Exception:  # noqa: BLE001
        return ""


def raw_links(url: str) -> int:
    raw = raw_html(url)
    if not raw:
        return -1
    host = E.host_of(url)
    return sum(1 for u in BUY.findall(raw) if STORE.search(u) and E.host_of(u) != host)


def judge_sources(p: dict) -> list[dict]:
    user = f"QUESTION: {p['question']}\n\n" + "\n\n".join(
        f"[{i}] {s['title']} | {s['url']}\n{G.cut(s['text'], 700)}" for i, s in enumerate(p["sources"], 1))
    r = E.claude_cli_json(SRC_SYSTEM, user, G.JUDGE, SRC_SCHEMA, timeout=300) or {}
    srcs = {s["n"]: s for s in r.get("sources") or []}
    out = []
    for i, s in enumerate(p["sources"], 1):
        j = srcs.get(i, {})
        links = raw_links(s["url"])
        out.append({"url": s["url"], "domain": s["domain"], "names_models": bool(j.get("names_models")),
                    "current_price": bool(j.get("current_price")), "code": bool(j.get("code")), "buy_links": links,
                    "actionable": bool(j.get("names_models") and j.get("current_price") and links > 0), "why": j.get("why", "")})
    return out


def judge_answer(d: dict) -> dict:
    r = E.claude_cli_json(ANS_SYSTEM, d["text"][:12000], G.JUDGE, ANS_SCHEMA, timeout=300) or {}
    buttons = Counter()
    for c in d.get("citations") or []:
        if c.get("source") != "ui_href":
            continue
        u = c["url"]
        buttons["dealectric /go/" if "dealectric.com/go/" in u else "dealectric page" if "dealectric.com" in u
                else "store" if STORE.search(u) else E.host_of(u)] += 1
    return {"products": r.get("products") or [], "buttons": dict(buttons)}


def summary(res: dict) -> None:
    for group in dict.fromkeys(v["group"] for v in res.values()):
        rows = [v for v in res.values() if v["group"] == group]
        if not rows:
            continue
        n = len(rows)
        act = [sum(s["actionable"] for s in v["sources"]) for v in rows]
        price = [sum(s["current_price"] for s in v["sources"]) for v in rows]
        code = [sum(s["code"] for s in v["sources"]) for v in rows]
        prods = [p for v in rows for p in v["answer"]["products"]]
        ours = sum(1 for p in prods if "dealectric" in p["source"].lower())
        retrieved = sum(1 for v in rows if v["dealectric_in_results"])
        print(f"\n## {group}: {n} answers, our page in ChatGPT's results {retrieved}/{n}")
        print(f"- other sources per result set (of up to 6): actionable {sum(act)/n:.1f}, current price {sum(price)/n:.1f}, "
              f"code {sum(code)/n:.1f}; result sets with no actionable source: {sum(1 for a in act if a == 0)}/{n}")
        print(f"- products recommended: {len(prods)} ({len(prods)/n:.1f} per answer), with a price shown "
              f"{sum(p['price_shown'] for p in prods)}, sourced to Dealectric {ours}")
        b = Counter()
        for v in rows:
            b.update(v["answer"]["buttons"])
        print(f"- buttons/links in the answers: {dict(b)}")
        print("| cell | our rank | actionable others | other domains with a current price | products (source) |")
        print("|---|---|---|---|---|")
        for k, v in res.items():
            if v["group"] != group:
                continue
            dom = ", ".join(s["domain"] for s in v["sources"] if s["current_price"]) or "-"
            pr = "; ".join(f"{p['product']} ({p['source']})" for p in v["answer"]["products"])
            print(f"| {k} | {v['our_rank']} | {sum(s['actionable'] for s in v['sources'])}/{len(v['sources'])} | {dom} | {pr} |")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    rf = OUT / "results.json"
    res = json.loads(rf.read_text()) if rf.exists() else {}
    pf = F.OUT / "packs.json"
    packs = json.loads(pf.read_text()) if pf.exists() else {}
    if not args.report:
        for group, f in CELLS:
            k = f.stem
            if k in res or not f.exists():
                continue
            if k not in packs:
                packs[k] = F.pack(f)
                pf.write_text(json.dumps(packs, indent=1))
            d = json.loads(f.read_text())
            sr = (d.get("response") or {}).get("search_results") or []
            rank = next((i for i, r in enumerate(sr, 1) if "dealectric.com" in (r.get("domain") or r.get("url") or "")), None)
            res[k] = {"group": group, "question": d["prompt"], "query": (d.get("queries") or [""])[0], "our_rank": rank,
                      "dealectric_in_results": rank is not None, "sources": judge_sources(packs[k]), "answer": judge_answer(d)}
            rf.write_text(json.dumps(res, indent=1))
            print(f"{k}: done", flush=True)
    summary(res)


if __name__ == "__main__":
    main()
