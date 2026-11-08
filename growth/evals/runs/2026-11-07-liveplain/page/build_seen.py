"""Builds seen-not-cited.html: every plain-prompt chat (runs 2026-11-07-liveplain and -rest) where our target page was
in ChatGPT's search results, with the result list, the full answer and the saved screenshot when one exists.

Run from the repo root: python3 growth/evals/runs/2026-11-07-liveplain/page/build_seen.py
Screenshots are copied, shrunk, to page/shots/ and published with the artifact as supporting files."""
import datetime
import glob
import html
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

RUNS = Path("growth/evals/runs")
PAGE = RUNS / "2026-11-07-liveplain/page"
SHOTS = PAGE / "shots"
e = html.escape

ANNOTATED = [
    ('best-solar-generator-kit-under-1000-for-home-backup', 'Same template as the under-$500 page, ranked #1, not cited. ChatGPT searched for models it had already picked (EcoFlow DELTA 2, BLUETTI AC180, Jackery 1000 v2) and cited BLUETTI\'s own AC180 page and a price guide.'),
    ('best-solar-generator-kit-under-500', 'Ranked #5 and the only source cited. The other results were Black Friday deal posts and a 2021 list; ours was the one page that answered "kit under $500".'),
    ('best-nas-under-400-for-jellyfin', 'Ranked #1. ChatGPT recommended our pick (UGREEN DXP2800) but cited Jellyfin\'s docs, B&H\'s product page and a 2-bay NAS roundup.'),
    ('1000wh-power-station-that-can-run-a-microwave', 'Ranked #2. It searched four models\' spec sheets and cited two other comparison sites. Worth reading ours side by side with unpluggedwatts.com.'),
    ('quietest-1000wh-power-station-while-charging', 'Ranked #1 and cited with two other noise comparisons: one of several sources with measured numbers.'),
    ('lightest-1000wh-lifepo4-power-station-for-car-camping', 'Ranked #1 and cited with Jackery\'s FAQ and three comparison sites.'),
    ('power-station-to-run-a-gas-furnace-in-an-outage', 'A how-to question. Ranked #1; it cited a guide on the same topic and Reliance\'s transfer-switch install manual.'),
]


def norm(u):
    return (u or '').split('?')[0].split('#')[0].rstrip('/').replace('www.', '')


def load():
    """One record per chat (the saved run file), with the scan's verdict (last scan row per cell)."""
    scan = {}
    for f in sorted(RUNS.glob("2026-11-07-liveplain*/scan.jsonl")):
        for line in f.open():
            r = json.loads(line)
            scan[(f.parent.name, r["cell"])] = r
    chats = {}
    for f in sorted(RUNS.glob("2026-11-07-liveplain*/chatgpt/*.json")):
        c = json.loads(f.read_text())
        s = scan.get((f.parent.parent.name, f.stem))
        if not s:
            continue
        c["_tier"], c["_rank"], c["_run"] = s.get("tier", 0), s.get("our_rank"), f.parent.parent.name
        jpg = f.with_suffix(".jpg")
        c["_jpg"] = jpg if jpg.exists() else None
        chats[c["slug"]] = c          # one plain chat per page; the -rest run never repeats a slug
    return chats


def clean_markup(c):
    """ChatGPT's answer is a UI program: markdown plus JSX-like widgets. Keep the markdown, turn citations into a
    marker, widgets into their visible text, and drop images, charts and state code."""
    m = "\n\n".join(c["response"].get("markup") or [])
    if not m.strip():
        return None
    m = re.sub(r"\{@body[^\n]*\}\n?", "", m)
    m = re.sub(r"<svg.*?</svg>", "", m, flags=re.S)
    m = re.sub(r"<Chart[^>]*/>", "*[chart]*", m)
    m = re.sub(r"<Cite[^>]*/>", " ⟦cite⟧", m)
    m = re.sub(r'<Entity[^>]*value="([^"]+)"[^>]*/>', r"\1", m)
    m = re.sub(r"<Entity[^>]*/>", "[shopping-catalog product]", m)
    m = re.sub(r"<AsyncImage(Group)?[^>]*/>", "", m)
    m = re.sub(r'<Link[^>]*href="([^"]+)"[^>]*>(.*?)</Link>', r"[\2](\1)", m, flags=re.S)
    m = re.sub(r"\{turn\w+\.(\w+)\}", lambda x: f"[{x.group(1).replace('_', ' ')}]", m)
    m = re.sub(r"<radio [^>]*>", "◯ ", m)
    m = re.sub(r"</?[A-Za-z][\w-]*(\s[^<>]*?)?/?>", "", m)      # every other widget tag: keep its text
    m = re.sub(r"\{[^{}\n]*\}", "", m)                          # leftover JSX expressions
    lines, fence = [], False
    for line in m.splitlines():
        if line.strip().startswith("```"):
            fence = not fence
            lines.append(line.strip())
        elif fence:
            lines.append(line)                                  # code keeps its indentation
        elif "GenUI." in line or "DIL." in line or "=>" in line or re.search(r"\)\}>\s*$|^<\w", line.strip()):
            continue                                            # widget event handlers, not visible text
        else:
            lines.append(line.strip())
    m = "\n".join(lines)
    m = re.sub(r"\n{3,}", "\n\n", m).strip()
    return m


def shot(c):
    if not c["_jpg"]:
        return None
    SHOTS.mkdir(parents=True, exist_ok=True)
    out = SHOTS / (c["slug"][:60] + ".jpg")
    if not out.exists():
        subprocess.run(["sips", "-Z", "1600", "-s", "formatOptions", "70", str(c["_jpg"]), "--out", str(out)],
                       check=True, capture_output=True)
    return f"shots/{out.name}"


def section(c, note=None, collapsed=False):
    r = c["response"]
    s = c["slug"]
    cited = {norm(x.get("url")) for x in (c.get("citations") or []) + (c.get("cite_pills") or [])}
    cited |= {norm(u.get("url")) for u in r.get("markup_urls") or []}
    res = r.get("search_results") or []
    rows = []
    for i, x in enumerate(res, 1):
        u = x.get("url") or ""
        d = (x.get("domain") or urlparse(u).netloc).replace("www.", "")
        pd = datetime.datetime.fromtimestamp(x["pub_date"], datetime.UTC).strftime("%b %-d, %Y") if x.get("pub_date") else "—"
        rows.append(f'<tr class="{"ours" if "dealectric.com" in u else ""}"><td class="n">{i}</td><td class="dom">{e(d)}</td>'
                    f'<td class="t"><a href="{e(u)}" target="_blank" rel="noopener">{e((x.get("title") or u)[:140])}</a></td>'
                    f'<td class="d">{pd}</td><td class="c">{"<span class=cite>Cited</span>" if norm(u) in cited else ""}</td></tr>')
    extra = sorted(u for u in cited if u and not any(norm(x.get("url")) == u for x in res))
    hit = c["_tier"] >= 4
    model = c.get("answer_model") or "?"
    pills = c.get("cite_pills") or []
    md = clean_markup(c)
    sid = e(s[:48])
    img = shot(c)
    head = (f'<span class="pill {"hit" if hit else "miss"}">{"Cited" if hit else "Not cited"}</span>'
            f'<span class="rank">our rank #{c["_rank"]}</span><span class="rank">{e(model)}</span>')
    body = f'''<dl><dt>Typed</dt><dd class="q">{e(c["prompt"])}</dd><dt>ChatGPT searched</dt><dd class="q">{"<br>".join(e(q) for q in (c.get("queries") or []))}</dd></dl>
<div class="tw"><table><thead><tr><th>#</th><th>Site</th><th>Result</th><th>Dated</th><th></th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
{('<p class="extra">Also cited, from a later search or a page it opened: ' + ", ".join(e(u) for u in extra) + '</p>') if extra else ''}
<details class="answer"{" open" if not collapsed else ""}><summary>Full ChatGPT answer</summary>
{f'<figure><img src="{img}" alt="ChatGPT chat, first screen" loading="lazy"><figcaption>Saved screenshot: the first screen of the chat only (the capture stops at the window height).</figcaption></figure>' if img else ''}
<div class="md" data-md="{sid}">{e(c.get("text") or "")}</div>
{f'<script type="application/json" id="md-{sid}">{json.dumps(md).replace("</", "<\\/")}</script>' if md else ''}
{('<p class="extra">Sources linked in the answer (⟦cite⟧ marks where): ' + ", ".join(f'<a href="{e(p.get("url") or "")}" target="_blank" rel="noopener">{e(p.get("label") or urlparse(p.get("url") or "").netloc)}</a>' for p in pills) + '</p>') if pills else ''}
</details>'''
    link = f'<a href="https://dealectric.com/{e(s)}" target="_blank" rel="noopener">/{e(s)}</a>'
    if collapsed:
        return f'<details class="ex" id="{sid}"><summary><header>{head}</header><h2>/{e(s)}</h2></summary><p class="note">{link}</p>{body}</details>'
    return f'<section class="ex" id="{sid}"><header>{head}</header><h2>{link}</h2>{f"<p class=note>{e(note)}</p>" if note else ""}{body}</section>'


def main():
    chats = load()
    seen = [c for c in chats.values() if c["_rank"]]
    ann = {s for s, _ in ANNOTATED}
    miss = sorted((c for c in seen if c["_tier"] < 4 and c["slug"] not in ann), key=lambda c: (c["_rank"], c["slug"]))
    hits = sorted((c for c in seen if c["_tier"] >= 4 and c["slug"] not in ann), key=lambda c: (c["_rank"], c["slug"]))
    n_miss = sum(c["_tier"] < 4 for c in seen)
    secs_a = "".join(section(chats[s], note) for s, note in ANNOTATED)
    secs_m = "".join(section(c, collapsed=True) for c in miss)
    secs_h = "".join(section(c, collapsed=True) for c in hits)
    css = Path(PAGE / "seen.css").read_text()

    def cited_domains(c):
        ds = []
        for p in c.get("cite_pills") or []:
            d = urlparse(p.get("url") or "").netloc.replace("www.", "")
            if d and d not in ds:
                ds.append(d)
        return ", ".join(ds) or "nothing (no sources linked)"
    index_rows = "".join(
        f'<tr><td class="n">#{c["_rank"]}</td><td><a href="#{e(c["slug"][:48])}">/{e(c["slug"])}</a></td><td class="extra">{e(cited_domains(c))}</td></tr>'
        for c in sorted((c for c in seen if c["_tier"] < 4), key=lambda c: (c["_rank"], c["slug"])))
    page = f'''<meta charset="utf-8">
<title>Seen but Not Cited</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,600&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400&display=swap">
<style>{css}</style>
<div class="wrap">
<div><h1>Seen but not cited</h1><p class="lede">Every Dealectric gap page whose own page showed up in ChatGPT's search results, from one plain chat each on Nov 7, 2026: the page's target query typed as is into a fresh temporary chat (signed in, Plus), no instructions. {len(seen)} chats had our page in the results; ChatGPT cited it in {len(seen) - n_miss} and left it out in {n_miss}. Each table lists the results the app handed the model, in its order; our rows are tinted and "Cited" marks the sources the answer linked. Under each is ChatGPT's full answer, rebuilt from the saved chat (product cards and images left out). Screenshots exist only for chats that cited us (the scan deleted the rest), and each shows only the first screen; from the next run the scan keeps a full-length screenshot of every chat where our page is in the results.</p></div>
<div class="key"><h3>What stands out</h3><ol>
<li>ChatGPT often names the models it plans to recommend in its own search, then cites pages that back those models: often the maker's product page or docs.</li>
<li>We get cited when we hold the one fact the answer needs that no primary source has: a kit price under a cap, measured noise, weight per Wh across brands.</li>
<li>When a retailer, maker or documentation page has the same facts, the answer cites that page instead, even if ours ranks first and agrees with it (the Jellyfin NAS case).</li>
</ol></div>
<div class="key" id="index"><h3>All {n_miss} seen but not cited, best rank first</h3><div class="tw"><table><thead><tr><th>Rank</th><th>Our page</th><th>Cited instead</th></tr></thead><tbody>{index_rows}</tbody></table></div></div>
<nav class="toc"><a href="#annotated">Annotated examples (7)</a><a href="#all-miss">All other seen, not cited ({len(miss)})</a><a href="#all-hit">Cited, for contrast ({len(hits)})</a></nav>
<h3 class="band" id="annotated">Annotated examples</h3>
{secs_a}
<h3 class="band" id="all-miss">All other chats where our page was in the results and not cited · {len(miss)}, best rank first</h3>
{secs_m}
<h3 class="band" id="all-hit">Chats that cited us, for contrast · {len(hits)}</h3>
{secs_h}
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
<script>
(function(){{
  function openHash(){{ var t=location.hash && document.getElementById(location.hash.slice(1)); if(t && t.tagName==='DETAILS'){{ t.open=true; t.scrollIntoView(); }} }}
  window.addEventListener('hashchange', openHash); openHash();
  if(!window.marked) return;   // without the library each answer stays as the plain saved text
  document.querySelectorAll('.md[data-md]').forEach(function(el){{
    var s=document.getElementById('md-'+el.dataset.md); if(!s) return;
    try{{ el.innerHTML=marked.parse(JSON.parse(s.textContent)).replace(/⟦cite⟧/g,'<span class="cp">cite</span>'); el.classList.add('rendered'); }}catch(e){{}}
  }});
}})();
</script>'''
    (PAGE / "seen-not-cited.html").write_text(page)
    print(len(page), "chars;", len(seen), "seen;", n_miss, "not cited;", len(list(SHOTS.glob("*.jpg"))), "shots")


if __name__ == "__main__":
    main()
