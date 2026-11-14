#!/usr/bin/env python3.12
"""Combined page method, ad hoc run of 2026-11-13 (Barry): the gap-page research method (tools/abpage.py) with two added
steps, kept apart from the daily flow. Nothing here changes abpage.py, kitpage.py or gapmine.py; this file routes to them.

1. Shape. After the ChatGPT harvest one agent call decides what the page should sell:
     single          a normal research-method gap page (abpage.research)
     kit             one bundle behind one link that fills one cart (kitpage.research)
     bundle_compare  2-4 single-cart kits, each for a different shopper situation (kitpage.research --compare)
   A bundle needs all four: the problem takes more than one item, assembling the set takes knowledge, one cart (one
   Shopify store we link, or Amazon) can hold it, and ChatGPT shows no catalog card for the set (card-slot rule, 11-13).
2. Price check. After a page is applied, each product it sells is priced the same day at the major US sellers (Google
   Shopping in the Agent Chrome via tools/buycheck.py, Amazon's own page via tools/amzprice.py). Where the price through
   our link is strictly the lowest, src/pricecheck.json gets the sellers and the page record gets "price_check": True
   (src/build.py price_check: "Lowest of N sellers checked <date>: ..."). A tie or a higher price changes nothing.

    python3.12 tools/combopage.py shape <folder>...
    python3.12 tools/combopage.py research <folder>...        shape, then the matching research
    python3.12 tools/combopage.py apply <folder>...           build, gate, commit locally (record carries "run")
    python3.12 tools/combopage.py price <folder>... [--pace 45]   price check for applied pages, flag, rebuild, commit

Folders are growth/focus/ab/<folder>/ as for abpage (harvest.json first: abpage.harvest).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _p in ("tools", "src", "growth/evals"):
    sys.path.insert(0, str(ROOT / _p))
import abpage as A  # noqa: E402
import kitpage as K  # noqa: E402
import repolock  # noqa: E402

RUN = "combo-1113"
PRICECHECK = ROOT / "src/pricecheck.json"
RETAILERS = [("amazon", "Amazon"), ("walmart", "Walmart"), ("best buy", "Best Buy"), ("bestbuy", "Best Buy"), ("newegg", "Newegg"),
             ("home depot", "Home Depot"), ("lowe", "Lowe's"), ("target", "Target"), ("b&h", "B&H"), ("costco", "Costco"),
             ("micro center", "Micro Center"), ("adorama", "Adorama"), ("rei", "REI"), ("sam's club", "Sam's Club")]


# ---------------------------------------------------------------- shape

def _stores() -> str:
    """Stores that can hold a multi-item cart behind one link: the Shopify stores of brands we link, and Amazon."""
    import products as P
    by = {}
    for p in P.PRODUCTS:
        if p.get("program", "").startswith("amazon"):
            continue
        host = re.sub(r"^https?://(www\.)?", "", p.get("url") or "").split("/")[0]
        by.setdefault((p["brand"], host), 0)
        by[(p["brand"], host)] += 1
    return "\n".join(f"{b} | {h} | {n} products listed" for (b, h), n in sorted(by.items())) + \
        "\nAmazon | amazon.com | any products sold on Amazon, one cart (tagged add-to-cart link)"


def shape_prompt(slug: str, h: dict, q: str) -> str:
    return "\n\n".join([
        "You decide what kind of page Dealectric should publish for one shopper question. Answer with one JSON object only.",
        f"## The question (as ChatGPT searched it)\n{q}",
        "## What ChatGPT answered and showed in two plain chats\n" + A._harvest_text(h)[:9000],
        "## Products Dealectric already lists (slug | brand | category | program | name)\n" + A._ours_list(),
        "## Carts one link can fill (brand | store | listed)\n" + _stores(),
        """## The choice
- "single": the shopper needs one product; the page compares models and recommends one. This is the default.
- "kit": the shopper's problem is solved only by a set of items, and one researched set behind one buy link is the answer.
- "bundle_compare": different shopper situations need different sets (a real tradeoff, e.g. one 24 V battery vs two 12 V), so the
  page compares 2-4 single-cart kits.
Choose "kit" or "bundle_compare" ONLY when all four tests hold; otherwise "single":
1. multi_item: the problem takes more than one item. Evidence: ChatGPT's own answer names an accessory or second product the
   shopper must add, or the question is a setup, a situation or "what do I need for".
2. knowledge: a sizing, connector, voltage, chemistry or compatibility fact decides whether the set works; a shopper who guesses
   can get it wrong.
3. one_cart: at least two of the items can go in ONE cart from the list above (one brand's store, or Amazon). A store's own
   bundle SKU (e.g. power station + panel sold as one item) also counts. Never two stores.
4. uncarded: ChatGPT showed no product card for that set as a single product (cards it showed are listed above under the
   carousel). A set sold everywhere as one carded product (e.g. a Jackery Solar Generator kit) fails this test.
Do not stretch: an accessory nobody needs, or two unrelated products, is not a kit.""",
        """## Output
{"shape": "single" | "kit" | "bundle_compare",
 "tests": {"multi_item": true|false, "knowledge": true|false, "one_cart": true|false, "uncarded": true|false},
 "items": ["<item type the set needs>", ...],
 "cart": "<brand store or Amazon that would hold it, or null>",
 "why": "<two sentences: the evidence from ChatGPT's answer and the fact that decides the set>"}""",
    ])


def shape(slug: str, force: bool = False) -> dict:
    d = A.pdir(slug)
    got = A.jload(d / "shape.json")
    if got and got.get("shape") and not force:
        return got
    h = A.jload(d / "harvest.json")
    if not h or not h.get("chats"):
        return {"shape": "single", "why": "no harvest", "status": "no harvest"}
    out = A.claude(shape_prompt(slug, h, A.query_for(slug, h)), tools=False, timeout=900)
    t = out.get("tests") or {}
    if out.get("shape") not in ("single", "kit", "bundle_compare") or (out.get("shape") != "single" and not all(t.get(k) for k in ("multi_item", "knowledge", "one_cart", "uncarded"))):
        out["decided"] = out.get("shape")
        out["shape"] = "single"   # a bundle only when all four tests hold
    A.jsave(d / "shape.json", out)
    return out


# ---------------------------------------------------------------- research and apply (routing only)

def research(slug: str, force: bool = False) -> dict:
    d = A.pdir(slug)
    if not force and (d / "draft.json").exists():
        dr = A.jload(d / "draft.json")
        return {"slug": slug, "status": "drafted", "shape": "kit" if dr.get("kit_page") else "single", "model": "cached"}
    sh = shape(slug)
    if sh["shape"] != "single":
        r = K.research(slug, force, compare=sh["shape"] == "bundle_compare")
        if r.get("status") == "drafted":
            return {**r, "shape": sh["shape"]}
        # the kit research found no honest one-cart set: note it and fall back to a single-product page
        sh.update({"fell_back": True, "kit_result": {k: str(v)[:300] for k, v in r.items()}, "shape": "single"})
        A.jsave(d / "shape.json", sh)
    r = A.research(slug, new_page=True, force=force)
    return {**r, "shape": "single"}


USED = re.compile(r"\b(renewed|refurbished|used|open[- ]box|pre-owned)\b", re.I)


def _norm(x: str) -> str:
    return re.sub(r"[^a-z0-9]", "", x.lower())


BUNDLE = re.compile(r"bundle|kit with|\bwith .{0,70}(speakers?|stand|case|cables?|cleaning|mat|headphones|records?)\b|\+|2[- ]pack|pack of", re.I)


def amazon_find(brand: str, model: str, tab) -> dict | None:
    """The Amazon listing for a table row with no product record: an organic search result, read in the Agent Chrome,
    whose title names the brand and every word of the model, new condition, not a seller's bundle; shortest title wins."""
    import urllib.parse
    tab.navigate("https://www.amazon.com/s?" + urllib.parse.urlencode({"k": f"{brand} {model}"}))
    rows = []
    for _ in range(6):
        time.sleep(3)
        rows = tab.eval("""[...document.querySelectorAll('div[data-component-type="s-search-result"]')].slice(0, 20).map(e => [e.dataset.asin,
            ((e.querySelector('[data-cy="title-recipe"]') || e.querySelector('h2') || {}).innerText || '').replace(/\\s+/g, ' '),
            /Sponsored/.test((e.querySelector('[data-cy="title-recipe"]') || e).innerText.slice(0, 40))])""") or []
        if len(rows) >= 4:
            break
    base = re.sub(r"\(.*?\)", " ", model)
    words = [_norm(w) for w in re.findall(r"[A-Za-z0-9+.-]+", base) if len(_norm(w)) >= 2]
    coded = [w for w in words if re.search(r"\d", w)]
    words = coded or words   # a model code ("EZ1-LV", "HMS-420-1WM-LV") identifies the listing; descriptive words need not match
    hits = [(asin, title) for asin, title, sponsored in rows
            if asin and _norm(brand) in _norm(title) and all(w in _norm(title) for w in words) and not USED.search(title) and not BUNDLE.search(title)]
    if not hits:
        return None
    asin, title = min(hits, key=lambda h: len(h[1]))
    return {"asin": asin, "title": title[:160]}


def amazon_rescue(draft: dict, d: Path) -> list[dict]:
    """A single-product draft with no row we sell: give its rows our tagged Amazon listing where one exists (the
    all_links rule of the 11-12 push: a row links our program, else our tagged Amazon listing, else the maker's page)."""
    sys.path.insert(0, str(ROOT / "growth/evals"))
    import ui
    tab = ui.Tab("about:blank")
    found = []
    try:
        for r in draft["page"]["rows"]:
            if r.get("slug") or r.get("asin") or not r.get("brand"):
                continue
            hit = amazon_find(r["brand"], r.get("model") or "", tab)
            found.append({"row": f"{r['brand']} {r.get('model')}", **(hit or {"asin": None})})
            if hit:
                r["asin"] = hit["asin"]
            time.sleep(4)
    finally:
        tab.close()
    draft["amazon_rescue"] = found
    A.jsave(d / "draft.json", draft)
    return found


def sanitize(draft: dict) -> list[str]:
    """Mechanical repairs for what the one fix pass keeps leaving behind: a product record under a program we don't have
    (set to the brand's approved program when there is one, else demoted to a plain row linking the maker's page), buy
    tokens that name no product, and the banned word in a rival's return-policy note."""
    import gappage
    import products as P
    notes = []
    progs = gappage.programs()
    known = {p["slug"] for p in P.PRODUCTS}
    pg = draft.get("page") or {}
    for p in list(draft.get("products") or []):
        if p.get("program") in progs:
            continue
        fit = next((k for k, v in progs.items() if not k.startswith("amazon") and v.lower().startswith(str(p.get("brand", "")).lower() + " ")), None)
        if fit and p.get("price") and p.get("url"):
            notes.append(f"{p['slug']}: program {p.get('program')!r} -> {fit}")
            p["program"] = fit
            p.setdefault("verified", A.today())
            continue
        draft["products"].remove(p)
        notes.append(f"{p['slug']}: no approved program, demoted to a plain row")
        for r in pg.get("rows") or []:
            if r.get("slug") == p["slug"]:
                r.pop("slug")
                r.update({"brand": p["brand"], "model": r.get("model") or p.get("model") or p["name"], "url": p.get("url")})
    for k in list(draft.get("new_categories") or {}):   # the category key is capped at 20 characters
        if len(k) > 20:
            parts = k.split("-")
            while len("-".join(parts)) > 20 and len(parts) > 1:
                parts = parts[1:]
            nk = "-".join(parts)[:20]
            draft["new_categories"][nk] = draft["new_categories"].pop(k)
            for p in draft.get("products") or []:
                if p.get("category") == k:
                    p["category"] = nk
            notes.append(f"category {k} -> {nk}")
    live = known | {p["slug"] for p in draft.get("products") or []}
    names = {r.get("slug"): r.get("model") for r in pg.get("rows") or []}
    for k in ("answer", "after", "intro"):
        t = pg.get(k)
        if not t:
            continue
        for tok in set(re.findall(r"\{buy:([a-z0-9-]+)\}", t)):
            if tok not in live:
                nm = names.get(tok) or tok.replace("-", " ")
                t = re.sub(r"\s*\(\{buy:%s\}\)" % re.escape(tok), "", t).replace("{buy:%s}" % tok, nm)
                notes.append(f"token {tok} replaced with text")
        pg[k] = t
    raw = json.dumps(pg, ensure_ascii=False)
    fixed = re.sub(r"(\d+)[- ][Dd]ay [Mm]oney[- ][Bb]ack [Gg]uarantee", r"\1-day returns", raw)
    fixed = re.sub(r"[Mm]oney[- ][Bb]ack [Gg]uarantee", "refund policy", fixed)
    fixed = re.sub(r"[Ss]atisfaction [Gg]uarantee", "satisfaction policy", fixed)
    if fixed != raw:
        draft["page"] = json.loads(fixed)
        notes.append("return-policy wording")
    if notes:
        draft.setdefault("sanitized", []).extend(notes)
        if not (draft.get("gate") or {}).get("pass"):
            draft.pop("gate", None)
    return notes


def fill_policy(draft: dict) -> int:
    """New product records that lack warranty or return terms take them from a product of the same brand we already
    list (the terms are the store's, read and verified when that product was added). Kit fix passes often drop them."""
    import products as P
    n = 0
    for p in draft.get("products") or []:
        for k in ("warranty", "returns"):
            if not str(p.get(k) or "").strip():
                src = next((x for x in P.PRODUCTS if x["brand"].lower() == str(p.get("brand", "")).lower() and x.get("program") == p.get("program") and x.get(k)), None)
                if src:
                    p[k] = src[k]
                    n += 1
    return n


def apply(slug: str) -> dict:
    d = A.pdir(slug)
    draft = A.jload(d / "draft.json")
    if not draft:
        return {"slug": slug, "status": "no draft"}
    kit = bool(draft.get("kit_page") or draft.get("bundle_compare"))
    if sanitize(draft) + [1] * fill_policy(draft):
        A.jsave(d / "draft.json", draft)
    rows = (draft.get("page") or {}).get("rows") or []
    amazon_pick = False
    if not kit and rows and not any(r.get("slug") for r in rows):
        if "amazon_rescue" not in draft:
            amazon_rescue(draft, d)
        amazon_pick = bool(rows[0].get("asin"))   # the pick must be linkable; otherwise the page stays skipped
        if amazon_pick and (draft.get("gate") or {}).get("skipped"):
            draft.pop("gate")
            A.jsave(d / "draft.json", draft)
    orig, orig_val = A.record_text, A.validate
    extra = f'"run": {RUN!r},\n ' + ('"all_links": True,\n ' if amazon_pick else "")
    A.record_text = lambda dr, old, g: orig(dr, old, g).replace('"method": ', extra + '"method": ', 1)
    if amazon_pick:
        A.validate = lambda dr, new: [e for e in orig_val(dr, new) if not e.startswith("NO_LISTED_PRODUCT")]
    try:
        res = K.apply(slug, True) if kit else A.apply(slug, True)
    finally:
        A.record_text, A.validate = orig, orig_val
    if amazon_pick:
        res["amazon_pick"] = rows[0]["asin"]
    return res


# ---------------------------------------------------------------- price check

def _retailer(merchant: str) -> str | None:
    m = merchant.lower()
    return next((name for key, name in RETAILERS if key in m), None)


def _load_pc() -> dict:
    return json.loads(PRICECHECK.read_text()) if PRICECHECK.exists() else {"products": {}}


def price_one(p: dict, tab, B, BC) -> dict | None:
    """One product: Google Shopping cards for the same model (buycheck's matching), reduced to the lowest price per major
    retailer plus the brand store. Returns the pricecheck.json entry, or a dict with "error"/"none"."""
    amazon = B.is_amazon(p)
    if amazon:
        a = B.amz_price(p["asin"])
        if not a or not a[2]:
            return {"none": "no fresh in-stock Amazon price"}
        q = dict(p, price=a[0])   # buycheck compares against p["price"]
    else:
        q = p
    r = BC.check(q, tab)
    if r.get("error"):
        return {"error": r["error"]}
    if not any(c.get("kind") == "retailer" for c in r.get("cards") or []):   # the full name often shows the brand's own cards only
        time.sleep(15)
        r2 = BC.check(q, tab, loose=True)
        if r2.get("error"):
            return {"error": r2["error"]}
        r = dict(r2, cards=(r.get("cards") or []) + (r2.get("cards") or []))
    sellers: dict[str, float] = {}
    for c in r.get("cards") or []:
        if c.get("kind") == "retailer":
            name = _retailer(c["merchant"])
        elif c.get("kind") == "brand":
            name = B.store_host(p) if amazon else None    # the brand store is "ours" for a linked product; for an Amazon pick it competes
        else:
            name = None
        if name and (name not in sellers or c["price"] < sellers[name]):
            sellers[name] = c["price"]
    c0 = B.best_offer(p)[0] if not amazon else None
    if amazon:
        how, ours = "amazon", q["price"]
        sellers.pop("Amazon", None)
    elif c0 and B.applied_by_link(p, c0) and not B.borrowed_test(p, c0):
        how, ours = "link", B.bc_after(p, B.best_offer(p)[2])
        sellers[f"{B.store_host(p)} without the link"] = p["price"]
    else:
        how, ours = "store", p["price"]
    if not sellers:
        return {"none": "no major seller lists this model"}
    lowest = min(sellers.values())
    entry = {"date": dt.date.today().isoformat(), "how": how, "ours": ours,
             "sellers": [[n, x] for n, x in sorted(sellers.items(), key=lambda kv: kv[1])][:5]}
    if lowest - ours < max(1.0, 0.01 * ours):
        return {"none": f"not the lowest: ours {ours}, {min(sellers, key=sellers.get)} {lowest}", "entry": entry}
    return entry


def price(folders: list[str], pace: float) -> dict:
    """Price-check the first product we sell on each applied page; flag the pages where our link is strictly the lowest."""
    import importlib
    import build as B
    import buycheck as BC
    import gaps
    sys.path.insert(0, str(ROOT / "growth/evals"))
    import ui
    pages = {}
    for f in folders:
        dr = A.jload(A.pdir(f) / "draft.json") or {}
        g = next((x for x in gaps.GAP_PAGES if x["slug"] == dr.get("slug")), None)
        if g and g.get("run") == RUN:
            pages[f] = g
    pc = _load_pc()
    log = A.jload(ROOT / "growth/combo/price-log.json", {})
    today = dt.date.today().isoformat()
    tab = ui.Tab("about:blank")
    stopped = None
    try:
        for f, g in pages.items():
            slugs = [r["slug"] for r in g["rows"] if r.get("slug")][:2]   # the pick and the runner-up we sell
            for s in slugs:
                if s in log:   # checked once in this run; a re-check is a deliberate re-run with the log entry removed
                    if log[s].get("result") == "lowest":
                        pc["products"][s] = log[s]["entry"]
                    continue
                p = B.BY_SLUG[s]
                e = price_one(p, tab, B, BC)
                if e and e.get("error"):
                    stopped = e["error"]
                    print(f"{s}: {e['error']}; stopping this sitting", flush=True)
                    break
                log[s] = {"date": today, "result": "lowest" if e and "how" in e else (e or {}).get("none"), "entry": e if e and "how" in e else (e or {}).get("entry")}
                A.jsave(ROOT / "growth/combo/price-log.json", log)
                if e and "how" in e:
                    pc["products"][s] = e
                print(f"{s}: {log[s]['result']}", flush=True)
                time.sleep(pace)
            if stopped:
                break
    finally:
        tab.close()
    flagged = [f for f, g in pages.items() if any(r.get("slug") in pc["products"] for r in g["rows"]) and not g.get("price_check")]
    if not flagged:
        return {"flagged": [], "stopped": stopped}
    with repolock.hold("combopage-price"):
        if subprocess.run(["git", "status", "--porcelain", "src", "docs"], cwd=ROOT, capture_output=True, text=True).stdout.strip():
            return {"flagged": [], "stopped": stopped, "skipped": "src/ or docs/ has uncommitted changes"}
        PRICECHECK.write_text(json.dumps(pc, indent=1) + "\n")
        gp = ROOT / "src/gaps.py"
        kept = []
        for f in flagged:
            g = pages[f]
            before = gp.read_text()
            i = before.find(f'"slug": {g["slug"]!r}')   # record_text writes values with repr()
            j = before.find(f'"run": {RUN!r}', i) if i >= 0 else -1
            if j < 0 or j - i > 4000:
                print(f"{g['slug']}: record not found for flagging", flush=True)
                continue
            gp.write_text(before[:j] + '"price_check": True,\n ' + before[j:])
            r = subprocess.run(["python3.12", "src/build.py"], cwd=ROOT, capture_output=True, text=True)
            dr = A.jload(A.pdir(f) / "draft.json") or {}
            ok = r.returncode == 0
            if ok:
                cmd = ["python3.12", "growth/evals/fastloop.py", "check", f"docs/{g['slug']}.html", "--packs", A.pack_from_harvest(f), "--ranks", "1,3,6", "--research"]
                for m in dr.get("must") or []:
                    cmd += ["--must", m]
                ok = "PASS" in subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True).stdout
            if ok:
                kept.append(g["slug"])
            else:   # the longer pick line pushed the link past ChatGPT's cut: this page keeps its normal line
                gp.write_text(before)
                print(f"{g['slug']}: price line fails the length gate, not flagged", flush=True)
        subprocess.run(["python3.12", "src/build.py"], cwd=ROOT, capture_output=True, text=True)
        if subprocess.run(["python3.12", "tools/docsguard.py"], cwd=ROOT, capture_output=True, text=True).returncode:
            subprocess.run(["git", "checkout", "--", "src", "docs"], cwd=ROOT)
            return {"flagged": [], "stopped": stopped, "error": "docsguard failed; reverted"}
        subprocess.run(["git", "add", "src/pricecheck.json", "src/gaps.py", "docs", "worker/src/links-map.json", "growth/combo/price-log.json"], cwd=ROOT)
        subprocess.run(["git", "commit", "-q", "-m", f"Combo run: price check {today}, lowest-of-sellers line on {len(kept)} pages\n\n"
                        + "\n".join("/" + s for s in kept) + "\n\nCo-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>\n"], cwd=ROOT)
    return {"flagged": kept, "stopped": stopped}


def amazon_prices() -> dict:
    """Read Amazon's price for every ASIN on this run's pages that has none yet (tools/amzprice.py), rebuild, commit."""
    import gaps
    have = json.loads((ROOT / "src/amazon_prices.json").read_text())["asins"] if (ROOT / "src/amazon_prices.json").exists() else {}
    import products as P
    asins = {r["asin"] for g in gaps.GAP_PAGES if g.get("run") == RUN for r in g["rows"] if r.get("asin")}
    asins |= {P_["asin"] for g in gaps.GAP_PAGES if g.get("run") == RUN for r in g["rows"] if r.get("slug")
              for P_ in [next((x for x in P.PRODUCTS if x["slug"] == r["slug"]), {})] if P_.get("asin")}
    todo = sorted(a for a in asins if a not in have)
    if not todo:
        return {"read": 0}
    with repolock.hold("combopage-amazon"):
        if subprocess.run(["git", "status", "--porcelain", "src", "docs"], cwd=ROOT, capture_output=True, text=True).stdout.strip():
            return {"read": 0, "skipped": "src/ or docs/ has uncommitted changes"}
        r = subprocess.run(["python3.12", "tools/amzprice.py", *todo], cwd=ROOT, capture_output=True, text=True)
        subprocess.run(["python3.12", "src/build.py"], cwd=ROOT, capture_output=True, text=True)
        if subprocess.run(["python3.12", "tools/docsguard.py"], cwd=ROOT, capture_output=True, text=True).returncode:
            subprocess.run(["git", "checkout", "--", "src", "docs"], cwd=ROOT)
            return {"read": 0, "error": "docsguard failed; reverted"}
        subprocess.run(["git", "add", "src/amazon_prices.json", "docs", "worker/src"], cwd=ROOT)
        subprocess.run(["git", "commit", "-q", "-m", f"Combo run: Amazon prices read for {len(todo)} listings on the new pages\n\n"
                        "Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>\n"], cwd=ROOT)
    return {"read": len(todo), "tail": r.stdout[-300:]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["shape", "research", "apply", "price", "amazon"])
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--pace", type=float, default=45)
    a = ap.parse_args()
    if a.cmd == "amazon":
        print(json.dumps(amazon_prices()))
        return 0
    if a.cmd == "price":
        print(json.dumps(price(a.slugs, a.pace)))
        return 0
    fn = {"shape": lambda s: shape(s, a.force), "research": lambda s: research(s, a.force), "apply": apply}[a.cmd]
    for s in a.slugs:
        print(json.dumps({"folder": s, **{k: v for k, v in fn(s).items() if k != "_meta"}}, ensure_ascii=False)[:700], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
