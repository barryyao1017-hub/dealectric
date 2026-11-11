"""Page, brand and offer records for the sales dashboard (claude.ai artifact "Dealectric Sales Dashboard", 2026-11-11).

build.py writes them to worker/src/dash-meta.json on every build; the edge Worker's cron copies that file from GitHub
into D1 (meta_pages, meta_brands, meta_offers), where the dashboard joins them to traffic and sales. Each page and brand
gets a topic and the experiment it was built under, with that experiment's hypothesis in one sentence.

Page keys are the published path without slashes ("" = home), the same key the Worker logs in pageviews.page.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# One sentence per experiment, from the growth/ write-ups named in each comment.
H_GAPMINE = "Pages for questions with measured demand and thin coverage (opening = demand x (1 - coverage)) earn assistant landings (growth/gapmine/README.md)."
H_FUNNEL = "A page aimed at a gap question (few good answers) gets a higher code-and-link rate than one on a saturated question (growth/gap-experiment.md H1-H3)."
H_QUERY = "A page titled with the query the assistants themselves type gets indexed, ranks top 10 and is cited unprompted (DLC-51, growth/query-pages.md)."
H_BRAND_LAUNCH = "A page per newly approved program makes its products citable as soon as the program is linked."
H_KIT = "A researched bundle behind one filled-cart link sells where single products don't (kit pilot DLC-223)."
H_CODES = "A code tested in the brand's own cart makes assistants carry our /go/ link along with the code (Phase 2, growth/improvement-loop.md)."
H_FOCUS = "W3 focus product: copy changes on a few products ChatGPT already shows raise the share of answers with our /go/ link (growth/first-sale-plan.md)."
H_SEASON = "Black Friday and Cyber Monday shoppers ask for deals; one hub per category with cart-tested codes catches that demand."

FAMILIES = [   # (regex on the gap question's family, experiment name, hypothesis)
    (r"gap mining|^x2[01]", "Gap mining", H_GAPMINE),
    (r"brand page for|Awin brands", "Brand launch", H_BRAND_LAUNCH),
    (r"kit|solar kits", "Kits", H_KIT),
    (r"funnel|^x1[89]|run$|DLC-", "Gap funnels", H_FUNNEL),
]

ANGLES = {"A": "Normalise", "B": "Derive", "C": "Compatibility", "D": "Mechanism", "E": "Named measurements",
          "K1": "Sizing", "K2": "Compatibility", "K3": "Traps"}   # tools/abpage.py ANGLES, tools/kitpage.py KIT_ANGLES


def key(url_or_path):
    """Published page key: the last path segment (build.py flatten() publishes /a/b/<x>/ as /<x>), "" for the home page."""
    path = re.sub(r"^https?://[^/]+", "", url_or_path)
    segs = [s for s in path.split("/") if s]
    return re.sub(r"\.html$", "", segs[-1]) if segs else ""


def gap_record(g):
    q = g.get("question", "")
    m = re.match(r"(G\d+)\w* \((.*)\)", q)
    fam = m.group(2) if m else q
    exp, hyp = "Gap experiment", H_FUNNEL
    if re.match(r"Q\d+", q):
        exp, hyp = "Query pages (DLC-51)", H_QUERY
    else:
        for rx, e, h in FAMILIES:
            if re.search(rx, fam, re.I):
                exp, hyp = e, h
                break
    if g.get("kit"):
        exp, hyp = "Kits", H_KIT
    detail = []
    if g.get("method"):
        detail.append(f"research method {g['method']}")
    if g.get("angle"):
        detail.append(f"angle {g['angle']} ({ANGLES.get(g['angle'], '?')})")
    return {"experiment": exp, "hypothesis": hyp, "batch": (m.group(1) + ": " if m else "") + fam + (
        "; " + ", ".join(detail) if detail else ""), "published": g.get("published", "")}


def meta(products, gaps, comparisons, kits, links, codes_path, urls, focus_slugs=(), bfcm=None):
    pages = {}
    def add(k, **rec):
        pages.setdefault(k, {"page": k, **rec})

    for c in comparisons:
        add(c["slug"], kind="comparison", topic=c.get("h1") or c.get("title", ""), **gap_record(c))
    for g in gaps:
        add(g["slug"], kind="gap" if not g.get("kit") else "kit", topic=g.get("h1") or g.get("title", ""), **gap_record(g))

    compared = {}
    kit_items = {k["slug"]: [i["slug"] for i in k["items"]] for k in kits}
    for c in comparisons + gaps:
        for r in c.get("rows", []):
            for s in ([r["slug"]] if r.get("slug") else []) + kit_items.get(r.get("kit"), []):
                compared.setdefault(s, []).append(c["slug"])
    for p in products:
        if p["slug"] in focus_slugs:
            exp, hyp = "W3 focus", H_FOCUS
        elif compared.get(p["slug"]):
            n = len(set(compared[p["slug"]]))
            exp, hyp = "Catalog", f"Supplies {n} comparison page{'s' if n > 1 else ''} (e.g. /{compared[p['slug']][0]}) with a priced, linkable record."
        else:
            exp, hyp = "Catalog", f"Catalog coverage for {p['brand']}."
        add(p["slug"], kind="product", topic=p["name"], experiment=exp, hypothesis=hyp, batch=p.get("category", ""),
            published="", brand=p["brand"])

    for b in sorted({p["brand"] for p in products}):
        add(key(codes_path(b)), kind="brand codes", topic=f"{b} discount codes", experiment="Discount-code pages",
            hypothesis=H_CODES, batch="", published="", brand=b)

    for g in (bfcm or {}).get("groups", []):
        add(g["slug"], kind="seasonal", topic=g.get("h1", g["slug"]), experiment="Black Friday", hypothesis=H_SEASON,
            batch="", published="")
    for u in urls:
        k = key(u)
        if k in ("black-friday-deals", "cyber-monday-deals"):
            add(k, kind="seasonal", topic=k.replace("-", " ").capitalize(), experiment="Black Friday", hypothesis=H_SEASON,
                batch="", published="")
        add(k, kind="site", topic="Home" if k == "" else k.replace("-", " ").capitalize(), experiment="Site",
            hypothesis="Core site page (navigation, trust, data for agents).", batch="", published="")

    # Brands: networks, categories, and the program note that says when and why it was joined.
    brands = {}
    for p in products:
        net, _, prog = (p.get("program") or "").partition(":")
        b = brands.setdefault(p["brand"], {"brand": p["brand"], "networks": set(), "categories": {}, "notes": [], "aliases": set()})
        b["aliases"].add(p["brand"].lower())
        if net:
            b["networks"].add(net)
        b["categories"][p.get("category", "")] = b["categories"].get(p.get("category", ""), 0) + 1
        rec = (links.get(net) or {}).get(prog) or {}
        if rec.get("name") and net != "amazon":
            b["aliases"].add(rec["name"].lower())
        note = (rec.get("note") or "").split(". ")[0]
        if note and note not in b["notes"]:
            b["notes"].append(note)
        if rec.get("rate"):
            b.setdefault("rate", rec["rate"])
    launch = {re.split(r"[:,)]", g["question"].split("brand page for ", 1)[1])[0].split(" (")[0].strip(): g["slug"]
              for g in gaps if "brand page for " in g.get("question", "")}
    out_brands = []
    for b in brands.values():
        cats = sorted(b["categories"], key=lambda c: -b["categories"][c])
        hyp = H_BRAND_LAUNCH if b["brand"] in launch else "Approved program whose products fill comparison pages and earn commission."
        out_brands.append({
            "brand": b["brand"], "network": "/".join(sorted(b["networks"])), "rate": b.get("rate", ""),
            "topic": ", ".join(c.replace("-", " ") for c in cats[:3] if c),
            "experiment": "Brand launch" if b["brand"] in launch else "Program onboarding",
            "hypothesis": hyp + (f" Launch page: /{launch[b['brand']]}." if b["brand"] in launch else ""),
            "added": "; ".join(b["notes"])[:300], "aliases": sorted(b["aliases"])})

    return {"pages": sorted(pages.values(), key=lambda r: r["page"]), "brands": sorted(out_brands, key=lambda r: r["brand"])}


def offers(links_map):
    """/go/ slug -> brand and the page that sells it."""
    return [{"slug": s, "brand": e.get("brand", ""), "page": key(e.get("page") or s), "network": e.get("network", "")}
            for s, e in sorted(links_map.items())]


def write(path, products, gaps, comparisons, kits, links, codes_path, urls, links_map):
    import focus
    ab = os.path.join(ROOT, "src", "bfcm.json")
    m = meta(products, gaps, comparisons, kits, links, codes_path, urls,
             focus_slugs=set(focus.BUYBOX) | set(focus.DEAL_ROW), bfcm=json.load(open(ab)) if os.path.exists(ab) else None)
    m["offers"] = offers(links_map)
    for b in m["brands"]:
        b["aliases"] = list(b["aliases"])
    open(path, "w").write(json.dumps(m, indent=1, ensure_ascii=False) + "\n")
    return m
