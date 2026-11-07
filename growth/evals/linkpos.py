#!/usr/bin/env python3.12
"""Where the /go/ link sits in a ChatGPT answer, and what layout the answer had (DLC-85; standing metrics DLC-84).

    python3.12 growth/evals/linkpos.py growth/evals/runs/2026-10-28-visibility growth/evals/runs/2026-10-28-w3-r0*
    python3.12 growth/evals/linkpos.py <run dirs or answer files> --stored --md out.md --json out.json
    python3.12 growth/evals/linkpos.py <...> --all-phrasings --any-model      # not only gpt-6 deal answers

Inputs, any mix of:
- a visibility_scan.py / W3 run dir (scan.jsonl + chatgpt/<cell>.json): the last non-downgraded row per cell; the raw
  answer is parsed when chatgpt/<cell>.json exists, else the scan row gives /go/ presence only (position "unknown");
- a ui.py answer file (response.markup = ChatGPT's own answer program, the DIL source);
- a ctxprobe / cardprobe app record (the raw SSE stream, "sse"); the catalog records the answer binds
  (modelDataBindings) give the merchant behind a catalog card's button;
- any other dir: every such file under it.

Per answer (default: gpt-6 only, by resolved_model_slug, falling back to the model_slug; deal and coupon questions):
- layout: "card" (one product block), "list" (two or more), "plain" (no product block). A product block is a
  top-level <box>/<row> with an <AsyncImage>/<AsyncImageGroup> (one product per image) or a buy action
  (GenUI.openUrl button or <Link url>);
- every /go/ link and where it sits: widget_button (GenUI.openUrl("…/go/…")), widget_link (<Link url="…/go/…">),
  inline_md ([text](…/go/…)), bare_text, dom_only (an <a href> in the page but not in the markup), unknown (no raw
  answer); whether it is inside a product block; the product it is attached to (block text, else link text, line and
  heading, matched against offers.json names) and whether that is the /go/ slug's product (wrong_product);
- the destination of every widget button (ours / store / retailer / catalog / other) and of each product block's buy
  action;
- off_question: a /go/ slug that is not the product asked about (kit vs station counts);
- with --stored (metric a, DLC-77 method): did the version of the product page that OAI-SearchBot last fetched before
  the chat carry https://dealectric.com/go/<slug> in its text (crawl log + GitHub Pages deployments + git; no network).

Answers reused from another run (scan.jsonl "reused_from") count once in the pooled numbers.
w3score.py and visibility_scan.py print relay_block() of the same rows; no chats are made here.
"""
from __future__ import annotations

import argparse, html, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

OFFERS_FILE = E.REPO / "docs" / "offers.json"
MODEL = "gpt-6"
DEAL_PHRASINGS = ("deal", "coupon")
GO_RE = re.compile(r"https?://(?:www\.)?dealectric\.com/go/([A-Za-z0-9][A-Za-z0-9\-]*)")
URL_RE = r"https?://[^\s\"'<>)\]}\\]+"
BTN_RE = re.compile(r"""GenUI\.openUrl\(\s*(?:\\?["'](""" + URL_RE + r""")\\?["']|([A-Za-z0-9_]+)\??\.product_page\??\.uri)""")
LINK_RE = re.compile(r"""<Link\b([^>]*?)/?>""", re.S)
MD_RE = re.compile(r"\[([^\]]*)\]\((" + URL_RE + r")\)")
IMG_RE = re.compile(r"<AsyncImage(Group)?\b([^>]*)/?>", re.S)
BLOCK_TAG_RE = re.compile(r"<(/?)(box|row)\b([^>]*?)(/?)>", re.S)
HEAD_RE = re.compile(r"^#{1,4} +(.+)$", re.M)
RETAILERS = ("amazon.", "walmart.", "bestbuy.", "homedepot.", "lowes.", "target.", "costco.", "ebay.", "newegg.",
             "bhphotovideo.", "samsclub.", "wellbots.", "microcenter.", "rei.com", "acehardware.", "tractorsupply.")
GENERIC = set("""the a an and or with for of in to on by at from new plus pro max mini set kit pack bundle portable power
station charger charging wireless magnetic battery batteries bank solar panel generator station's foldable
usb cable fast w wh mah inch in official store us edition version gen formerly silver black
white color colour""".split())


# ------------------------------------------------------------------ catalog of our products
_OFFERS: dict | None = None


def offers() -> dict:
    global _OFFERS
    if _OFFERS is None:
        _OFFERS = {p["id"]: p for p in json.loads(OFFERS_FILE.read_text())["products"]} if OFFERS_FILE.exists() else {}
    return _OFFERS


def toks(s: str) -> set[str]:
    s = re.sub(r"(?<=\d),(?=\d{3})", "", (s or "").lower())
    s = re.sub(r"(\d)\s+(w|wh|mah|ah|v)\b", r"\1\2", s)   # "400 W" and "400W" are one token
    return {t for t in re.split(r"[^a-z0-9]+", s) if len(t) >= 2 or t.isdigit()}


def key_tokens(slug: str) -> set[str]:
    """Identifying tokens from the id and the model field (not the name: a kit's name repeats its station's specs)."""
    p = offers().get(slug) or {}
    brand = toks(p.get("brand") or slug.split("-")[0])
    t = (toks(slug.replace("-", " ")) | toks(p.get("model"))) - brand - GENERIC
    return {x for x in t if any(c.isdigit() for c in x) or len(x) >= 3}


def strong(t: str) -> bool:
    """A token that names a product on its own: a model number (s2000, 400w) or a long name word (aerofit)."""
    return (len(t) >= 2 and any(c.isdigit() for c in t)) or len(t) >= 5


def brand_of(slug: str) -> str:
    return ((offers().get(slug) or {}).get("brand") or slug.split("-")[0]).lower()


def store_hosts(slug: str) -> set[str]:
    """The brand's own store hosts: merchant_url host of every product of the same brand."""
    b = brand_of(slug)
    return {E.host_of(p["offer"].get("merchant_url") or "") for p in offers().values()
            if (p.get("brand") or "").lower() == b and (p.get("offer") or {}).get("merchant_url")} - {""}


def named_products(ctx: str, family: set[str]) -> list[str]:
    """The products of `family` (slugs) the context text names, best first: most identifying tokens matched, then the
    larger share of the product's tokens. A product counts as named with a strong token, two tokens, or all of them."""
    ct = toks(ctx)
    out = []
    for s in family:
        kt = key_tokens(s)
        hit = kt & ct
        if not hit or (not any(strong(x) for x in hit) and len(hit) < 2 and hit != kt):
            continue
        out.append((len(hit) + len(hit) / len(kt), s))
    return [s for _, s in sorted(out, reverse=True)]


def attach(ctx: str, go: str, asked: str) -> str | None:
    """The product a /go/ link sits next to: another product b only when the context names b by a token that tells b
    apart from the go slug's product and names none of the go product's own distinguishing tokens (a kit card holding
    /go/<station> is b = kit). Else the go slug when anything is named, None when nothing is."""
    named = named_products(ctx, family_of(go, asked))
    if not named:
        return None
    ct = {t for t in toks(ctx) if len(t) >= 2}   # a bare digit ("2." in a numbered list) tells nothing apart
    for b in named:
        if b != go and (key_tokens(b) - key_tokens(go)) & ct and not (key_tokens(go) - key_tokens(b)) & ct:
            return b
    return go


def family_of(*slugs: str) -> set[str]:
    brands = {brand_of(s) for s in slugs if s}
    return {s for s, p in offers().items() if (p.get("brand") or "").lower() in brands} | {s for s in slugs if s}


# ------------------------------------------------------------------ reading an answer
def dest_class(url: str, slug: str, catalog: bool = False) -> str:
    h = E.host_of(url)
    if "dealectric.com" in h:
        return "ours"
    if h and (h in store_hosts(slug) or any(h.endswith("." + s) or s.endswith("." + h) for s in store_hosts(slug))):
        return "catalog-store" if catalog else "store"
    if catalog:
        return "catalog-retailer" if any(r in h for r in RETAILERS) else ("catalog" if not h else "catalog-other")
    if any(r in h for r in RETAILERS):
        return "retailer"
    return "other"


def dedupe_parts(parts: list[str]) -> str:
    keep = []
    for p in sorted({p for p in parts if isinstance(p, str) and p.strip()}, key=len, reverse=True):
        if not any(p.strip() in k for k in keep):
            keep.append(p)
    return "\n\n".join(sorted(keep, key=lambda p: parts.index(p)))


def from_sse(rec: dict) -> tuple[str, dict, str | None]:
    """(answer markup, {ref: product_page url}, model) from a ctxprobe/cardprobe record's raw stream."""
    import cardprobe as C
    msgs = [m for st in rec.get("sse") or [] for m in C.rebuild(st.get("text", ""))]
    markup, binds, model = "", {}, None
    for m in msgs:
        md = m.get("metadata") or {}
        if md.get("resolved_model_slug") or md.get("model_slug"):
            model = md.get("resolved_model_slug") or md.get("model_slug")
        c = m.get("content") or {}
        if (m.get("author") or {}).get("role") != "assistant" or c.get("content_type") != "text":
            continue
        parts = [p for p in c.get("parts") or [] if isinstance(p, str)]
        if parts and len(parts[0]) > len(markup):
            markup = parts[0]
        og = (((md.get("model_dil_v2") or {}).get("appData") or {}).get("opGenui") or {})
        for ref, r in (og.get("modelDataBindings") or {}).items():
            if isinstance(r, dict):
                binds[ref] = ((r.get("product_page") or {}).get("uri")) or ""
    return markup, binds, model


def top_blocks(markup: str) -> list[tuple[int, int]]:
    """Spans of top-level <box>/<row> elements."""
    out, depth, start = [], 0, None
    for m in BLOCK_TAG_RE.finditer(markup):
        closing, selfclose = m.group(1) == "/", m.group(4) == "/"
        if selfclose:
            continue
        if not closing:
            if depth == 0:
                start = m.start()
            depth += 1
        elif depth > 0:
            depth -= 1
            if depth == 0 and start is not None:
                out.append((start, m.end()))
                start = None
    if depth > 0 and start is not None:   # unclosed (cut stream): runs to the end
        out.append((start, len(markup)))
    return out


def plain(s: str) -> str:
    s = re.sub(r"<Cite\b[^>]*/>", " ", s)
    s = re.sub(r"""(?:title|value|query|disambig)=\{?["']([^"']*)["']\}?""", r" \1 ", s)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def parse(markup: str, binds: dict, slug: str, dom_urls: list[str] | None = None, catalog_hosts: set[str] | None = None) -> dict:
    """Layout, product blocks, /go/ links with their position and attached product, button destinations."""
    blocks = []
    for a, b in top_blocks(markup):
        seg = markup[a:b]
        imgs = IMG_RE.findall(seg)
        acts = [m for m in BTN_RE.finditer(seg)] + [m for m in LINK_RE.finditer(seg) if re.search(r"\burl=", m.group(1))]
        n = len(imgs) or (1 if acts else 0)
        if n:
            blocks.append({"span": (a, b), "n_products": n, "img_offsets": [a + m.start() for m in IMG_RE.finditer(seg)]})
    n_products = sum(b["n_products"] for b in blocks)
    layout = "list" if n_products >= 2 else "card" if n_products == 1 else "plain"

    def block_at(i):
        return next((b for b in blocks if b["span"][0] <= i < b["span"][1]), None)

    def product_ctx(i: int, b: dict) -> str:
        a, z = b["span"]
        offs = b["img_offsets"]
        if len(offs) >= 2:   # several products in one box: the stretch from the image before i to the next image
            a = max([o for o in offs if o <= i] or [a])
            z = min([o for o in offs if o > i] or [z])
        return plain(markup[a:z])

    def heading_before(i: int) -> str:
        hs = [m.group(1) for m in HEAD_RE.finditer(markup[:i])]
        return hs[-1] if hs else ""

    def line_at(i: int) -> str:
        a = markup.rfind("\n", 0, i) + 1
        z = markup.find("\n", i)
        return markup[a: z if z >= 0 else len(markup)]

    links, spans = [], []

    def add(kind, url, i, label=""):
        m = GO_RE.match(url)
        if not m:
            return
        spans.append((i, i + len(url)))
        b = block_at(i)
        go = m.group(1).lower()
        go = E.resolve_go_slug(go, offers()) or go
        if b:
            attached = attach(product_ctx(i, b), go, slug)
        else:
            attached = None
            for ctx in (plain(label), plain(line_at(i)), plain(heading_before(i))):
                attached = attach(ctx, go, slug)
                if attached:
                    break
        variant = bool(attached and attached != go and (key_tokens(go) & key_tokens(attached)))
        links.append({"slug": go, "where": kind, "in_block": bool(b), "attached": attached,
                      "wrong_product": bool(attached and attached != go), "variant": variant, "label": plain(label).strip()[:80]})

    for m in BTN_RE.finditer(markup):
        if m.group(1):
            add("widget_button", m.group(1), m.start(1))
    for m in LINK_RE.finditer(markup):
        um = re.search(r"""\burl=\\?["']?(""" + URL_RE + ")", m.group(1))
        if um:
            tm = re.search(r"""\btitle=\\?["']([^"'\\]*)""", m.group(1))
            add("widget_link", um.group(1), m.start(1) + um.start(1), tm.group(1) if tm else "")
    for m in MD_RE.finditer(markup):
        add("inline_md", m.group(2), m.start(2), m.group(1))
    for m in GO_RE.finditer(markup):
        if not any(a <= m.start() < z for a, z in spans):
            add("bare_text", m.group(0), m.start())
    have = {l["slug"] for l in links}
    for u in dom_urls or []:
        m = GO_RE.match(u)
        if m and (E.resolve_go_slug(m.group(1).lower(), offers()) or m.group(1).lower()) not in have:
            g = E.resolve_go_slug(m.group(1).lower(), offers()) or m.group(1).lower()
            have.add(g)
            links.append({"slug": g, "where": "dom_only", "in_block": None, "attached": None, "wrong_product": False,
                          "variant": False, "label": ""})

    # every widget button's destination, and each product block's first buy action
    buttons, block_dest = [], []
    cat_host = next(iter(catalog_hosts)) if catalog_hosts and len(catalog_hosts) == 1 else ""
    for m in BTN_RE.finditer(markup):
        if m.group(1):
            buttons.append({"host": E.host_of(m.group(1)), "class": dest_class(m.group(1), slug), "in_block": bool(block_at(m.start()))})
        else:
            u = binds.get(m.group(2)) or (f"https://{cat_host}/" if cat_host else "")
            buttons.append({"host": E.host_of(u) or "catalog", "class": dest_class(u, slug, catalog=True), "in_block": bool(block_at(m.start()))})
    for b in blocks:
        a, z = b["span"]
        seg = markup[a:z]
        first = None
        for m in BTN_RE.finditer(seg):
            if m.group(1):
                first = (m.start(), E.host_of(m.group(1)), dest_class(m.group(1), slug))
            else:
                u = binds.get(m.group(2)) or (f"https://{cat_host}/" if cat_host else "")
                first = (m.start(), E.host_of(u) or "catalog", dest_class(u, slug, catalog=True))
            break
        lm = next((m for m in LINK_RE.finditer(seg) if re.search(r"\b(url|ref)=", m.group(1))), None)
        if lm and (first is None or lm.start() < first[0]):
            um = re.search(r"""\burl=\\?["']?(""" + URL_RE + ")", lm.group(1))
            rm = re.search(r"""\bref=\\?["']?(turn\w+product\d+)""", lm.group(1))
            if um:
                first = (lm.start(), E.host_of(um.group(1)), dest_class(um.group(1), slug))
            elif rm:
                u = binds.get(rm.group(1)) or (f"https://{cat_host}/" if cat_host else "")
                first = (lm.start(), E.host_of(u) or "catalog", dest_class(u, slug, catalog=True))
        block_dest.append({"n_products": b["n_products"], "host": first[1] if first else None, "class": first[2] if first else "none"})
    return {"layout": layout, "n_products": n_products, "n_blocks": len(blocks), "links": links, "buttons": buttons,
            "block_dest": block_dest, "widgets": bool(re.search(r"<(box|row|button|AsyncImage|Link)\b", markup))}


def phrasing_of(qid: str) -> str:
    return (qid or "").rsplit("--", 1)[-1] if "--" in (qid or "") else ""


def row_from_rec(rec: dict, *, run: str, cell: str, qid: str, slug: str, phrasing: str, started_at: str | None,
                 model: str | None, scan: dict | None = None) -> dict:
    binds, catalog_hosts, dom = {}, set(), []
    if rec.get("sse"):
        markup, binds, m2 = from_sse(rec)
        model = model or m2
        fmt = "sse"
    else:
        resp = rec.get("response") or {}
        markup = dedupe_parts(resp.get("markup") or [])
        fmt = "ui" if markup else "ui-dom"
        for c in rec.get("citations") or []:
            u = c.get("url") or ""
            if "openai_catalog" in u or "utm_medium=feed" in u:
                catalog_hosts.add(E.host_of(u))
            if c.get("source") == "ui_href":
                dom.append(E.strip_tracking(u))
        if not markup:
            markup = rec.get("text") or ""
    p = parse(markup, binds, slug, dom_urls=dom, catalog_hosts=catalog_hosts)
    if fmt == "ui-dom":
        p["layout"] = "unknown"
    return finish({"run": run, "cell": cell, "qid": qid, "slug": slug, "phrasing": phrasing, "started_at": started_at,
                   "model": model, "raw": fmt, "reused_from": (scan or {}).get("reused_from"), **p})


def row_from_scan(r: dict, run: str) -> dict:
    links = []
    for u in r.get("go") or []:
        m = GO_RE.match(u)
        if m:
            g = E.resolve_go_slug(m.group(1).lower(), offers()) or m.group(1).lower()
            links.append({"slug": g, "where": "unknown", "in_block": None, "attached": None, "wrong_product": None,
                          "variant": False, "label": ""})
    return finish({"run": run, "cell": r["cell"], "qid": r["qid"], "slug": r["slug"], "phrasing": r.get("phrasing") or phrasing_of(r["qid"]),
                   "started_at": r.get("started_at"), "model": r.get("answer_model") or (r.get("models") or [None])[-1],
                   "raw": None, "reused_from": r.get("reused_from"), "layout": "unknown", "n_products": None, "n_blocks": None,
                   "links": links, "buttons": [], "block_dest": [], "widgets": None})


def finish(row: dict) -> dict:
    gos = sorted({l["slug"] for l in row["links"]})
    row["go"] = gos
    row["go_present"] = bool(gos)
    row["off_question"] = [g for g in gos if g != row["slug"]]
    row["wrong_product"] = sorted({l["slug"] + "->" + l["attached"] for l in row["links"] if l.get("wrong_product")})
    wh = [l["where"] for l in row["links"]]
    order = ["widget_button", "widget_link", "inline_md", "bare_text", "dom_only", "unknown"]
    row["go_where"] = next((w for w in order if w in wh), "absent")
    row["go_in_block"] = any(l.get("in_block") for l in row["links"]) if row["raw"] and row["links"] else None
    return row


# ------------------------------------------------------------------ loading
def load_run(d: Path) -> list[dict]:
    every = [json.loads(l) for l in (d / "scan.jsonl").open() if l.strip()]
    rows = {r["cell"]: r for r in every if not r.get("downgraded")}
    out = []
    for cell, r in rows.items():
        f = d / "chatgpt" / f"{cell}.json"
        if f.exists():
            rec = json.loads(f.read_text())
            model = rec.get("answer_model") or ((rec.get("models") or r.get("models") or [None])[-1])
            out.append(row_from_rec(rec, run=d.name, cell=cell, qid=r["qid"], slug=r["slug"],
                                    phrasing=r.get("phrasing") or phrasing_of(r["qid"]), started_at=r.get("started_at"),
                                    model=model, scan=r))
        else:
            out.append(row_from_scan(r, d.name))
    return out


def load_file(f: Path) -> dict | None:
    try:
        rec = json.loads(f.read_text())
    except (ValueError, UnicodeDecodeError):
        return None
    if not isinstance(rec, dict) or not (rec.get("sse") or isinstance((rec.get("response") or {}), dict) and "markup" in (rec.get("response") or {})):
        return None
    stem = f.stem
    if rec.get("tag"):          # ctxprobe / cardprobe: <qid>--<rep>
        qid = re.sub(r"--\d+$", "", rec["tag"])
    else:                       # ui.py / visibility_scan: <qid>-<n>
        qid = rec.get("qid") or re.sub(r"-\d+$", "", stem)
    slug = rec.get("slug") or qid.split("--")[0]
    if slug not in offers():   # e.g. aurzen-travelplay--discovery: take the longest catalog id the qid starts with
        slug = max((s for s in offers() if qid.startswith(s.split("-")[0]) and s.startswith(qid.split("--")[0])), key=len, default=slug)
    model = rec.get("answer_model") or (None if rec.get("sse") else (rec.get("models") or [None])[-1])
    run = f.parent.parent.name if f.parent.name in ("chatgpt", "app") else f.parent.name
    return row_from_rec(rec, run=run, cell=stem, qid=qid, slug=slug, phrasing=rec.get("phrasing") or phrasing_of(qid),
                        started_at=rec.get("started_at"), model=model)


def load(paths, deal_only: bool = True, model: str | None = MODEL) -> list[dict]:
    rows = []
    for p in map(Path, paths):
        if p.is_dir() and (p / "scan.jsonl").exists():
            rows += load_run(p)
        elif p.is_dir():
            rows += [r for f in sorted(p.rglob("*.json")) if (r := load_file(f))]
        elif p.is_file():
            r = load_file(p)
            if r:
                rows.append(r)
    if deal_only:
        rows = [r for r in rows if r["phrasing"] in DEAL_PHRASINGS]
    if model:
        rows = [r for r in rows if r["model"] == model]
    loaded = {(r["run"], r["cell"]) for r in rows}
    for r in rows:   # an answer reused from a run that is also loaded counts once
        r["dup"] = bool(r.get("reused_from") and (r["reused_from"], r["cell"]) in loaded)
    return rows


# ------------------------------------------------------------------ metric (a): the stored copy carries the /go/ URL
def add_stored(rows: list[dict]) -> None:
    import storedcopy as SC
    crawls = SC.page_crawls(SC.load_crawls())
    deploys = json.loads(SC.DEPLOYS.read_text()) if SC.DEPLOYS.exists() else []
    blobs = SC.Blobs()
    for r in rows:
        r["stored_go"], r["index_fetch"] = None, None
        if not r.get("started_at") or not deploys:
            continue
        t = r["started_at"][:19] + "Z"
        fetch = SC.last_before(crawls.get("/" + r["slug"], {}).get("OAI-SearchBot", []), t)
        if not fetch:
            continue
        dep = [d for d in deploys if d["at"] <= fetch]
        raw = blobs.get(f"{dep[-1]['sha']}:docs/{r['slug']}.html") if dep else None
        if raw is None:
            continue
        text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw.decode("utf-8", "replace"), flags=re.S)))
        r["index_fetch"] = fetch
        r["stored_go"] = f"dealectric.com/go/{r['slug']}" in text


# ------------------------------------------------------------------ summaries
def frac(k: int, n: int) -> str:
    return f"{k}/{n} ({100 * k / n:.0f}%)" if n else "0/0"


def pooled(rows: list[dict]) -> list[dict]:
    return [r for r in rows if not r.get("dup")]


def summarize(rows: list[dict]) -> dict:
    rs = pooled(rows)
    go = [r for r in rs if r["go_present"]]
    raw = [r for r in rs if r["raw"] and r["raw"] != "ui-dom"]
    s = {"n": len(rs), "n_go": len(go), "n_raw": len(raw), "n_go_raw": sum(1 for r in raw if r["go_present"]),
         "where": Counter(r["go_where"] for r in go),
         "go_in_block": Counter(r["go_in_block"] for r in go if r["raw"]),
         "layout": {lay: (sum(r["go_present"] for r in raw if r["layout"] == lay), sum(1 for r in raw if r["layout"] == lay))
                    for lay in ("card", "list", "plain")},
         "buttons": Counter(b["class"] for r in raw for b in r["buttons"]),
         "block_dest": Counter(r["block_dest"][0]["class"] for r in raw if r["block_dest"]),
         "wrong": [f"{r['run']}/{r['cell']}: {', '.join(r['wrong_product'])}" for r in rs if r["wrong_product"]],
         "off_q": [f"{r['run']}/{r['cell']}: {', '.join(r['off_question'])}" for r in rs if r["off_question"]],
         "per_product": {}}
    by = defaultdict(list)
    for r in rs:
        by[r["slug"]].append(r)
    s["per_product"] = {k: (sum(r["go_present"] for r in v), len(v)) for k, v in sorted(by.items())}
    st = [r for r in rs if r.get("stored_go") is not None]
    if any("stored_go" in r for r in rs):
        s["stored"] = {"known": len(st), "with_go": sum(r["stored_go"] for r in st),
                       "go_if_stored": (sum(r["go_present"] for r in st if r["stored_go"]), sum(1 for r in st if r["stored_go"])),
                       "go_if_not": (sum(r["go_present"] for r in st if not r["stored_go"]), sum(1 for r in st if not r["stored_go"])),
                       "never_fetched": sum(1 for r in rs if r.get("stored_go") is None)}
    return s


def relay_block(rows: list[dict], title: str = "/go/ relay (gpt-6, deal and coupon questions; linkpos.py)") -> str:
    """The standing DLC-84 lines for w3score.py and visibility_scan.py."""
    s = summarize(rows)
    if not s["n"]:
        return f"\n{title}: no gpt-6 deal answers in this run"
    lay = ", ".join(f"{k} {frac(*v)}" for k, v in s["layout"].items() if v[1])
    lines = [f"\n{title}",
             f"- (b) /go/ link rate: {frac(s['n_go'], s['n'])} pooled; per product: "
             + "; ".join(f"{k} {a}/{n}" for k, (a, n) in s["per_product"].items()),
             f"- (c) where the /go/ sits: " + (", ".join(f"{k} {v}" for k, v in s["where"].most_common()) or "-")
             + (f"; inside a product block {s['go_in_block'].get(True, 0)} of {sum(s['go_in_block'].values())} parsed" if s["go_in_block"] else ""),
             f"- (c) layout -> /go/ (raw answers only, n={s['n_raw']} of {s['n']}): {lay or 'no raw answers on this machine'}",
             f"- (c) widget buttons go to: " + (", ".join(f"{k} {v}" for k, v in s["buttons"].most_common()) or "-")
             + "; first product block's buy action: " + (", ".join(f"{k} {v}" for k, v in s["block_dest"].most_common()) or "-"),
             f"- (d) /go/ attached to another product: {len(s['wrong'])} of {s['n_go_raw']} parsed /go/ answers"
             + (f" ({s['n_go'] - s['n_go_raw']} more without a raw answer: unknown)" if s['n_go'] > s['n_go_raw'] else "") + (f" ({'; '.join(s['wrong'])})" if s["wrong"] else "")
             + f"; /go/ slug not the product asked about: {len(s['off_q'])}" + (f" ({'; '.join(s['off_q'])})" if s["off_q"] else "")]
    if "stored" in s:
        st = s["stored"]
        lines.append(f"- (a) stored copy (OAI-SearchBot's last fetch before the chat) carries the product's /go/ URL: "
                     f"{st['with_go']}/{st['known']} (page never fetched before the chat: {st['never_fetched']}); "
                     f"/go/ given when it does {frac(*st['go_if_stored'])}, when it doesn't {frac(*st['go_if_not'])}")
    if s["n_raw"] < s["n"]:
        lines.append(f"- {s['n'] - s['n_raw']} answer(s) have no raw answer file here (chatgpt/<cell>.json is gitignored): "
                     "position and layout 'unknown' for them")
    lines.append("- (e) Claude link rate: not measured (no Claude answers to these questions)")
    return "\n".join(lines)


def table(rows: list[dict]) -> str:
    out = ["| run | cell | layout | products | /go/ | where | in block | attached to | block buy action | widget buttons |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (not r["go_present"], r["run"], r["cell"])):
        out.append(f"| {r['run']}{' (dup)' if r.get('dup') else ''} | {r['cell']} | {r['layout']} | {r['n_products'] if r['n_products'] is not None else '-'} | "
                   f"{', '.join(r['go']) or '-'} | {', '.join(sorted({l['where'] for l in r['links']})) or 'absent'} | "
                   f"{'' if r['go_in_block'] is None else 'yes' if r['go_in_block'] else 'no'} | "
                   f"{', '.join(sorted({l['attached'] or '?' for l in r['links']})) if r['raw'] and r['links'] else '-'} | "
                   f"{', '.join(f'{b['class']}:{b['host']}' for b in r['block_dest']) or '-'} | "
                   f"{', '.join(f'{b['class']}:{b['host']}' for b in r['buttons']) or '-'} |")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--all-phrasings", action="store_true", help="not only deal and coupon questions")
    ap.add_argument("--any-model", action="store_true", help="not only gpt-6 answers")
    ap.add_argument("--stored", action="store_true", help="metric (a): the stored copy carries the /go/ URL")
    ap.add_argument("--json")
    ap.add_argument("--md", help="write the per-answer table and the summary as markdown")
    a = ap.parse_args()
    rows = load(a.paths, deal_only=not a.all_phrasings, model=None if a.any_model else MODEL)
    if a.stored:
        add_stored(rows)
    block = relay_block(rows)
    print(block.strip())
    if a.md:
        Path(a.md).write_text(block.strip() + "\n\n" + table(rows) + "\n")
    if a.json:
        Path(a.json).write_text(json.dumps(rows, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
