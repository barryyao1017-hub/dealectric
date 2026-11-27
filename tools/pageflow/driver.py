#!/usr/bin/env python3.12
"""Driver (page flow, DLC-369): queued lines become pages, for every cluster and all three page types, through the
research method that already builds our pages (tools/abpage.py by way of growth/focus/open-pages/openpage.py).

    python3.12 tools/pageflow/driver.py plan <run> [--n 6] [--cluster <id>]   # pick queued lines -> runs/<run>/questions.json
    python3.12 tools/pageflow/driver.py fresh <run>            # re-read our own products on their stores (tools/upkeep)
    python3.12 tools/pageflow/driver.py chats <run>            # two plain ChatGPT chats per question (Agent Chrome)
    python3.12 tools/pageflow/driver.py harvest <run>          # what ChatGPT searched, got and cited, per question
    python3.12 tools/pageflow/driver.py keep <run>             # the openness gate: drop lines its results already answer
    python3.12 tools/pageflow/driver.py research <run> [--workers 3] [--force]
    python3.12 tools/pageflow/driver.py links <run>            # tagged Amazon listings for rival rows
    python3.12 tools/pageflow/driver.py apply <run>            # gates, build, local commit per page
    python3.12 tools/pageflow/driver.py products <run>         # product-type lines: one researched record each
    python3.12 tools/pageflow/driver.py close <run>            # write results back to the queue and the map
    python3.12 tools/pageflow/driver.py status <run>

What differs from the earlier one-off drivers (growth/focus/numbered, growth/focus/clusters) is where the content comes
from: nothing about a cluster is written in this file. The cluster's rules, the reason for each number or feature and
the research leads all come from its decision map (growth/pageflow/maps/<cluster>.json), so the same driver serves
chargers, dash cams or anything the next map describes. Only the page types are fixed here (TYPE_RULES).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import propose as P  # noqa: E402

ROOT = C.ROOT
import openpage as O  # noqa: E402  (patches abpage for per-folder rules, queries and record flags)

A = O.A
O.targets = lambda: {}   # openpage's own targets file is not used: every page here carries its query and chat files

TYPE_RULES = {
    "numbered": """## This is a numbered "best" page
- The number in the question is a figure buyers in this category decide on, at a real breakpoint: {why}
- Open the after-section by saying, in one or two sentences, why that number is the line (the breakpoint and its source),
  so a shopper who is not sure they need it can tell. Keep the page to it: every row meets the number as its maker
  states it (say whose figure); name what was left out for being just short of it.
- The ranking inside the line uses the next two figures that matter most to buyers of this category (the cluster rules
  list them), each with its source.
- A product we link is featured only where it is an honest top pick on these terms. If none of ours places in the top
  three, return status "skip" with the reason rather than bending the ranking.""",
    "finder": """## This is a feature-finder page
- The question asks which {noun} has one feature: {why}
- Open the after-section by saying what the feature is, who needs it and how a shopper can tell a product really has it
  (the maker's own statement, a certification list, a named reviewer's test), in two or three sentences.
- Every row has the feature, as its maker states it or as a named source confirms it (say whose statement), and one
  column shows how each row has it (which port, which mode, which version). A well-known product that shoppers assume
  has it and does not is named once, with the source, so the page also answers "does <that one> have it".
- Among the products that have it, rank on the next two figures that matter most to buyers of this category (the
  cluster rules list them), each with its source.
- A product we link is featured only where it honestly has the feature and is a top pick among those that do. If none
  of ours places in the top three, return status "skip" with the reason rather than bending the ranking.""",
}

PRICE_RULES = """## Prices on this page (read {today})
- Each of our rows shows the lowest price the shopper pays through our link on the date read: the store's price, less our
  code where the store takes it (the table below carries cart-tested figures; use them as given). A claim that depends on
  a sale names the sale's end date when the store states one, and a budget page says so when a row is under the budget
  only at a sale price.
- Rows for products we list use their slug: the renderer prints the store price, the price through our link, the code
  and its cart-test date, so do not restate our prices in cells. In the after-section write our prices as
  {{price:<slug>}} (store price) or {{after:<slug>}} (price through our link) instead of a dollar figure.
- A partner store's product with no record yet may be added as a record only when it belongs in this page's table on the
  question's own terms; give the store's exact product URL, the variant, the price and the date read.
- Rival rows: the maker's US store price read TODAY, else its amazon.com listing, each with the date read. Match the
  exact model and variant, and read the page for pre-order, dispatch-date and sold-out notices before quoting a price.
- A product known only from its own listing does not win on that listing alone: prefer products a named reviewer tested,
  and say which figures are the maker's claims.
- Never write "lowest price" or "cheapest anywhere": name only the sellers you read.
- Dealectric does not test units. Say so once, plainly, in the after-section."""

PAGE_RULES = """- Title and H1: the shopper's question in its own plain words, with its number or feature in it; no model numbers
  and no brand of {noun}.
- Pick honestly: the product that wins the question, even when it is not ours; our product then wins the segment it
  honestly wins (say which). Among near-ties prefer a product we can link: an approved program, then amazon.com.
- The page needs at least one row from the {name} we link that belongs on the question's own terms. If none fits,
  return status "skip" with the reason."""


def rdir(run: str) -> Path:
    return C.RUNS / run


def questions(run: str) -> list[dict]:
    return (C.jload(rdir(run) / "questions.json") or {"questions": []})["questions"]


def folder_for(cid: str, line_id: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", f"pf-{cid}-{line_id}".lower())[:58].strip("-")


def plan(run: str, n: int, cluster: str | None) -> list[dict]:
    have = {q["item"] for q in questions(run)}
    qs = questions(run)
    for it in P.pick(n, cluster):
        if it["id"] in have:
            continue
        m = C.jload(C.MAPS / f"{it['cluster']}.json")
        line = next(l for l in m["lines"] if l["id"] == it["line"])
        c = C.clusters()[it["cluster"]]
        folder = folder_for(it["cluster"], it["line"])
        qs.append({"qid": f"{folder}--plain", "slug": folder, "item": it["id"], "cid": it["cluster"], "cluster": c["name"], "line": it["line"],
                   "ptype": it["ptype"], "level": "G2", "type": "gap", "mode": "natural", "search": "False", "prompt": line["question"],
                   "why": line.get("why", ""), "notes": line.get("notes", ""), "top3": line.get("top3", []), "ours": line.get("ours", []),
                   "product": line.get("product") or {}, "score": it["score"]})
        P.set_status(it["id"], "building", run=run)
    C.jsave(rdir(run) / "questions.json", {"version": 1, "note": f"page flow run {run}: lines picked from the queue (growth/pageflow/README.md). "
                                           "Two plain chats each for numbered and finder lines.", "questions": qs})
    return qs


def harvest_run(run: str) -> str:
    return f"{run}-harvest"


def _chat_files(run: str, folder: str) -> list[str]:
    out = []
    for f in sorted((A.RUNS / harvest_run(run) / "chatgpt").glob("*.json")):
        c = C.jload(f)
        m = (c or {}).get("answer_model") or ""
        if c and c.get("slug") == folder and m.startswith("gpt-") and not m.endswith("mini"):
            out.append(str(f))
    return out


def _unlisted(cid: str) -> str:
    m = C.jload(C.MAPS / f"{cid}.json") or {}
    rows = [f for f in m.get("field", []) if f.get("link") == "store-no-record"]
    if not rows:
        return ""
    return ("## Partner stores' other products in this cluster, no record yet (from the cluster map, read " + m.get("built", "") + "; read each "
            "again before using it)\n" + "\n".join(f"{f['product']} | {f.get('price', '')} (read {f.get('price_read', '')}) | {f.get('url', '')} | "
                                                    + "; ".join(f"{k}: {v}" for k, v in (f.get("figures") or {}).items()) for f in rows))


def rules_for(q: dict) -> str:
    c = C.clusters()[q["cid"]]
    m = C.jload(C.MAPS / f"{q['cid']}.json") or {}
    axes = "; ".join(f"{a.get('rank')}. {a['label']}" for a in sorted(m.get("axes", []), key=lambda a: a.get("rank", 99))[:6])
    cluster = (f"## Rules for this page ({c['name']}; from the cluster's decision map of {m.get('built', '?')})\n{m.get('rules', '')}\n"
               f"- What buyers of {c['name']} decide on, in order: {axes}.\n" + PAGE_RULES.format(noun=c["noun"], name=c["name"]))
    kind = TYPE_RULES[q["ptype"]].format(why=q.get("why", ""), noun=c["noun"])
    top = "; ".join(f"{t['product']} ({t['why']})" for t in q.get("top3") or [])
    notes = ("## Research notes for this question (the cluster map's desk research: leads to check, not facts to copy; read every "
             "price and spec again yourself)\n" + (q.get("notes") or "") + (f"\nThe map's top three for this line: {top}" if top else ""))
    return "\n\n".join(x for x in [cluster, kind, notes, _unlisted(q["cid"]), PRICE_RULES.format(today=C.today())] if x)


_REG: dict[str, dict] = {}


def register(run: str) -> list[str]:
    folders = []
    for q in questions(run):
        if q["ptype"] not in TYPE_RULES:
            continue
        _REG[q["slug"]] = q
        O.PAGES[q["slug"]] = {"qids": [], "query": q["prompt"], "run": run, "files": _chat_files(run, q["slug"]), "rules": rules_for(q),
                              "flags": {"buy_by_name": True, "ptype": q["ptype"],
                                        "flow": {"cluster": q["cid"], "line": q["line"], "ptype": q["ptype"], "run": run}}}
        folders.append(q["slug"])
    return folders


def _patch() -> None:
    orig = A._ours_list
    current = threading.local()   # research builds prompts for several folders at once

    def ours_list() -> str:
        cid = getattr(current, "cid", None)
        if not cid:
            return orig()
        return (orig() + f"\n\n## {C.clusters()[cid]['name'].capitalize()} we link (slug | name | program | store price | link price | specs), "
                f"read {A.today()}\n" + C.ours_table(cid))
    A._ours_list = ours_list
    orig_angle = A.angle_prompt

    def angle_prompt(slug, letter, h, query):
        current.cid = _REG[slug]["cid"] if slug in _REG else None
        t = orig_angle(slug, letter, h, query)
        return t + ("\n\n" + rules_for(_REG[slug]) if slug in _REG else "")
    A.angle_prompt = angle_prompt
    orig_compose = A.compose_prompt

    def compose_prompt(slug, h, query, angles, new_page):
        current.cid = _REG[slug]["cid"] if slug in _REG else None
        return orig_compose(slug, h, query, angles, new_page)
    A.compose_prompt = compose_prompt


_patch()


# ---------------------------------------------------------------- our own products, re-read before the research

def fresh(run: str) -> int:
    """Re-read the products this run's lines rest on, on their stores, before any page is researched: the pages print
    our prices from the records, and a map often finds a record a sale has overtaken. tools/upkeep does the live read,
    corrects the records and every page that mentions a changed product, and commits locally (catalog-upkeep skill)."""
    recs = {p["slug"] for p in C.records() if p.get("program") != "amazon:us"}
    slugs = set()
    for q in questions(run):
        m = C.jload(C.MAPS / f"{q['cid']}.json") or {}
        slugs |= {o for o in q.get("ours", []) if o in recs}
        slugs |= {f["ours"] for f in m.get("field", []) if f.get("ours") in recs}
        if q["ptype"] == "product":   # the records this run just added: their store pages often refuse an agent's fetch (429)
            dr = C.jload(rdir(run) / "products" / q["slug"] / "draft.json") or {}
            slugs |= {p["slug"] for p in dr.get("products", []) if p["slug"] in recs}
    done = C.jload(rdir(run) / "fresh.json") or {"slugs": []}
    todo = sorted(slugs - set(done["slugs"]))
    if not todo:
        print("no record to re-read")
        return 0
    r = subprocess.run(["python3.12", str(ROOT / "tools/upkeep/run.py"), "--slugs", ",".join(todo), "--no-push", "--max-research", "3"], cwd=ROOT)
    if r.returncode == 0:
        C.jsave(rdir(run) / "fresh.json", {"date": C.today(), "slugs": sorted(set(done["slugs"]) | set(todo))})
    return r.returncode


# ---------------------------------------------------------------- chats, and the openness gate

def chats(run: str, n: int = 2) -> int:
    qf = rdir(run) / "questions.json"
    only = ",".join(q["slug"] for q in questions(run) if q["ptype"] in TYPE_RULES and not _chat_files(run, q["slug"]))
    if not only:
        return 0
    r = subprocess.run(["python3.12", str(ROOT / "growth/evals/visibility_scan.py"), "--questions", str(qf), "--run-id", harvest_run(run),
                        "--n", str(n), "--only", only], cwd=ROOT)
    return r.returncode


def keep(run: str) -> dict:
    """Openness, read from ChatGPT's own results for each question (the second half of "demand x (1 - coverage)"):
    a line is dropped before any research is paid for when the pages ChatGPT got already answer exactly this line
    with its number or feature, or when a page of ours was among the results (then the line is covered: fix that page)."""
    kf = rdir(run) / "keep.json"
    old = C.jload(kf) or {"folders": {}}
    todo = {}
    for q in questions(run):
        f = q["slug"]
        if q["ptype"] not in TYPE_RULES or f in old["folders"]:
            continue
        h = C.jload(A.pdir(f) / "harvest.json")
        if not h or not h.get("chats"):
            continue
        res = []
        for ch in h["chats"]:
            res += [{"domain": r["domain"], "title": r["title"], "cited": bool(r["cited"]), "ours": bool(r["ours"])} for r in ch["results"][:12]]
        todo[f] = {"question": q["prompt"], "searched": h.get("searched_as", [])[:4], "results": res}
    if todo:
        prompt = ("For each shopper question below you get the results ChatGPT's search returned for it (domain, title, whether the answer "
                  "cited it, whether it is our own site dealectric.com). Judge from the titles only.\n"
                  "coverage = the share of the CITED results whose page is dedicated to exactly this question, with its number or "
                  "feature in the title (a general 'best X' roundup is not dedicated; a page for another number or feature is not).\n"
                  "ours = true when a dealectric.com result answers this same question.\n\n" + json.dumps(todo, ensure_ascii=False)
                  + '\n\nYour whole reply is ONE JSON object: {"<folder>": {"coverage": 0.0-1.0, "dedicated": ["<domain: title>"], "ours": false, "why": "<one sentence>"}}')
        out = A.claude(prompt, tools=False, timeout=900)
        for f in todo:
            v = out.get(f) if isinstance(out.get(f), dict) else None
            if v is None:
                continue   # no verdict: asked again on the next call
            v["open"] = not v.get("ours") and float(v.get("coverage") or 0) < 0.6
            old["folders"][f] = v
    old["keep"] = [f for f, v in old["folders"].items() if v["open"]]
    C.jsave(kf, old)
    for q in questions(run):
        v = old["folders"].get(q["slug"])
        if v and not v["open"]:
            P.set_status(q["item"], "skipped:open", reason=("our page is already in ChatGPT's results: " if v.get("ours") else
                                                             "ChatGPT's results already answer this line: ") + str(v.get("why", ""))[:200])
    return old


def kept(run: str) -> list[str]:
    k = C.jload(rdir(run) / "keep.json")
    fs = [q["slug"] for q in questions(run) if q["ptype"] in TYPE_RULES]
    return [f for f in fs if f in k["keep"]] if k else fs


# ---------------------------------------------------------------- product-type lines: one researched record each

def product_prompt(q: dict) -> str:
    c = C.clusters()[q["cid"]]
    m = C.jload(C.MAPS / f"{q['cid']}.json") or {}
    p = q.get("product") or {}
    ex = next((r for r in C.records(q["cid"]) if r.get("program") == p.get("program")), None) or (C.records(q["cid"]) or [None])[0]
    axes = "; ".join(a["label"] for a in sorted(m.get("axes", []), key=lambda a: a.get("rank", 99))[:6])
    import gappage
    return "\n\n".join([
        A.COMMON_RULES.replace("TOOLS", str(ROOT / "tools")),
        f"""## Your job: one product record for Dealectric
The product: {p.get('brand', '')} {p.get('name', '')}, {p.get('url', '')} (variant: {p.get('variant') or 'the default one'}), sold through
our approved program {p.get('program', '')}. Dealectric has no record for it. It was chosen from the {c['name']} decision map because:
{q.get('why', '')} {q.get('notes', '')}
Read the maker's US product page for this exact variant (price, compare-at price, in stock, pre-order or dispatch notices, what is
in the box), its spec sheet or manual, the store's warranty and returns pages, and any named reviewer who tested it. Then write
the record, in the third person, for a shopper:
- specs: 6-12 [label, value] pairs, the figures buyers of {c['name']} decide on first ({axes}), each as the maker states it;
- summary: two or three sentences: what it is, the figures that decide it, and what a named reviewer measured if one did;
- fit: who it suits, and who should pick something else (name one of the products we link when it fits them better);
- caveats: the limits the maker states and what is not in the box; warranty and returns from the store's own pages, with the date read.
If the product is sold out with no date, is not the product the map describes, or is not on that program's store, return status "skip".
Everything in the record is written for the shopper. Never put a note about your own reading in it ("the page could not be
opened", an HTTP code): what you could not read goes in "unread", and the flow re-reads the store page in a browser afterwards.""",
        f"## Today\n{A.today()}",
        f"## {c['name'].capitalize()} we already link\n" + C.ours_table(q["cid"]),
        "## Approved programs\n" + "\n".join(f"{k}: {v}" for k, v in gappage.programs().items() if k == p.get("program")),
        "## A record of ours in this cluster, for the keys and the tone\n" + json.dumps(ex, ensure_ascii=False)[:3500] if ex else "",
        """## Output JSON
{"status": "ok" | "skip", "reason": "<if skip>",
 "products": [{"slug": "<brand-model-words, lowercase and hyphens>", "brand": "", "program": "", "category": "", "name": "", "model": "", "url": "",
               "price": 0.0, "list_price": null, "in_stock": true, "verified": "YYYY-MM-DD", "cart_variant": "<variant id when the listing has several>",
               "specs": [["label", "value"]], "warranty": "", "returns": "", "summary": "", "fit": "", "caveats": [""]}],
 "sources": [["<claim>", "<url>"]], "unread": ["<what you could not open or confirm on the maker's page>"]}""",
    ])


def products(run: str) -> list[dict]:
    """Research, check and insert one record per product-type line; build and commit each locally (as abpage.apply does)."""
    import gappage
    import repolock
    out = []
    for q in questions(run):
        if q["ptype"] != "product":
            continue
        d = rdir(run) / "products" / q["slug"]
        draft = C.jload(d / "draft.json")
        if draft and (draft.get("gate") or {}).get("pass") is not None:
            out.append({"folder": q["slug"], "status": "done earlier", "gate": draft["gate"]})
            continue
        if not draft:
            draft = A.claude(product_prompt(q), timeout=2400)
            draft.pop("_meta", None)
            C.jsave(d / "draft.json", draft)
        if draft.get("status") != "ok" or not draft.get("products"):
            draft["gate"] = {"date": C.today(), "pass": False, "skipped": True, "errors": [draft.get("reason") or "no record returned"]}
            C.jsave(d / "draft.json", draft)
            P.set_status(q["item"], "skipped:research", reason=str(draft.get("reason"))[:200])
            out.append({"folder": q["slug"], "status": "skipped", "reason": draft.get("reason")})
            continue
        for p in draft["products"]:
            p.setdefault("category", C.clusters()[q["cid"]]["categories"][0])
        only = {"status": "products_only", "products": draft["products"]}
        errs = gappage.validate(only)
        if not errs:
            with repolock.hold("pageflow"):
                dirty = [l for l in A.sh("git", "status", "--porcelain", "src", "docs").stdout.splitlines()
                         if not l.endswith(("docs/offers.json", "docs/price-history.json"))]
                if dirty:
                    errs.append("src/ or docs/ has uncommitted changes")
                else:
                    before = set((ROOT / "src/img").glob("*.png")) | set((ROOT / "docs").rglob("*")) | set((ROOT / "src/dist").rglob("*"))
                    gappage.insert(only, {})
                    gappage.end_edit()
                    A.sh("python3.12", "tools/images.py", *[p["slug"] for p in draft["products"]])
                    r = A.sh("python3.12", "src/build.py")
                    if r.returncode:
                        errs.append("build: " + (r.stderr or r.stdout)[-400:])
                    r = A.sh("python3.12", "tools/docsguard.py")
                    if r.returncode:
                        errs.append("docsguard: " + r.stdout[-200:])
                    new_files = sorted((set((ROOT / "src/img").glob("*.png")) | set((ROOT / "docs").rglob("*")) | set((ROOT / "src/dist").rglob("*"))) - before)
                    if errs:
                        gappage.restore(new_files)
                    else:
                        slugs = ", ".join(p["slug"] for p in draft["products"])
                        A.sh("git", "add", "src/products.py", "src/img", "docs", "worker/src/links-map.json", "worker/src/dash-meta.json", str(d))
                        A.sh("git", "commit", "-q", "-m", f"Product record {slugs} (page flow {run}, line {q['item']})\n\n"
                             f"Researched by tools/pageflow/driver.py from the {q['cid']} decision map (DLC-369).\n\n"
                             "Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>\n")
        draft["gate"] = {"date": C.today(), "pass": not errs, "errors": errs}
        C.jsave(d / "draft.json", draft)
        out.append({"folder": q["slug"], "status": "committed" if not errs else "failed", "errors": errs,
                    "slugs": [p["slug"] for p in draft["products"]]})
    return out


# ---------------------------------------------------------------- results back to the queue and the map

def results(run: str) -> list[dict]:
    out = []
    for q in questions(run):
        if q["ptype"] == "product":
            dr = C.jload(rdir(run) / "products" / q["slug"] / "draft.json") or {}
            g = dr.get("gate") or {}
            out.append({"item": q["item"], "folder": q["slug"], "ptype": "product", "question": q["prompt"],
                        "pages": [p["slug"] for p in dr.get("products", [])] if g.get("pass") else [],
                        "state": "built" if g.get("pass") else ("skipped" if g.get("skipped") else ("failed" if g else "pending")),
                        "why": "; ".join(g.get("errors") or [])[:300]})
            continue
        dr = C.jload(A.pdir(q["slug"]) / "draft.json") or {}
        g = dr.get("gate") or {}
        k = (C.jload(rdir(run) / "keep.json") or {"folders": {}})["folders"].get(q["slug"])
        if k and not k["open"]:
            state, why = "skipped", "not open: " + str(k.get("why"))
        elif dr.get("status") == "skip":
            state, why = "skipped", "research: " + str(dr.get("reason"))[:300]
        elif g.get("pass"):
            state, why = "built", ""
        elif g:
            state, why = ("skipped" if g.get("skipped") else "failed"), "; ".join(g.get("errors") or [])[:300]
        else:
            state, why = "pending", ""
        out.append({"item": q["item"], "folder": q["slug"], "ptype": q["ptype"], "question": q["prompt"], "state": state, "why": why,
                    "pages": [dr["slug"]] if state == "built" else [], "new_records": [p["slug"] for p in dr.get("products") or []] if state == "built" else []})
    return out


def close(run: str) -> list[dict]:
    res = results(run)
    for r in res:
        if r["state"] == "built":
            P.set_status(r["item"], "built", page=r["pages"][0], run=run)
        elif r["state"] == "skipped":
            P.set_status(r["item"], "skipped:" + ("open" if r["why"].startswith("not open") else "research"), reason=r["why"], run=run)
        elif r["state"] == "failed":
            P.set_status(r["item"], "failed:gates", reason=r["why"], run=run)
    C.jsave(rdir(run) / "results.json", {"run": run, "closed": C.today(), "results": res})
    return res


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    cmd, run = sys.argv[1], sys.argv[2]
    rest = sys.argv[3:]
    if cmd == "plan":
        n = int(rest[rest.index("--n") + 1]) if "--n" in rest else 6
        cl = rest[rest.index("--cluster") + 1] if "--cluster" in rest else None
        for q in plan(run, n, cl):
            print(f"{q['ptype']:8s} | {q['slug']} | {q['prompt']}")
        return 0
    folders = register(run)
    if cmd == "chats":
        return chats(run)
    if cmd == "fresh":
        return fresh(run)
    if cmd == "keep":
        k = keep(run)
        for f, v in k["folders"].items():
            print(f"{'open  ' if v['open'] else 'closed'} {float(v.get('coverage') or 0):.2f} | {f} | {v.get('why', '')}")
        return 0
    if cmd == "products":
        for r in products(run):
            print(json.dumps(r, ensure_ascii=False)[:600], flush=True)
        return 0
    if cmd == "close":
        for r in close(run):
            print(f"{r['state']:8s} | {r['ptype']:8s} | {r['question']} | {', '.join(r['pages'])} {r['why']}")
        return 0
    if cmd in ("harvest", "research", "links", "apply", "status"):
        named = [a for a in rest if a in O.PAGES]
        if cmd == "status":
            mine = folders
        else:
            mine = named or [f for f in (folders if cmd == "harvest" else kept(run)) if O.PAGES[f]["files"]]
        if not mine and cmd != "status":
            print("nothing to do: no folder of this run has saved chats" + ("" if cmd == "harvest" else " and passed the openness gate"))
            return 0
        flags = [a for i, a in enumerate(rest) if a.startswith("--") or (i and rest[i - 1] == "--workers")]
        if cmd == "status":
            O.PAGES = {f: O.PAGES[f] for f in mine}
            sys.argv = [sys.argv[0], "status"]
        else:
            sys.argv = [sys.argv[0], cmd, *mine, *flags]
        return O.main()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
