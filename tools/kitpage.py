#!/usr/bin/env python3.12
"""Kit pages (DLC-223, Barry 2026-11-10): the research method of tools/abpage.py, aimed at "what do I need for X"
questions whose answer is a bundle, sold behind one link that opens a filled cart (src/kits.py, tools/kitcheck.py).

Barry: the kit is worth handing over only when picking the set takes real knowledge. So the five research angles are
about what makes a set work (sizing, compatibility, traps), what our stores can put in one cart, and what the shopper
would otherwise assemble; the composer picks the one fact no result ChatGPT got states and builds the page and the kit
around it. Research runs on abpage.MODELS (Opus 5.5 high).

    python3.12 tools/kitpage.py harvest <slug>... --runs <run id>
    python3.12 tools/kitpage.py research <slug>...
    python3.12 tools/kitpage.py apply <slug>... [--local]   kit -> src/kits.py, cart test, page -> src/gaps.py, build, gate
Files per page: growth/focus/ab/<slug>/ (harvest.json, angle-K*.json, compose.json, verify.json, draft.json).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "src"), str(ROOT / "growth/evals")]
import abpage as A  # noqa: E402

KIT_ANGLES = {
    "K1": ("Sizing", "The numbers that decide each item of the kit for this need: watt-hours against the actual load and "
           "hours, panel watts against refill time, storage against retention, wattage against a circuit or port limit. "
           "Each figure from the maker's spec or a named measurement, with the one-line arithmetic."),
    "K2": ("Compatibility", "Exact pairings between the kit's items: connectors, voltages, protocols, firmware, mounts, "
           "generations, input windows. Which model works with which, from the makers' own documents, and the "
           "exclusions they state. This is where a wrong set fails."),
    "K3": ("Traps", "The combinations shoppers get wrong for this need and what happens (it won't charge, it trips, it "
           "voids the warranty, it is unsafe, it needs an adapter nobody mentions), each from a maker document, a named "
           "reviewer, or a forum thread with the date and how many people report it."),
    "K4": ("Carts", "Which approved stores (list below) can put two or more of the kit's items in ONE cart: the brand's "
           "own US store (same Shopify store) or Amazon. For each candidate cart: the products with their store URL, "
           "today's price, whether the brand already sells the same combination as a bundle SKU (and its price: if it "
           "is cheaper than the items bought separately, that bundle SKU is the item to use) and any free gift. Use "
           "storecheck.py for Shopify stores."),
    "K5": ("What else is out there", "The kits and product sets the shopper would otherwise assemble: what ChatGPT's "
           "answer recommended, what the cited rival pages list, the big brands' own bundles, each priced today from the "
           "maker or the retailer shown, and where each set falls short for this need."),
}


def kit_angle_prompt(slug: str, letter: str, h: dict, query: str) -> str:
    name, what = KIT_ANGLES[letter]
    return "\n\n".join([
        A.COMMON_RULES.replace("TOOLS", str(ROOT / "tools")),
        f"## Your job: research ONE angle, \"{letter}. {name}\", for the shopper question below\n{what}",
        "The shopper needs a SET of products that work together. The page this feeds will recommend one kit, sold as one "
        "link that fills one store's cart, and it must hold one fact about making the set work that none of the results "
        "ChatGPT got already states. Read the cited rival pages (and the top results) first, then research your angle, "
        "then judge how much your best finding would stand out against those pages.",
        f"## Today\n{A.today()}",
        f"## The shopper question\n{query}",
        "## What ChatGPT did with it (saved app chats)\n" + A._harvest_text(h),
        "## Approved programs (a kit's cart must be one of these stores, or Amazon)\n" + A._programs(),
        "## Products Dealectric already lists (slug | brand | category | program | name)\n" + A._ours_list(),
        """## Output JSON
{"angle": "%s",
 "gap": "<one sentence: 'No result ChatGPT got states <X>.' X is your angle's best finding>",
 "standout": <0-3: 0 = a cited rival already has it, 1 = rivals have part of it, 2 = new and useful, 3 = new and it decides the set>,
 "standout_why": "<which rival pages you compared against and what they lack>",
 "kit_items": ["<item type>: <brand model that fits, and why>", ...],
 "carts": [{"store": "<brand store or Amazon>", "items": ["<brand model> | <url> | <price today> | <date>"], "bundle_sku": "<the store's own bundle of these, with price, or none>"}],
 "findings": [{"product": "<brand model or 'general'>", "label": "<what>", "value": "<value with unit>", "source": "<url>", "source_title": "<title>", "read": "YYYY-MM-DD", "note": "<method, conditions, arithmetic>"}],
 "unsourced": ["<what you looked for and could not source>"]}""" % letter,
    ])


def kit_compose_prompt(slug: str, h: dict, query: str, angles: dict) -> str:
    base = A.compose_prompt(slug, h, query, angles, True)
    base = base.replace("Six research agents each researched one angle", "Five research agents each researched one angle "
                        "of making the set work (K1 sizing, K2 compatibility, K3 traps, K4 carts, K5 what else is out there)")
    base = base.replace("Angle F (category, priced) is not\nchosen as the angle; its rows and prices go in every page's table.",
                        "K4 and K5 are not chosen as the angle; they supply the kit and the table.")
    kit = """
## This page sells a KIT (DLC-223)
The answer to this question is a set of products. Build ONE kit: 2-5 items that together answer the need, every item
from ONE cart: the same approved brand's own US store (all items with that brand's program), or all items on Amazon
(program amazon:us, any brands). Never mix stores in one kit. Use products we already list where they fit; add product
records (in "products") for the others, each from the maker's page, with the store URL of the exact item. A kit item is
only in the kit because the need requires it: no padding. If the store sells the exact combination as its own bundle SKU
for less than the items, use that bundle SKU as one item and say so. If no single cart can hold 2+ items that honestly
fit, return status "skip" with the reason.
- kit: {"slug": "kit-<short need words>", "name": "<what the kit is for, 2-5 words, e.g. 'CPAP camping kit'>",
  "items": [{"slug": "<product slug>", "qty": 1, "option": "<variant words if the product page has options, e.g. '1 Set' or 'Black', else ''>",
  "role": "<the job this item does in the kit, with the deciding figure>"}]}
- The page's rows are the kit's items first (each its own row with the item's role in a column), then the alternatives
  the shopper would consider (other kits or the parts a rival recommends), so the table shows why this set works.
- answer: names the kit's items and carries the one fact that makes the set work (the angle's finding). The renderer puts
  the kit's single buy link, with what it costs through the link, under the H1; put {kit:<kit slug>} once in "after"
  where the page explains the set ("The kit: ..." line).
- "must": phrases from the answer that carry the kit and its deciding fact."""
    return base.replace("## Today", kit + "\n\n## Today", 1).replace(
        '"angle": "<A-E>"', '"angle": "<K1-K3>"').replace(
        '"products": [', '"kit": {"slug", "name", "items": [...]},\n "products": [')


def research(slug: str, force: bool = False) -> dict:
    d = A.pdir(slug)
    if not force and (d / "draft.json").exists():
        return {"slug": slug, "status": "drafted (cached)"}
    h = A.jload(d / "harvest.json")
    if not h or not h["chats"]:
        return {"slug": slug, "status": "no harvest"}
    q = A.query_for(slug, h)
    todo = [x for x in KIT_ANGLES if force or not (d / f"angle-{x}.json").exists() or A.jload(d / f"angle-{x}.json", {}).get("status") == "error"]
    with cf.ThreadPoolExecutor(max_workers=len(KIT_ANGLES)) as ex:
        for x, out in zip(todo, ex.map(lambda x: A.claude(kit_angle_prompt(slug, x, h, q)), todo)):
            A.jsave(d / f"angle-{x}.json", out)
    angles = {x: {k: v for k, v in A.jload(d / f"angle-{x}.json", {}).items() if k != "_meta"} for x in KIT_ANGLES}
    if sum(1 for a in angles.values() if a.get("findings")) < 3:
        return {"slug": slug, "status": "error", "reason": "fewer than 3 angle reports came back"}
    comp = A.jload(d / "compose.json")
    if force or not comp or comp.get("status") not in ("ok", "skip"):
        comp = A.claude(kit_compose_prompt(slug, h, q, angles))
        A.jsave(d / "compose.json", comp)
    if comp.get("status") != "ok":
        return {"slug": slug, "status": comp.get("status"), "reason": comp.get("reason")}
    ver = A.jload(d / "verify.json")
    if force or not ver or not ver.get("draft"):
        ver = A.claude(A.verify_prompt({k: v for k, v in comp.items() if k != "_meta"}))
        A.jsave(d / "verify.json", ver)
    if not ver.get("draft"):
        return {"slug": slug, "status": "error", "reason": "verifier returned no draft"}
    draft = ver["draft"]
    draft.setdefault("kit", comp.get("kit"))
    import products as P
    import gaps
    taken = {p["slug"] for p in P.PRODUCTS} | {g["slug"] for g in gaps.GAP_PAGES} | {p["slug"] for p in draft.get("products") or []}
    s2 = draft.get("slug") or ""
    if s2 in taken or not re.fullmatch(r"[a-z0-9-]{8,90}", s2):
        s2 = re.sub(r"[^a-z0-9]+", "-", (draft.get("page") or {}).get("title", "").split(":")[0].lower()).strip("-")[:80]
    draft.update({"status": "ok", "slug": s2, "new_page": True, "searched_as": h["searched_as"], "angle": comp.get("angle"),
                  "why_angle": comp.get("why_angle"), "query": q, "kit_page": True})
    A.jsave(d / "draft.json", draft)
    return {"slug": slug, "status": "drafted", "page": s2, "kit": (draft.get("kit") or {}).get("name")}


def kit_errors(draft: dict) -> list[str]:
    import products as P
    k = draft.get("kit") or {}
    errs = []
    if not re.fullmatch(r"kit-[a-z0-9-]{4,60}", k.get("slug") or ""):
        errs.append(f"kit slug {k.get('slug')!r} must look like kit-<words>")
    items = k.get("items") or []
    have = {p["slug"]: p for p in P.PRODUCTS + (draft.get("products") or [])}
    if len(items) < 2:
        errs.append("a kit needs 2+ items")
    missing = [i.get("slug") for i in items if i.get("slug") not in have]
    if missing:
        errs.append(f"kit items not among our products or the draft's new products: {missing}")
    progs = {have[i["slug"]]["program"] for i in items if i.get("slug") in have}
    hosts = {re.sub(r"^www\.", "", re.sub(r"^https?://([^/]+).*", r"\1", have[i["slug"]]["url"])) for i in items if i.get("slug") in have}
    amazon = all(p.startswith("amazon:") for p in progs)
    if not amazon and (len(progs) > 1 or len(hosts) > 1 or any(p.startswith("amazon:") for p in progs)):
        errs.append(f"kit items span more than one cart: programs {sorted(progs)}, stores {sorted(hosts)}")
    if "{kit:" + (k.get("slug") or "") + "}" not in (draft.get("page") or {}).get("after", ""):
        errs.append("the after-section must carry {kit:<kit slug>} once")
    return errs


def product_errors(draft: dict) -> list[str]:
    """gappage's checks on the draft's new product records (fields, program, category, Amazon listing), with
    amzcheck retried while Amazon walls it (11-10: 3 of 5 ASINs blocked on one pass, found on the next)."""
    import gappage, amzcheck, time
    real = amzcheck.listing
    def patient(a):
        for i in range(5):
            info = real(a)
            if info.get("found") or not info.get("blocked"):
                return info
            time.sleep(15 * (i + 1))
        return info
    amzcheck.listing = patient
    try:
        errs = gappage.validate({**draft, "status": "products_only"}) if draft.get("products") else []
    finally:
        amzcheck.listing = real
    if any("unknown category" in e for e in errs):
        import products as P
        errs.append("for an unknown category use one of these keys: " + ", ".join(P.CATEGORIES) +
                    "; or add it under the draft's top-level \"new_categories\": {key: [label, one-line description]}")
    return errs


def write_kit(draft: dict) -> None:
    """Add (or replace) the kit in src/kits.py."""
    k = dict(draft["kit"])
    k["page"] = draft["slug"]
    k["items"] = [{x: i[x] for x in ("slug", "qty", "option", "role") if i.get(x) not in (None, "")} for i in k["items"]]
    p = ROOT / "src/kits.py"
    src = p.read_text()
    src = re.sub(r"\n # ---- " + re.escape(k["slug"]) + r" ----\n \{.*?\},\n", "\n", src, flags=re.S)
    j = src.rstrip().rfind("]")
    src = src[:j] + f" # ---- {k['slug']} ----\n {json.dumps(k, ensure_ascii=False)},\n" + src[j:]
    p.write_text(src)


def apply(slug: str, local: bool) -> dict:
    d = A.pdir(slug)
    draft = A.jload(d / "draft.json")
    if not draft:
        return {"slug": slug, "status": "no draft"}
    errs = kit_errors(draft) + product_errors(draft)
    if errs and not draft.get("kit_fix"):
        fx = A.claude(A.fix_prompt(draft, errs + ["(this page sells a kit: keep the 'kit' key, same shape)"]))
        if fx.get("draft"):
            keep = {k: draft[k] for k in ("new_page", "searched_as", "angle", "why_angle", "query", "slug", "kit_page") if k in draft}
            draft = {**fx["draft"], **keep, "status": "ok", "kit_fix": {"errors": errs, "log": fx.get("log")}}
            A.jsave(d / "draft.json", draft)
            errs = kit_errors(draft) + product_errors(draft)
    if errs:
        return {"slug": slug, "status": "failed", "errors": errs}
    if not local:
        return {"slug": slug, "status": "skipped", "reason": "kit pages apply with --local only (the kit and its products are committed first)"}
    dirty = [l for l in subprocess.run(["git", "status", "--porcelain", "src", "docs"], cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
             if not l.endswith(("docs/offers.json", "docs/price-history.json"))]
    if dirty:
        return {"slug": slug, "status": "skipped", "reason": "src/ or docs/ has uncommitted changes"}
    # 1. products and the kit, cart-tested, committed first (abpage.apply refuses a dirty src/)
    import gappage
    news = [p["slug"] for p in draft.get("products") or []]
    if news:
        gappage.insert({**draft, "status": "products_only"}, {})
        subprocess.run(["python3.12", "tools/images.py", *news], cwd=ROOT, capture_output=True, text=True)
    write_kit(draft)
    r = subprocess.run(["python3.12", "tools/kitcheck.py", draft["kit"]["slug"]], cwd=ROOT, capture_output=True, text=True)
    print(r.stdout[-1500:], r.stderr[-600:], flush=True)
    if r.returncode:
        subprocess.run(["git", "checkout", "--", "src/products.py", "src/kits.py", "src/kits-tested.json"], cwd=ROOT)
        subprocess.run(["git", "clean", "-fdq", "src/img"], cwd=ROOT)
        return {"slug": slug, "status": "failed", "errors": ["cart test: " + (r.stdout or r.stderr)[-400:]]}
    subprocess.run(["git", "add", "src/products.py", "src/kits.py", "src/kits-tested.json", "src/img"], cwd=ROOT)
    subprocess.run(["git", "commit", "-q", "-m", f"Kit {draft['kit']['slug']} for /{draft['slug']}: products and cart test (DLC-223)\n\n"
                    "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"], cwd=ROOT)
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    # 2. the page: abpage.apply with the record carrying "kit"; products are already in, so none are re-inserted
    import importlib
    for m in ("products", "gaps"):
        if m in sys.modules:
            importlib.reload(sys.modules[m])
    draft = {**draft, "products": []}
    A.jsave(d / "draft.json", draft)
    orig_rt, orig_pc = A.record_text, A.pick_check
    A.record_text = lambda dr, old, g: orig_rt(dr, old, g).replace('"method": ', f'"kit": {dr["kit"]["slug"]!r},\n "method": ', 1)
    A.pick_check = lambda dr: []   # the pick is the kit (kit_errors checked it); the row-1 product check doesn't apply
    try:
        res = A.apply(slug, True)
    finally:
        A.record_text, A.pick_check = orig_rt, orig_pc
    if res.get("status") != "committed":
        subprocess.run(["git", "revert", "--no-edit", sha], cwd=ROOT, capture_output=True)
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["harvest", "research", "apply"])
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--runs", nargs="*", default=[])
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--local", action="store_true")
    a = ap.parse_args()
    if a.cmd == "harvest":
        for s in a.slugs:
            h = A.harvest(s, a.runs)
            print(f"{s}: {len(h['chats'])} chats, tags {h['searched_as'][:3]}")
    elif a.cmd == "research":
        with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
            for r in ex.map(lambda s: research(s, a.force), a.slugs):
                print(json.dumps(r, ensure_ascii=False), flush=True)
    else:
        for s in a.slugs:
            print(json.dumps(apply(s, a.local), ensure_ascii=False)[:1200], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
