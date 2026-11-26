#!/usr/bin/env python3.12
"""Open-query report (2026-11-14): read the discovery run's saved answers, call each query open / contested / closed
from ChatGPT's own answer, crop the screenshots and write one HTML page.

    python3.12 growth/focus/open-queries/report.py [--run-id 2026-11-14-openq]

Verdict from one plain chat (rules of thumb from the 11-14 top/bottom analysis, not a validated gate):
  no search   ChatGPT answered from memory: no page can be retrieved.
  open        it searched, at most half of the product rows are catalog cards, and at most a third of the sources it
              cited are primary (a maker, an official body or a major reviewer).
  contested   one of the two fails.     closed   both fail.
Answers that name no product are kept apart ("advice"): nothing from the catalog competes, but nothing is being sold.
"""
from __future__ import annotations

import argparse, html, json, re, subprocess, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "growth" / "evals"))
from domains import classify  # noqa: E402
import openscan as O  # noqa: E402
import visibility_scan as VS  # noqa: E402

PRIMARY = {"maker", "official", "publisher"}
LABEL = {"maker": "maker", "official": "official body", "publisher": "major reviewer", "retailer": "retailer",
         "community": "forum", "small": "small site", "ours": "Dealectric"}


def verdict(r: dict) -> dict:
    rows = r["carded"] + r["typed"]
    cited = [d for d in r["cited"] if classify(d) != "ours"]
    cls = [classify(d) for d in cited]
    prim = sum(c in PRIMARY for c in cls)
    card_share = r["carded"] / rows if rows else 0.0
    prim_share = prim / len(cited) if cited else 0.0
    top = [classify(d) for d in r["results"]]
    top_prim = sum(c in PRIMARY for c in top)
    if not r["searched"]:
        v = "no search"
    else:
        ok_card, ok_src = card_share <= 0.5, prim_share <= 1 / 3
        v = "open" if ok_card and ok_src else "closed" if not ok_card and not ok_src else "contested"
        if rows == 0:
            v = "advice, open" if ok_src else "advice, sourced"
    return {"verdict": v, "rows": rows, "card_share": card_share, "prim_share": prim_share, "cited_cls": cls,
            "cited_other": cited, "top_prim": top_prim, "top_n": len(top)}


def reason(r: dict, v: dict) -> str:
    out = []
    if not r["searched"]:
        return "ChatGPT answered from memory without searching, so no page is read for this question."
    if v["rows"]:
        if r["carded"] == 0:
            out.append(f"ChatGPT named {v['rows']} product{'s' if v['rows'] != 1 else ''} and attached a catalog card to none of them in this answer: it typed every row itself.")
        else:
            out.append(f"{r['carded']} of {v['rows']} product rows are catalog cards; ChatGPT typed the other {r['typed']} itself.")
    else:
        out.append("The answer names no product, so nothing from the catalog competes, and nothing is being sold either.")
    c = Counter(v["cited_cls"])
    if v["cited_other"]:
        parts = [f"{n} {LABEL[k]}{'s' if n != 1 and k != 'official' else ''}" for k, n in c.most_common()]
        names = ", ".join(dict.fromkeys(v["cited_other"]))
        out.append(f"It cited {len(v['cited_other'])} source{'s' if len(v['cited_other']) != 1 else ''}: {', '.join(parts)} ({names}).")
    else:
        out.append("It cited no source for its recommendations.")
    out.append(f"{v['top_prim']} of the {v['top_n']} results it retrieved are makers, official bodies or major reviewers.")
    if r.get("our_rank"):
        out.append(f"Our page is already in the results at rank {r['our_rank']}" + (" and is cited." if r["tier"] >= 4 else ", not cited."))
    return " ".join(out)


def crop(src: Path, dst: Path) -> bool:
    if dst.exists():
        return True
    if not src.exists():
        return False
    h = int(subprocess.run(["sips", "-g", "pixelHeight", str(src)], capture_output=True, text=True).stdout.split()[-1])
    ch = max(200, min(h - 70, 1500))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-vf", f"crop=830:{ch}:620:60,scale=640:-1", "-q:v", "5", str(dst)])
    return dst.exists()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", default="2026-11-14-openq")
    args = ap.parse_args()
    run = ROOT / "growth" / "evals" / "runs" / args.run_id
    out = HERE / "report"
    (out / "shots").mkdir(parents=True, exist_ok=True)
    rows = []
    for f in sorted((run / "chatgpt").glob("*.json")):
        rec = json.loads(f.read_text())
        if rec.get("downgraded"):
            continue
        q = rec.get("queue") or {}
        s = VS.score(rec, {"code": None})
        r = {"qid": rec["qid"], "prompt": rec["prompt"], "group": q.get("group"), "shape": q.get("shape"), "source": q.get("source"),
             "evidence": q.get("evidence") or [], "use_case": q.get("use_case"), "volume": q.get("volume"), "tier": s["tier"], "our_rank": s["our_rank"],
             "started_at": rec.get("started_at"), **O.reading(rec)}
        v = verdict(r)
        r.update(v, reason=reason(r, v))
        r["shot"] = f"shots/{r['qid'][:5]}.jpg" if crop(run / "chatgpt" / f"{r['qid']}.jpg", out / "shots" / f"{r['qid'][:5]}.jpg") else None
        rows.append(r)
    for r in rows:
        r["more"] = []       # repeat chats on the same question, in order
    byq = {r["qid"]: r for r in rows}
    # repeat chats: the second on every query that read open in the first run, the third on those the first two split on
    for run_id, suffix, name in (("2026-11-15-openq-confirm", "b", "Second"), ("2026-11-15-openq-third", "c", "Third")):
        conf = ROOT / "growth" / "evals" / "runs" / run_id
        for f in sorted((conf / "chatgpt").glob("*.json")) if (conf / "chatgpt").exists() else []:
            rec = json.loads(f.read_text())
            if rec.get("downgraded") or rec["qid"] not in byq:
                continue
            s = VS.score(rec, {"code": None})
            r2 = {"qid": rec["qid"], "prompt": rec["prompt"], "tier": s["tier"], "our_rank": s["our_rank"], "started_at": rec.get("started_at"), **O.reading(rec)}
            v2 = verdict(r2)
            r2.update(v2, reason=reason(r2, v2), name=name)
            r2["shot"] = f"shots/{rec['qid'][:5]}{suffix}.jpg" if crop(conf / "chatgpt" / f"{rec['qid']}.jpg", out / "shots" / f"{rec['qid'][:5]}{suffix}.jpg") else None
            byq[rec["qid"]]["more"].append(r2)
    for r in rows:
        chats = [r] + r["more"]
        r["n_chats"], r["n_open"] = len(chats), sum(c["verdict"] == "open" for c in chats)
    (out / "readings.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    unknown = Counter(d for r in rows for d in r["cited"] + r["results"] if classify(d) == "small")
    (out / "small-domains.txt").write_text("\n".join(f"{n}\t{d}" for d, n in unknown.most_common()))
    vc = Counter(r["verdict"] for r in rows)
    print(len(rows), "answers;", dict(vc))
    (out / "open-queries.html").write_text(page(rows, vc))
    return 0


def kind(p: str) -> str:
    p = p.lower().strip()
    if re.search(r"\b(what should i (buy|get)|which|what (kind|type|size|battery|power|solar|setup|do i need)|recommend|best|easiest|smallest|lightest|quiet)", p):
        return "asks what to buy or which one"
    if re.match(r"(can|will|is|are|does|do|should)\b", p):
        return "yes/no (can it, is it, will it)"
    if re.match(r"how (long|many|much|big)", p):
        return "how long / how many / how much"
    if re.match(r"how (do|to|can)", p):
        return "how do I"
    return "other"


def esc(s) -> str:
    return html.escape(str(s or ""))


def card(r: dict) -> str:
    src = {"authored": "use case, written by Claude", "autocomplete": "typed into Google or Bing (autocomplete)",
           "forum": "asked on forums"}.get(r["source"] or "", r["source"] or "")
    if r.get("volume"):
        src = f"{r['volume']:,} Bing searches in 3 months"
    ev = "".join(f' <a href="{esc(u)}">[{i + 1}]</a>' for i, u in enumerate(r["evidence"][:3]))
    typed = ("<div class=\"small\">Typed by ChatGPT, no card: " + esc("; ".join(r["typed_names"][:5])) + "</div>") if r["typed_names"] else ""
    chips = f'<span class="tag web">{r["typed"]} typed</span> <span class="tag card">{r["carded"]} carded</span>'
    q = esc("; ".join(r["queries"][:2])) or "none"
    img = f'<a href="{r["shot"]}"><img src="{r["shot"]}" alt="ChatGPT answer to: {esc(r["prompt"])}" loading="lazy"></a>' if r["shot"] else ""
    sec = ""
    for s2 in r.get("more") or []:
        typed2 = (" Typed, no card: " + esc("; ".join(s2["typed_names"][:5])) + ".") if s2["typed_names"] else ""
        link2 = f' <a href="{s2["shot"]}">{s2["name"]} answer</a>' if s2["shot"] else ""
        sec += (f'<p><b>{s2["name"]} chat: {esc(s2["verdict"])}.</b> <span class="tag web">{s2["typed"]} typed</span> <span class="tag card">{s2["carded"]} carded</span> '
                f'{esc(s2["reason"])}{typed2}{link2}</p>')
    first = "<b>First chat: " + esc(r["verdict"]) + ".</b> " if r.get("more") else ""
    return (f'<article><h3>{esc(r["prompt"])}</h3><div class="chips">{chips} <span class="small">{esc(r["group"])} · {esc(src)}{ev}</span></div>'
            f'<p>{first}{esc(r["reason"])}</p>{typed}<div class="small">ChatGPT searched: {q}</div>{sec}{img}</article>')


RELATED = {   # our existing pages on the same need, for the landings column
    "ac030": ["solar-generator-with-panels-included", "best-solar-generator-kit-under-1000-for-home-backup", "best-solar-generator-for-power-outages"],
    "pm014": ["small-power-station-to-keep-wifi-router-and-modem-on-in-an-outage"], "pm022": ["1kwh-power-station-with-1000w-solar-input-two-ports"],
    "pm026": ["power-station-to-run-a-pellet-stove-in-an-outage"], "pq023": ["quietest-1000wh-power-station-while-charging"],
    "pq025": ["power-station-for-cpap"], "pr006": ["power-station-to-run-a-heated-blanket-all-night"],
    "pr008": ["1000wh-power-station-that-can-run-a-microwave"], "pm005": ["lightest-1000wh-lifepo4-power-station-for-car-camping"],
    "pn010": ["enclosed-3d-printer-multiple-filaments", "best-large-enclosed-3d-printer"]}


def demand_section(rows: list[dict]) -> str:
    f, g = HERE / "report" / "demand.json", HERE / "report" / "landings-by-page.json"
    if not f.exists():
        return ""
    dem, land = json.loads(f.read_text())["queries"], (json.loads(g.read_text()) if g.exists() else {})
    byq = {r["qid"][:5]: r for r in rows}
    trs = []
    for qid, d in sorted(dem.items(), key=lambda x: -x[1]["searches_13wk"]):
        r = byq.get(qid)
        best = max(d["keywords"], key=lambda k: k[1] or 0)
        kw = f'{esc(best[0])} ({best[1]:,})' if best[1] else "none above Bing's threshold"
        pages = RELATED.get(qid, [])
        ours = "; ".join(f'<a href="https://dealectric.com/{s}">{esc(s.replace("-", " "))}</a>: {land.get(s, 0)}' for s in pages) or "no page yet"
        trs.append(f'<tr><td>{esc(d["label"])}</td><td class=n>{r["n_open"]} of {r["n_chats"]}</td><td class=n>{d["searches_13wk"]:,}</td><td>{kw}</td><td>{ours}</td></tr>')
    total, kit = sum(land.values()), sum(n for s, n in land.items() if re.search(r"solar-generator|solar-kit|kit", s))
    return (f'<section><h2 class="prose">Demand for the 22</h2><p class="prose"><b>Only one of these topics shows real search volume.</b> "Solar generators for home use" had 5,096 Bing searches in 13 weeks; '
            f'CPAP battery searches add up to 439; the rest are below Bing\'s reporting threshold. Our own data points the same way: of {total} shopper landings from ChatGPT since 29 Oct, {kit} were on solar generator kit pages, '
            f'and our existing pages on the long-tail needs below have had almost none.</p>'
            f'<div class="wrap"><table><thead><tr><th>Topic</th><th class=n>Open in</th><th class=n>Bing searches, 13 weeks</th><th>Keyword with the most searches</th><th>Our page on this need: shopper landings from ChatGPT</th></tr></thead><tbody>{"".join(trs)}</tbody></table></div>'
            f'<p class="small prose" style="margin-top:8px">Bing counts are exact US searches for five short keywords per topic (Bing Webmaster Tools), and Bing is a small share of all search, so read them as relative size. Landings are human visits that arrived from a ChatGPT link (Worker log), 29 Oct to 15 Nov. Neither measures what people ask inside ChatGPT, which no source reports.</p></section>')


def strict_section() -> str:
    f = HERE / "report" / "strict-22.json"
    if not f.exists():
        return ""
    trs = []
    for d in json.loads(f.read_text()):
        reach = "no product rows" if d["reach"] is None else f'{d["reach"]:.0%}'
        trs.append(f'<tr><td>{esc(d["prompt"])}</td><td class=n>{reach}</td><td class=n>{d["cards"]}</td><td class=n>{d["sellers"]} of {d["clicked"]}</td></tr>')
    return ('<section class="prose"><h2>The 22, re-scored on catalog reach</h2>'
            '<p>Each of the 22 was asked once more and every typed product name was clicked. <b>Catalog reach</b> is the share of product rows where the shopper can get to a seller inside ChatGPT: '
            'rows with a card, plus typed rows whose panel showed a seller. In 4 of the 22 no row reached a seller; in 5 every row did.</p>'
            '<div class="wrap"><table><thead><tr><th>Question</th><th class=n>Catalog reach</th><th class=n>Cards</th><th class=n>Typed names with a seller</th></tr></thead><tbody>'
            + "".join(trs) + '</tbody></table></div>'
            '<p class="small" style="margin-top:8px">One chat per question, so read each row as a sample. A panel with no seller does not prove the product is outside the catalog: the same product showed a seller in one chat and none in another. '
            'The 66 demand-shortlist questions were scored the same way on <a href="https://claude.ai/artifact/GuNuAXm5mF9bhzbUzVXMc3">their own page</a>: 4 fully open, 25 partly, 15 closed.</p></section>')


def page(rows: list[dict], vc: Counter) -> str:
    opens = [r for r in rows if r["verdict"] == "open"]
    opens.sort(key=lambda r: (r["group"] != "solar", r["card_share"], r["prim_share"], -r["rows"]))
    adv = [r for r in rows if r["verdict"] == "advice, open"]
    rest = [r for r in rows if r["verdict"] not in ("open", "advice, open")]
    rest.sort(key=lambda r: r["verdict"])
    by = Counter((r["source"], r["verdict"] == "open") for r in rows)
    srcs = sorted({r["source"] for r in rows if r["source"]})
    src_rows = "".join(f"<tr><td>{esc(s)}</td><td class=n>{by[(s, True)] + by[(s, False)]}</td><td class=n>{by[(s, True)]}</td></tr>" for s in srcs)
    kinds = {}
    for r in rows:
        k = kinds.setdefault(kind(r["prompt"]), [0, 0, 0, 0])
        k[0] += 1; k[1] += r["searched"]; k[2] += r["rows"] > 0; k[3] += r["verdict"] == "open"
    kind_rows = "".join(f"<tr><td>{esc(k)}</td><td class=n>{v[0]}</td><td class=n>{v[1]}</td><td class=n>{v[2]}</td><td class=n>{v[3]}</td></tr>"
                        for k, v in sorted(kinds.items(), key=lambda x: -x[1][0]))
    rest_rows = "".join(f'<tr><td><a href="{r["shot"]}">{esc(r["prompt"])}</a></td><td>{esc(r["verdict"])}</td><td class=n>{r["carded"]}/{r["rows"]}</td>'
                        f'<td>{esc(", ".join(dict.fromkeys(r["cited_other"]))[:90])}</td></tr>' for r in rest)
    adv_rows = "".join(f'<tr><td><a href="{r["shot"]}">{esc(r["prompt"])}</a></td><td>{esc(", ".join(dict.fromkeys(r["cited_other"]))[:110]) or "none"}</td></tr>' for r in adv)
    n = len(rows)
    key = lambda r: (r["group"] != "solar", -r["n_open"] / r["n_chats"], sum(c["card_share"] for c in [r] + r["more"]) / r["n_chats"])
    rep = [r for r in rows if r["more"]]
    every = sorted([r for r in rep if r["n_open"] == r["n_chats"]], key=key)
    most = sorted([r for r in rep if r["n_chats"] >= 3 and r["n_open"] == 2], key=key)
    one = sorted([r for r in rep if r["n_open"] == 1], key=key)
    neither = [r for r in rep if r["n_open"] == 0]
    todo = sorted([r for r in opens if not r["more"]], key=key)
    grid = lambda rs: '<div class="grid">\n' + "\n".join(card(r) for r in rs) + "\n</div>"
    if rep:
        nb = sum(r["group"] == "solar" for r in every)
        lede = (f"<b>{len(every)} queries were open in every chat ({nb} for solar generators), and {len(most)} more in two chats of three.</b> "
                f"{len(one)} were open in one chat only, and {len(neither)} that first read as open did not hold up. {n} questions were asked in all.")
        note = "Solar generators first, then the other brands. The screenshot is the first answer; the later answers are linked in each card."
        sections = (f'<section><h2>Open in every chat ({len(every)})</h2><p class="small prose">{note}</p>{grid(every)}</section>'
                    + (f'<section><h2>Open in two chats of three ({len(most)})</h2><p class="small prose">The first two chats disagreed and the third came back open.</p>{grid(most)}</section>' if most else "")
                    + (f'<section><h2>Open in one chat only ({len(one)})</h2><p class="small prose">ChatGPT usually answers these with catalog cards or a maker\'s page. Not a target.</p>{grid(one)}</section>' if one else "")
                    + (f'<section><h2>Open, not yet asked again ({len(todo)})</h2>{grid(todo)}</section>' if todo else "")
                    + (f'<section class="prose"><h2>Did not hold up ({len(neither)})</h2><p class="small">Open on the first reading, then closed once the cited sources were checked and the question was asked again.</p><ul>'
                       + "".join(f'<li>{esc(r["prompt"])} <span class="small">({esc(", then ".join(c["verdict"] for c in [r] + r["more"]))})</span></li>' for r in neither) + "</ul></section>" if neither else ""))
    else:
        lede = f"<b>{len(opens)} of {n} questions asked are open:</b> ChatGPT searched the web, typed most of the product rows itself because its catalog had no card for them, and leaned on small sites instead of a maker, an official body or a major reviewer."
        sections = f'<section><h2>Open now</h2><p class="small prose">Solar generators first, then the other brands; within each, most open first.</p>{grid(opens)}</section>'
    return TEMPLATE.format(n=n, n_open=len(opens), lede=lede, sections=sections, demand=demand_section(rows), strict=strict_section(), n_adv=len(adv), n_cont=vc["contested"], n_closed=vc["closed"],
                           n_nosearch=vc["no search"], n_advsrc=vc["advice, sourced"],
                           notes=(HERE / "notes.html").read_text() if (HERE / "notes.html").exists() else "", src_rows=src_rows, kind_rows=kind_rows, rest_rows=rest_rows, adv_rows=adv_rows,
                           last=max((r["started_at"] or "") for r in rows)[:16].replace("T", " ") if rows else "")


TEMPLATE = """<title>Open Queries</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap">
<style>
/* Layout: summary column, then a two-column gallery of open queries, each with ChatGPT's answer as evidence. */
:root{{--bg:#f7f8f6;--surface:#fff;--fg:#1b211d;--muted:#5d665f;--line:#dde2dc;--web:#b86a00;--web-soft:#fbefd9;--card:#3a5f8a;--card-soft:#e4ecf5;--link:#1f6b4a;
--display:"Space Grotesk",system-ui,sans-serif;--body:"Inter",system-ui,sans-serif}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#141815;--surface:#1c211d;--fg:#e7ebe6;--muted:#9aa49c;--line:#2f3731;--web:#f0b04a;--web-soft:#3a2d12;--card:#8fb4de;--card-soft:#1d2c3d;--link:#7fd0a8;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#141815;--surface:#1c211d;--fg:#e7ebe6;--muted:#9aa49c;--line:#2f3731;--web:#f0b04a;--web-soft:#3a2d12;--card:#8fb4de;--card-soft:#1d2c3d;--link:#7fd0a8;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:36px 72px}}
main{{max-width:1080px;margin:0 auto;display:flex;flex-direction:column;gap:36px}}
.prose{{max-width:68ch}} h1{{font-family:var(--display);font-size:clamp(28px,5vw,38px);line-height:1.1;margin:0 0 12px}}
h2{{font-family:var(--display);font-size:22px;margin:0 0 10px}} h3{{font-size:16px;font-weight:600;margin:0;line-height:1.3;text-wrap:balance}}
p{{margin:0 0 10px}} a{{color:var(--link)}} .meta,.small{{color:var(--muted);font-size:13px}}
.tag{{display:inline-block;font-size:12px;font-weight:600;padding:1px 7px;border-radius:4px;white-space:nowrap}}
.tag.web{{background:var(--web-soft);color:var(--web)}} .tag.card{{background:var(--card-soft);color:var(--card)}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}}
article{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:16px;display:flex;flex-direction:column;gap:8px;min-width:0}}
article p{{font-size:14px;margin:0}} article img{{display:block;width:100%;border:1px solid var(--line);border-radius:4px;margin-top:6px;background:#fff}}
.chips{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
.wrap{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}}
th,td{{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}} td.n,th.n{{text-align:right;white-space:nowrap}}
.stats{{display:flex;flex-wrap:wrap;gap:8px 28px;margin:14px 0}} .stats div b{{font-family:var(--display);font-size:26px;display:block;line-height:1.1}}
@media (max-width:760px){{.grid{{grid-template-columns:1fr}}}}
</style>
<main>
<header class="prose">
<h1>Open queries</h1>
<div class="meta">Dealectric · ChatGPT answers read 14 to 15 Nov 2026, latest chat {last} UTC · discovery resumed on 15 Nov and is still running</div>
<p>{lede}</p>
<div class="stats"><div><b>{n}</b>asked</div><div><b>{n_open}</b>open on first reading</div><div><b>{n_adv}</b>advice only, weak sources</div><div><b>{n_cont}</b>contested</div><div><b>{n_closed}</b>closed</div><div><b>{n_nosearch}</b>no search</div></div>
{notes}
<p class="small">How each call is made, from one plain chat per question with search not forced: <b>open</b> means at most half of the product rows are catalog cards and at most a third of the cited sources are primary. <b>Contested</b> fails one test, <b>closed</b> fails both. <b>Advice only</b> answers name no product. <b>Carded and typed:</b> a carded row is ChatGPT's own shopping tile, filled from its product catalog with the price and a retailer button; a typed row is a product ChatGPT wrote out itself, with no tile and no retailer button, backed by the pages it cites. Both are real products on sale. Typed does not mean the product is missing from the catalog: the same product can come back as a card in another chat, which is why each query was asked more than once. These are rules of thumb from the top-versus-bottom analysis. Every question is in plain shopper wording; none names a model.</p>
</header>
<section><h2 class="prose">Typed row and carded row, side by side</h2>
<p class="prose small">Both rows are from one real answer, to "best solar generator kit under $500". They look alike; what differs is where the row's facts come from and where its link goes.</p>
<div class="grid">
<article><h3><span class="tag web">Typed</span> ChatGPT wrote this row itself</h3><img src="shots/x-typed.jpg" alt="A product row ChatGPT typed itself, with a source link to a web page">
<p>ChatGPT's catalog gave it nothing for this bundle in this answer, so it took the name and the price from a web page it had read. The link under the row, "Source: Kit comparison and offer", goes to that web page. Here the page is ours. This is the row a page can win.</p></article>
<article><h3><span class="tag card">Carded</span> filled from ChatGPT's catalog</h3><img src="shots/x-carded.jpg" alt="A product row filled from ChatGPT's shopping catalog, with a retailer link">
<p>The title, the price and the seller ("Sam's Club") come from ChatGPT's own product catalog, which retailers feed. The link, "View at retailer", goes straight to the retailer's listing. No web page is needed for this row, so no page gets the click.</p></article>
</div></section>
{strict}
{sections}
{demand}
<section class="prose"><h2>Advice answers with weak sources ({n_adv})</h2>
<p class="small">ChatGPT searched and cited small sites, but named no product. A page can win the citation here; whether it can sell is untested.</p>
<div class="wrap"><table><thead><tr><th>Question</th><th>Cited</th></tr></thead><tbody>{adv_rows}</tbody></table></div></section>
<section class="prose"><h2>Not open</h2>
<div class="wrap"><table><thead><tr><th>Question</th><th>Call</th><th class=n>Carded rows</th><th>Cited</th></tr></thead><tbody>{rest_rows}</tbody></table></div></section>
<section class="prose"><h2>What kind of question gets a search</h2>
<p class="small">ChatGPT decides for itself whether to search. A question it answers from memory cannot be won by any page, so this is the first gate.</p>
<div class="wrap"><table><thead><tr><th>Question form</th><th class=n>Asked</th><th class=n>Searched</th><th class=n>Named products</th><th class=n>Open</th></tr></thead><tbody>{kind_rows}</tbody></table></div></section>
<section class="prose"><h2>Where the questions came from</h2>
<div class="wrap"><table><thead><tr><th>Source</th><th class=n>Asked</th><th class=n>Open</th></tr></thead><tbody>{src_rows}</tbody></table></div></section>
</main>
"""

if __name__ == "__main__":
    sys.exit(main())
