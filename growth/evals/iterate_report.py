#!/usr/bin/env python3.12
"""Report page for one iterate run: each round's starting page (screenshot), the drafts and their scores, the winning
change, and a recap of what ChatGPT's answers did (picks named, links handed over, what it linked instead).

    python3.12 growth/evals/iterate_report.py --target rv-2kwh --run rv-open-1

Writes <run>/report/index.html plus the round screenshots beside it; publish that folder as one artifact (the page
references round-NN.png). Rerun while the loop runs: an unfinished round is shown from its cached answers.
"""
from __future__ import annotations

import argparse, collections, difflib, glob, html, json, re, shutil
from pathlib import Path
from urllib.parse import urlparse

RUNS = Path(__file__).resolve().parents[2] / "growth" / "focus" / "fastloop-runs"
PICKS = ["AC200L", "C2000", "PowerStation 2000", "Elite 200", "Explorer 2000", "EcoFlow"]
H = html.escape


def rows_of(rdir: Path) -> dict[str, list[dict]]:
    """Answers per draft file (incumbent, v0..); side files kept for history (old host, gpt-6 only) are skipped."""
    out = {}
    for f in sorted(rdir.glob("*.jsonl")):
        if "-" in f.stem:
            continue
        out[f.stem] = [json.loads(x) for x in f.read_text().splitlines() if x.strip()]
    return out


def rate(rs: list[dict], k: str) -> float | None:
    lk = [r for r in rs if r["linked"]]
    return sum(r[k] for r in lk) / len(lk) if lk else None


def pct(x) -> str:
    return "–" if x is None else f"{x:.0%}"


def plain(a: str) -> str:
    a = re.sub(r"<[^>]+>", " ", a)
    a = re.sub(r"[#*|`]+", " ", a)
    return re.sub(r"\s+", " ", a).strip()


def first_sentence_diff(a: dict, b: dict) -> tuple[str, str]:
    """The changed stretch of the first field that differs, with ~60 characters of context, tags stripped."""
    for k in ("title", "h1", "intro", "after"):
        if a[k] != b[k]:
            sa, sb = plain(a[k]), plain(b[k])
            ops = [o for o in difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_opcodes() if o[0] != "equal"]
            i1, j1, i2, j2 = ops[0][1], ops[0][3], ops[-1][2], ops[-1][4]
            return (k, f"…{sa[max(0, i1 - 60):i2 + 60]}…"), (k, f"…{sb[max(0, j1 - 60):j2 + 60]}…")
    return ("", ""), ("", "")


def recap(all_rows: list[dict]) -> dict:
    lk = [r for r in all_rows if r["linked"]]
    miss = [r for r in lk if not r["m1"]]
    replay_only = [r for r in miss if all("workers.dev" in u or "/x/" in u for u in r["links"])]
    cited_no_go = [r for r in miss if r["m2"]]
    other = collections.Counter(urlparse(u).netloc.replace("www.", "") for r in miss for u in r["links"]
                                if "workers.dev" not in u and "dealectric.com" not in u)
    picks = collections.Counter(p for r in all_rows for p in PICKS if p in r["answer"][:1500])
    lead = collections.Counter()
    for r in all_rows:
        a = r["answer"][:1500]
        pos = {p: a.find(p) for p in PICKS if p in a}
        if pos:
            lead[min(pos, key=pos.get)] += 1
    return {"n": len(all_rows), "linked": len(lk), "hits": sum(r["m1"] for r in lk), "miss": len(miss),
            "replay_only": len(replay_only), "cited_no_go": len(cited_no_go), "other": other.most_common(6),
            "picks": picks.most_common(), "lead": lead.most_common(3),
            "models": collections.Counter(r.get("model") or "?" for r in all_rows).most_common()}


def sample(rows: list[dict], hit: bool) -> dict | None:
    for r in rows:
        if r["linked"] and r["m1"] == hit and len(plain(r["answer"])) > 200:
            return r
    return None


def build(target: str, run: str) -> Path:
    out = RUNS / target / "iterate" / run
    rep = out / "report"
    rep.mkdir(exist_ok=True)
    rounds = []
    for rdir in sorted(out.glob("round-[0-9][0-9]")):
        rn = int(rdir.name[-2:])
        if (rdir / "incumbent.png").exists():
            shutil.copy(rdir / "incumbent.png", rep / f"{rdir.name}.png")
        done = out / f"{rdir.name}.json"
        rows = rows_of(rdir)
        if done.exists():
            d = json.loads(done.read_text())
            drafts = [("base", "", d["incumbent"]["score"], "", rows.get("incumbent", []))]
            for i, v in enumerate(d["variants"]):
                drafts.append((v["dimension"], v["change"], v["score"], v["decision"], rows.get(f"v{i}", [])))
            win = next((v for v in d["variants"] if v["decision"].startswith("new base")), None)
            diff = first_sentence_diff(d["incumbent"]["record"], win["record"]) if win else None
        else:
            vs = json.loads((rdir / "variants.json").read_text()) if (rdir / "variants.json").exists() else []
            drafts = [("base", "", None, "", rows.get("incumbent", []))]
            for i, v in enumerate(vs):
                drafts.append((v["dimension"], v["change"], None, "scoring…", rows.get(f"v{i}", [])))
            win, diff = None, None
        rounds.append({"n": rn, "name": rdir.name, "done": done.exists(), "drafts": drafts, "win": win, "diff": diff,
                       "rows": [r for rs in rows.values() for r in rs]})
    log = (out / "log.md").read_text() if (out / "log.md").exists() else ""
    final = json.loads((out / "final" / "check.json").read_text()) if (out / "final" / "check.json").exists() else None
    (rep / "index.html").write_text(page(target, run, rounds, log, final))
    return rep


CSS = """
:root { --bg:#f6f7f8; --surface:#fff; --fg:#1b2228; --muted:#5d6a74; --line:#dde2e6; --mark:#e0242b; --win:#157347;
  --drop:#9a6b00; --t-win:#e3f3ea; --ins:#e3f3ea; --del:#fbe4e4; --sans:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"JetBrains Mono",ui-monospace,Menlo,monospace; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#12171b; --surface:#1a2126; --fg:#e6eaed;
  --muted:#97a3ad; --line:#2c353c; --mark:#ff4d52; --win:#4cc38a; --drop:#e0b44a; --t-win:#16301f; --ins:#16301f; --del:#3a1a1c; color-scheme:dark } }
:root[data-theme="dark"] { --bg:#12171b; --surface:#1a2126; --fg:#e6eaed; --muted:#97a3ad; --line:#2c353c; --mark:#ff4d52;
  --win:#4cc38a; --drop:#e0b44a; --t-win:#16301f; --ins:#16301f; --del:#3a1a1c; color-scheme:dark }
body { background:var(--bg); color:var(--fg); font:15px/1.55 var(--sans); }
.wrap { max-width:1120px; margin:0 auto; padding-block:28px 64px; padding-left:max(16px, env(safe-area-inset-left, 0px));
  padding-right:max(16px, env(safe-area-inset-right, 0px)); display:grid; gap:36px; }
h1 { font-size:28px; line-height:1.2; margin:0; text-wrap:balance; }
h2 { font-size:20px; margin:0; text-wrap:balance; }
h3 { font-size:13px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); margin:0; font-weight:600; }
p { margin:0; max-width:72ch; }
.muted { color:var(--muted); }
section { display:grid; gap:14px; }
.round { display:grid; grid-template-columns:minmax(0,300px) minmax(0,1fr); gap:20px; align-items:start;
  background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:18px; }
.round > * { min-width:0; }
.shot { display:block; width:100%; height:auto; border:1px solid var(--line); border-radius:4px; }
.side { display:grid; gap:12px; }
.tbl { overflow-x:auto; }
table { border-collapse:collapse; font-size:14px; width:100%; }
td, th { text-align:left; padding:6px 8px; border-bottom:1px solid var(--line); vertical-align:top; }
th { font-size:11px; color:var(--muted); font-weight:600; text-transform:uppercase; letter-spacing:.06em; }
td.n { font-family:var(--mono); font-variant-numeric:tabular-nums; white-space:nowrap; }
tr.win td { background:var(--t-win); }
.dec { font-size:12px; white-space:nowrap; }
.dec.w { color:var(--win); font-weight:600; } .dec.d { color:var(--drop); }
.chg { font-size:13px; color:var(--muted); }
.diff { display:grid; gap:6px; font-size:14px; }
.diff div { padding:8px 10px; border-radius:4px; }
.diff .b { background:var(--del); } .diff .a { background:var(--ins); }
.diff b { font-size:11px; text-transform:uppercase; letter-spacing:.06em; margin-right:6px; }
.kpis { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:12px; }
.kpi { background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:12px 14px; display:grid; gap:2px; }
.kpi .v { font:600 24px/1.2 var(--mono); font-variant-numeric:tabular-nums; }
.kpi .l { font-size:13px; color:var(--muted); }
ul { margin:0; padding-left:20px; display:grid; gap:6px; max-width:80ch; }
blockquote { margin:0; padding:10px 14px; border-left:3px solid var(--line); background:var(--surface); font-size:14px; color:var(--muted); }
blockquote .tag { font:600 11px/1 var(--mono); text-transform:uppercase; letter-spacing:.06em; color:var(--fg); display:block; margin-bottom:6px; }
.pill { font:600 11px/1 var(--mono); padding:3px 6px; border-radius:3px; border:1px solid var(--line); color:var(--muted); }
@media (max-width:760px) { .round { grid-template-columns:1fr; } .round .shotbox { max-width:320px; } }
"""


def page(target: str, run: str, rounds: list[dict], log: str, final: dict | None) -> str:
    allr = [r for rd in rounds for r in rd["rows"]]
    rc = recap(allr)
    done = [rd for rd in rounds if rd["done"]]
    parts = [f'<title>RV Page Iterations</title><meta name="claude:viewport-fit-sides" content="cover">'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700&'
             'family=JetBrains+Mono:wght@400;600&display=swap">', f"<style>{CSS}</style><div class='wrap'>"]
    status = (f"Final check done." if final else
              f"{len(done)} round{'s' if len(done) != 1 else ''} finished"
              + (f", round {rounds[-1]['n']} running" if rounds and not rounds[-1]["done"] else "") + "; no final check yet.")
    parts.append(f"""<header style="display:grid;gap:10px"><h1>Iterating the RV 2kWh page on buy-link hand-over</h1>
<p class="muted">Page: <code>/best-2kwh-power-station-for-rv</code>. Run <code>{H(run)}</code>. Each round, Opus writes five
one-change variants of the current base; ChatGPT answers six recorded RV shopper searches with the draft inserted at rank 5
(the search results served as a page it opens). <b>M1</b> = share of linked answers that hand over our
<code>dealectric.com/go/</code> buy link; <b>M2</b> = share citing our page. The best variant by M1 becomes the next base.
Status: {H(status)}</p></header>""")

    # headline numbers
    path = []
    for rd in done:
        base = rd["drafts"][0][2]
        path.append(f"R{rd['n']} base {pct(base['m1'])}" + (f" → {pct(rd['win']['score']['m1'])}" if rd["win"] else ""))
    parts.append(f"""<section><h3>At a glance</h3><div class="kpis">
<div class="kpi"><span class="v">{len(rounds)}</span><span class="l">rounds started ({len(done)} finished)</span></div>
<div class="kpi"><span class="v">{rc['n']}</span><span class="l">ChatGPT answers recorded</span></div>
<div class="kpi"><span class="v">{rc['hits']}/{rc['linked']}</span><span class="l">linked answers that handed over our buy link</span></div>
<div class="kpi"><span class="v">{sum(1 for x in rc['lead'] if x[0] == 'AC200L') and dict(rc['lead']).get('AC200L', 0)}/{rc['n']}</span><span class="l">answers leading with our pick, the AC200L</span></div>
</div><p class="muted">Winner path: {H('; '.join(path)) or '–'}.</p></section>""")

    # rounds
    parts.append("<section><h2>Rounds</h2>")
    for rd in rounds:
        trs = []
        for name, chg, s, dec, rows in rd["drafts"]:
            if s:
                n, m1, m2 = s["answers"], s["m1"], s["m2"]
            else:
                n, m1, m2 = len(rows), rate(rows, "m1"), rate(rows, "m2")
            cls = "w" if dec.startswith("new base") else ("d" if dec.startswith("dropped") else "")
            trs.append(f"<tr class='{'win' if cls == 'w' else ''}'><td><b>{H(name)}</b><div class='chg'>{H(chg)}</div></td>"
                       f"<td class='n'>{n}</td><td class='n'>{pct(m1)}</td><td class='n'>{pct(m2)}</td>"
                       f"<td class='dec {cls}'>{H(dec)}</td></tr>")
        models = collections.Counter(r.get("model") or "?" for r in rd["rows"])
        mtxt = ", ".join(f"{m} {c}" for m, c in models.most_common())
        diff = ""
        if rd["diff"] and rd["diff"][0][1]:
            (k, b), (_, a) = rd["diff"]
            diff = (f"<div class='diff'><h3>Winning change ({H(k)})</h3><div class='b'><b>Before</b>{H(b)}</div>"
                    f"<div class='a'><b>After</b>{H(a)}</div></div>")
        elif rd["done"]:
            diff = "<p class='muted'>No variant beat the base; the base carries over.</p>"
        else:
            diff = "<p class='muted'>Round in progress: rates are raw shares of the answers so far (not yet standardized).</p>"
        img = (f"<a class='shotbox' href='{rd['name']}.png'><img class='shot' src='{rd['name']}.png' alt='Round {rd['n']} starting page'></a>"
               if (RUNS).exists() else "")
        parts.append(f"""<div class="round" id="r{rd['n']}"><div class="side">{img}
<span class="muted" style="font-size:13px">Round {rd['n']} starting page (full-page screenshot; open to zoom)</span></div>
<div class="side"><h2>Round {rd['n']} <span class="pill">{'finished' if rd['done'] else 'running'}</span></h2>
<p class="muted" style="font-size:13px">Answers by model: {H(mtxt)}.</p>
<div class="tbl"><table><thead><tr><th>Draft</th><th>Answers</th><th>M1</th><th>M2</th><th>Decision</th></tr></thead>
<tbody>{''.join(trs)}</tbody></table></div>{diff}</div></div>""")
    parts.append("</section>")

    # recap of ChatGPT's answers
    other = ", ".join(f"{d} ({c})" for d, c in rc["other"]) or "none"
    picks = ", ".join(f"{p} {c}" for p, c in rc["picks"])
    hit, miss = sample(allr, True), sample(allr, False)
    q = ""
    for tag, r in (("Handed over our link", hit), ("No buy link", miss)):
        if r:
            q += (f"<blockquote><span class='tag'>{tag} · {H(r.get('model') or '?')}</span>"
                  f"{H(plain(r['answer'])[:420])}…<br><span style='font-size:12px'>Links: "
                  f"{H(', '.join(u for u in r['links'] if 'workers.dev' not in u) or 'only the results page itself')}</span></blockquote>")
    parts.append(f"""<section><h2>What ChatGPT's answers did</h2><ul>
<li><b>It almost always picks our pick.</b> The AC200L led {dict(rc['lead']).get('AC200L', 0)} of {rc['n']} answers.
Products named in the opening of answers: {H(picks)}. The fight is not over the recommendation; it is over which link comes with it.</li>
<li><b>Most misses carry no buy link at all.</b> Of {rc['miss']} linked answers without our buy link, {rc['replay_only']} cited
only the search-results page it was given (a replay artifact: live ChatGPT cites the source pages), and {rc['cited_no_go']} cited our
page but linked the product by name or not at all.</li>
<li><b>Rival links in the misses are few:</b> {H(other)}. When a store link replaced ours it was usually BLUETTI's own store
(bluettipower.com), the pattern the card-test don't warns about.</li>
<li><b>Models differ.</b> Answers by model: {H(', '.join(f'{m} {c}' for m, c in rc['models']))}. gpt-6-mini hands over our link more
often than gpt-6, so rounds are compared within model (each draft's rate weighted to the round's mix).</li>
<li><b>Order mattered most so far.</b> Round 2's winner names the pick first and gives the reason after it ("Under $900, … is the
BLUETTI AC200L, because it has a built-in TT-30 outlet"). Changes to the closing section and bolded caveat lists lowered both
M1 and M2.</li>
<li><b>Nothing is significant yet.</b> Every winning gain so far sits inside the noise margin (21 points in round 1, 32 in round 2),
so no lesson has entered the knowledge base. The one noise test is the final check: the final base against the published page.</li>
</ul>{q}</section>""")

    if final:
        p, f = final["published"], final["final"]
        parts.append(f"""<section><h2>Final check</h2><p>Published page M1 {pct(p['m1'])} / M2 {pct(p['m2'])}; final base M1
{pct(f['m1'])} / M2 {pct(f['m2'])}; margin {pct(final['margin'])}: {'beats the published page by more than noise' if final['beats_published'] else 'not beyond noise'}.
Next: a live check with search on and Barry's OK before shipping.</p></section>""")

    notes = [ln for ln in log.splitlines() if re.match(r"^(Rule change|Replay host|Model|Outage|Robustness)", ln)]
    parts.append("<section><h2>Changes to the method along the way</h2><ul>"
                 + "".join(f"<li>{H(n)}</li>" for n in notes)
                 + "<li>Round 1 ran on the old replay host (dealectric.com/x); the same base scored 71% there and 25% on the neutral host, "
                   "so round 1's numbers run high and are not comparable with later rounds.</li></ul></section>")
    parts.append("</div>")
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="rv-2kwh")
    ap.add_argument("--run", default="rv-open-1")
    a = ap.parse_args()
    print(build(a.target, a.run))


if __name__ == "__main__":
    main()
