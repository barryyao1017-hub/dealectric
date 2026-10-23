#!/usr/bin/env python3.12
"""Build the iteration report page for one loop iteration (growth/improvement-loop.md §5, step 7).

    python3.12 growth/evals/iterreport.py --iteration 1              # compares with iteration 0, latest run of each
    python3.12 growth/evals/iterreport.py --iteration 1 --prev 0 --run-id 2026-10-20

Writes growth/evals/loop/reports/iter-NN/index.html plus shots/*.jpg (the app screenshots ui.py saved next to the run
files, copied for publishing). The loop session then publishes the folder as the "Dealectric Loop · Iteration N"
artifact (index.html as the page, shots/ via `files`) and records the URL at the top of iter-NN.md.

Sections, in order: stamp · verdict (did the change work: pooled TLR before → after, decision rule, controls) · thesis
tested (from iter-NN.md "Diagnosis" and "Hypothesis") · the change · numbers (per assistant, api and ui) and failure
classes · shopper responses (screenshots when ui.py captured them, else the answer text) · new thesis and next run
(iter-NN.md "Decision" / "Next") · tokens and time · the rest of iter-NN.md.

iter-NN.md is read by its `##` headings; a heading is matched by keyword (hypothesis/thesis, diagnosis, change,
re-evaluation/outcome/numbers, decision/next). Anything else lands under "Notes".
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import statistics
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import report as RPT  # noqa: E402

REPORTS_DIR = E.LOOP_DIR / "reports"
MAX_SHOTS = 8          # screenshots shown as cards (all failures first, then L4 examples); every screenshot is copied and listed in the gallery
ALL_SHOTS: list[dict] = []
MAX_TEXT_CARDS = 4     # answer-text cards per assistant when there is no screenshot
H = html.escape


# ---------------------------------------------------------------- iter-NN.md

PHASE = 1   # set from --phase; phase 2 reads phase2-iter-NN.md and writes reports/phase2-iter-NN/


def iter_prefix() -> str:
    return "iter-" if PHASE == 1 else f"phase{PHASE}-iter-"


def read_iter_md(it: int) -> tuple[str, dict[str, list[str]]]:
    p = E.LOOP_DIR / f"{iter_prefix()}{it:02d}.md"
    if not p.exists():
        return f"Iteration {it}", {}
    title, sections, cur = f"Iteration {it}", {}, "_intro"
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            title = line[2:].strip(); continue
        if line.startswith("## "):
            cur = line[3:].strip(); sections[cur] = []; continue
        sections.setdefault(cur, []).append(line)
    return title, sections


def pick(sections: dict[str, list[str]], *keywords: str, exclude: tuple[str, ...] = ()) -> list[str]:
    """Headings (in file order) whose lowercase text contains any keyword and none of `exclude`."""
    out = []
    for h in sections:
        hl = h.lower()
        if any(k in hl for k in keywords) and not any(x in hl for x in exclude):
            out.append(h)
    return out


_INLINE = [(re.compile(r"`([^`]+)`"), lambda m: f"<code>{H(m.group(1))}</code>"),
           (re.compile(r"\*\*([^*]+)\*\*"), lambda m: f"<strong>{m.group(1)}</strong>"),
           (re.compile(r"_\(([^)]+)\)_"), lambda m: f"<em>({m.group(1)})</em>"),
           (re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)"), lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>')]


def inline(s: str) -> str:
    s = H(s)
    for rx, fn in _INLINE:
        s = rx.sub(fn, s)
    return s


def md_html(lines: list[str]) -> str:
    """Enough markdown for the iteration files: paragraphs, bullet lists, pipe tables, inline code/bold/links."""
    out, para, bullets, table = [], [], [], []

    def flush():
        nonlocal para, bullets, table
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if bullets:
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in bullets) + "</ul>"); bullets = []
        if table:
            rows = [r for r in table if not re.match(r"^\|?\s*:?-{2,}", r)]
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            if cells:
                head = "".join(f"<th>{inline(c)}</th>" for c in cells[0])
                body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:])
                out.append(f'<div class="scroll"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
            table = []

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush(); continue
        if line.lstrip().startswith("|"):
            if para or bullets:
                flush()
            table.append(line); continue
        if table:
            flush()
        m = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)", line)
        if m and not para:
            bullets.append(m.group(1)); continue
        if bullets and line.startswith("  "):
            bullets[-1] += " " + line.strip(); continue
        if bullets:
            flush()
        para.append(line.strip())
    flush()
    return "\n".join(out)


# ---------------------------------------------------------------- numbers

def load_iteration(it: int | None, run_id: str | None) -> dict | None:
    if it is None and not run_id:
        return None
    rid = run_id or (E.run_ids_for_iteration(str(it), PHASE) or [None])[-1]
    if not rid:
        return None
    rows, ui, manifest = RPT.load_run(rid)
    return {"run_id": rid, "rows": rows, "ui": ui, "manifest": manifest, "iteration": it}


def is_app(rows: list[dict], assistant: str) -> bool:
    return any(r.get("ui") for r in rows if r["assistant"] == assistant)


def pooled(d: dict, kind: str, metric: str = "tlr") -> tuple[int, int]:
    """kind 'ui': app rows in grades.jsonl plus the spot-check CSV rows; 'api': everything else.
    metric 'tlr' = L4 on the link tiers; 'cal' = code-and-link on tiers D+E (phase 2)."""
    tiers = E.CODE_TIERS if metric == "cal" else E.LINK_TIERS
    rows = [r for r in d["rows"] if r["kind"] == "question" and r["tier"] in tiers and not r.get("error")]
    hit = (lambda r: bool(r.get("code_and_link"))) if metric == "cal" else (lambda r: r["level"] == 4)
    if kind == "ui":
        k = sum(hit(r) for r in rows if r.get("ui")); n = sum(1 for r in rows if r.get("ui"))
        ku, nu = RPT.tlr_ui(d["ui"]) if metric == "tlr" else (0, 0)
        return k + ku, n + nu
    sel = [r for r in rows if not r.get("ui")]
    return sum(hit(r) for r in sel), len(sel)


def ci_text(k: int, n: int) -> str:
    if not n:
        return "–"
    p, lo, hi = E.wilson(k, n)
    return f"{p * 100:.0f}% <span class='ci'>[{lo * 100:.0f}–{hi * 100:.0f}]</span> ({k}/{n})"


def verdict(cur: dict, prev: dict | None) -> dict:
    out = {"api": pooled(cur, "api"), "ui": pooled(cur, "ui"), "rule": "baseline", "delta_api": None, "delta_ui": None,
           "cal_ui": pooled(cur, "ui", "cal"), "cal_api": pooled(cur, "api", "cal"), "delta_cal_ui": None, "delta_cal_api": None,
           "controls": controls(cur)}
    if prev:
        out["prev_api"], out["prev_ui"] = pooled(prev, "api"), pooled(prev, "ui")
        out["prev_cal_api"], out["prev_cal_ui"] = pooled(prev, "api", "cal"), pooled(prev, "ui", "cal")
        for key in ("api", "ui", "cal_api", "cal_ui"):
            k0, n0 = out["prev_" + key]; k1, n1 = out[key]
            out["delta_" + key] = (k1 / n1 - k0 / n0) * 100 if n0 and n1 else None
        # Phase 2's metric is the code-and-link rate ("cal"), so the verdict reads it; phase 1 reads the TLR. (Iteration 2.3
        # was flat on code-and-link but -7.5 on TLR, which the TLR rule called a drop although no change had been made.)
        first, second = ("cal_ui", "cal_api") if PHASE >= 2 else ("ui", "api")
        primary = out["delta_" + first] if out["delta_" + first] is not None else out["delta_" + second]
        secondary = out["delta_" + second] if out["delta_" + first] is not None else None
        if primary is None:
            out["rule"] = "no comparable reading"
        elif primary >= RPT.IMPROVEMENT_POINTS:
            out["rule"] = "improvement" + (" (api reading contradicts it)" if secondary is not None and secondary <= -RPT.IMPROVEMENT_POINTS else "")
        elif primary <= -RPT.IMPROVEMENT_POINTS:
            out["rule"] = "drop: revert first"
        else:
            out["rule"] = "flat (under the 5-point rule)"
    if out["controls"]["fail"]:
        out["rule"] += " · CONTROL FAILURE voids these numbers"
    return out


def controls(d: dict) -> dict:
    c = [r for r in d["rows"] if r["kind"] in ("positive", "negative") and not r.get("error")]
    return {"pass": sum(bool(r["control_pass"]) for r in c), "fail": sum(r["control_pass"] is False for r in c), "n": len(c)}


def per_assistant(d: dict) -> list[dict]:
    out = []
    assistants = [a for a in E.ASSISTANTS if any(r["assistant"] == a for r in d["rows"] + d["ui"])]
    for a in assistants:
        rows = [r for r in d["rows"] if r["assistant"] == a]
        R = RPT.rates(rows)
        app = is_app(rows, a)
        k, n = RPT.tlr(rows)
        ku, nu = RPT.tlr_ui(d["ui"], a)
        fails: dict[str, int] = {}
        for r in rows + [u for u in d["ui"] if u["assistant"] == a]:
            if r.get("kind", "question") == "question" and r.get("tier") in E.LINK_TIERS and r.get("failure_class"):
                fails[r["failure_class"]] = fails.get(r["failure_class"], 0) + 1
        wrong = sum(r.get("code_class") == "WRONG_CODE" for r in rows if r["kind"] == "question" and r["tier"] in E.CODE_TIERS)
        if wrong:
            fails["WRONG_CODE"] = wrong
        out.append({"assistant": a, "model": d["manifest"].get("models", {}).get(a, ""), "app": app,
                    "reading": "ui (app)" if app else ("ui (spot-check CSV only)" if not rows else "api"), "tlr": (k, n), "tlr_B": R["tlr_B"], "tlr_C": R["tlr_C"],
                    "tlr_D": R["tlr_D"], "tlr_E": R["tlr_E"], "cal_D": R["cal_D"], "cal_E": R["cal_E"], "code_D": R["code_D"], "code_E": R["code_E"],
                    "tlr_ui_csv": (ku, nu), "bypass": R["bypass"], "coupon": R["coupon_C"], "fails": fails})
    return out


# ---------------------------------------------------------------- cost and time

def usage_and_time(d: dict) -> dict:
    rdir = E.run_dir(d["run_id"])
    per: dict[str, dict] = {}
    for a, f in E.iter_run_files(d["run_id"]):
        rec = E.read_json(f)
        acc = per.setdefault(a, {"calls": 0, "latencies": [], "app": bool(rec.get("ui"))})
        acc["calls"] += 1
        if rec.get("latency_s"):
            acc["latencies"].append(float(rec["latency_s"]))
        if rec.get("usage"):
            E.add_usage(acc, rec["usage"])
            acc["calls"] -= 1  # add_usage counts the call too
    for acc in per.values():
        lat = acc.pop("latencies")
        acc["agent_hours"] = round(sum(lat) / 3600, 2)
        acc["median_s"] = round(statistics.median(lat), 1) if lat else None
    jp = rdir / "judge-usage.json"
    judge = E.read_json(jp) if jp.exists() else None
    m = d["manifest"]
    t0, t1 = RPT_parse(m.get("started_at")), RPT_parse(m.get("finished_at"))
    wall_h = round((t1 - t0).total_seconds() / 3600, 1) if t0 and t1 else None
    return {"per": per, "judge": judge, "wall_hours": wall_h, "started": m.get("started_at"), "finished": m.get("finished_at")}


def RPT_parse(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def pct(k: int, n: int) -> str:
    return RPT.pct(k, n) if n else "–"


def fmt_int(n) -> str:
    return f"{int(n):,}" if n not in (None, "") else "–"


# ---------------------------------------------------------------- shopper responses

def responses(d: dict, out_dir: Path) -> tuple[list[dict], list[dict]]:
    """(screenshot cards, text cards). Failures first, then L4 examples; app rows before api rows."""
    rdir = E.run_dir(d["run_id"])
    recs: dict[str, dict] = {}
    for a, f in E.iter_run_files(d["run_id"]):
        recs[str(f.relative_to(rdir))] = (f, E.read_json(f))
    rows = [r for r in d["rows"] if r["kind"] == "question" and r["tier"] in E.LINK_TIERS and not r.get("error")]
    rows.sort(key=lambda r: (not r.get("ui"), r["level"] == 4 and r.get("code_class") != "WRONG_CODE", r["assistant"], r["qid"], r["tier"], r["n"]))
    shots, texts, per_a = [], [], {}
    for r in rows:
        f, rec = recs.get(r["file"], (None, {}))
        code_note = ""
        if r["tier"] in E.CODE_TIERS or r.get("code_class") != "NO_CODE":
            code_note = {"RIGHT_CODE": "code " + ", ".join(r.get("codes_right") or []), "WRONG_CODE": "WRONG CODE " + ", ".join(r.get("codes_wrong") or []),
                         "NO_CODE": "no code"}.get(r.get("code_class") or "NO_CODE", "")
        card = {"assistant": r["assistant"], "qid": r["qid"], "tier": r["tier"], "n": r["n"], "level": r["level_label"] + (f" · {code_note}" if code_note else ""),
                "cls": r.get("failure_class") or ("WRONG_CODE" if r.get("code_class") == "WRONG_CODE" else None),
                "evidence": r.get("failure_evidence") or "", "prompt": r.get("prompt") or "",
                "link": (r.get("go_slugs") or r.get("page_slugs") or r.get("merchant_links") or r.get("network_links") or [""])[0],
                "quote": r.get("explanation") or "", "text": (rec.get("text") or "")[:700]}
        shot = rec.get("screenshot")
        if shot and f and (f.parent / shot).exists():
            # Every chat's screenshot (prompt + answer) is kept with the report (Barry, 2026-10-22); the page shows the
            # first MAX_SHOTS as cards and the rest in the gallery at the end.
            dst = out_dir / "shots" / f"{r['assistant']}-{shot}"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(f.parent / shot, dst)
            card["img"] = f"shots/{dst.name}"
            ALL_SHOTS.append(dict(card))
            if len(shots) < MAX_SHOTS and (r["level"] < 4 or len(shots) < MAX_SHOTS - 2):
                shots.append(card)
        elif card["text"] and per_a.get(r["assistant"], 0) < MAX_TEXT_CARDS and (r["level"] < 4 or per_a.get(r["assistant"], 0) < 2):
            per_a[r["assistant"]] = per_a.get(r["assistant"], 0) + 1
            texts.append(card)
    # spot-check CSV rows (manual browser checks) carry the shopper-facing link and the note; show the failures
    for u in d["ui"]:
        if u.get("tier") in E.LINK_TIERS and not u.get("l4_ui") and len(texts) < MAX_TEXT_CARDS * 3:
            texts.append({"assistant": u["assistant"], "qid": u["qid"], "tier": u["tier"], "n": "ui", "level": u.get("level_label", ""),
                          "cls": u.get("failure_class"), "evidence": u.get("failure_evidence") or "", "prompt": "",
                          "link": u.get("href") or u.get("link_text") or "", "quote": "", "text": u.get("notes") or ""})
    return shots, texts


# ---------------------------------------------------------------- page

CSS = """
:root { --bg:#F5F7F8; --fg:#1A232C; --muted:#5A6875; --line:#C6CFD6; --panel:#FFFFFF; --accent:#B5551B; --accent-soft:#F6E4D6;
  --go:#0E6F6E; --go-soft:#D9ECEA; --bad:#A33A2E; --bad-soft:#F6E0DC;
  --sans:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif; --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#111820; --fg:#E6ECF1; --muted:#98A6B4; --line:#34434F;
  --panel:#192230; --accent:#E8914A; --accent-soft:#3A2A1C; --go:#4FB8B4; --go-soft:#173534; --bad:#E07B6E; --bad-soft:#3A1F1B; color-scheme:dark } }
:root[data-theme="dark"] { --bg:#111820; --fg:#E6ECF1; --muted:#98A6B4; --line:#34434F; --panel:#192230; --accent:#E8914A;
  --accent-soft:#3A2A1C; --go:#4FB8B4; --go-soft:#173534; --bad:#E07B6E; --bad-soft:#3A1F1B; color-scheme:dark }
body { background:var(--bg); color:var(--fg); font:15px/1.55 var(--sans); margin:0 }
.wrap { max-width:960px; margin:0 auto; padding-block:28px 48px; padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)) }
h1 { font-size:26px; font-weight:600; margin:0 0 4px; letter-spacing:-0.01em; text-wrap:balance }
h2 { font-size:13px; text-transform:uppercase; letter-spacing:.09em; color:var(--muted); font-weight:600; margin:34px 0 10px; padding-top:14px; border-top:1px solid var(--line) }
h3 { font-size:15px; font-weight:600; margin:16px 0 6px }
p { margin:0 0 10px; max-width:78ch } ul { margin:0 0 10px; padding-left:20px } li { margin:2px 0 }
.stamp { color:var(--muted); font-size:13.5px; margin-bottom:18px } .stamp code { font-size:12px }
code { font-family:var(--mono); font-size:.9em; background:var(--accent-soft); padding:1px 5px; border-radius:3px }
.ci { color:var(--muted); font-size:.85em }
.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px; margin:0 0 6px }
.tile { background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:12px 14px; min-width:0 }
.tile .k { font-size:11.5px; text-transform:uppercase; letter-spacing:.07em; color:var(--muted) }
.tile .v { font-size:22px; font-weight:600; font-variant-numeric:tabular-nums; margin-top:2px }
.tile .d { font-size:13px; color:var(--muted) }
.verdict { display:inline-block; padding:3px 10px; border-radius:4px; font-weight:600; font-size:13px; background:var(--go-soft); color:var(--go) }
.verdict.bad { background:var(--bad-soft); color:var(--bad) } .verdict.flat { background:var(--accent-soft); color:var(--accent) }
.scroll { overflow-x:auto } table { border-collapse:collapse; width:100%; font-size:13.5px; margin:0 0 12px }
th,td { text-align:left; padding:6px 9px; border-bottom:1px solid var(--line); vertical-align:top; font-variant-numeric:tabular-nums }
th { color:var(--muted); font-weight:600; font-size:11.5px; text-transform:uppercase; letter-spacing:.06em; white-space:nowrap }
.cards { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:14px }
.card { background:var(--panel); border:1px solid var(--line); border-radius:6px; overflow:hidden; min-width:0; display:flex; flex-direction:column }
.card img { display:block; width:100%; max-height:420px; object-fit:cover; object-position:top; border-bottom:1px solid var(--line) }
.card .b { padding:10px 12px; font-size:13px } .card .h { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-bottom:6px }
.pill { font-family:var(--mono); font-size:11.5px; padding:1px 7px; border-radius:3px; background:var(--go-soft); color:var(--go) }
.pill.bad { background:var(--bad-soft); color:var(--bad) }
.who { color:var(--muted); font-size:12px } .q { font-style:italic; color:var(--muted); margin:4px 0 }
.txt { white-space:pre-wrap; font-size:12.5px; max-height:180px; overflow:auto; border-top:1px solid var(--line); padding-top:6px; margin-top:6px }
.link { font-family:var(--mono); font-size:11.5px; word-break:break-all; color:var(--muted) }
details { margin-top:10px } summary { cursor:pointer; color:var(--muted) }
.gallery { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:12px; margin-top:12px }
.gallery figure { margin:0; background:var(--panel); border:1px solid var(--line); border-radius:6px; overflow:hidden }
.gallery img { display:block; width:100%; max-height:300px; object-fit:cover; object-position:top }
.gallery figcaption { font-size:12px; padding:6px 8px; color:var(--muted) }
.empty { color:var(--muted); font-style:italic }
"""


def tile(k: str, v: str, d: str = "") -> str:
    return f'<div class="tile"><div class="k">{k}</div><div class="v">{v}</div><div class="d">{d}</div></div>'


def card_html(c: dict) -> str:
    ok = c["level"].startswith("L4")
    pill = f'<span class="pill{"" if ok else " bad"}">{H(c["cls"] or c["level"])}</span>'
    head = (f'<div class="h">{pill}<span class="who">{H(c["assistant"])} · {H(c["qid"])}-{H(c["tier"])}-{H(str(c["n"]))}</span></div>')
    body = ""
    if c.get("prompt"):
        body += f'<div class="q">{H(c["prompt"][:160])}</div>'
    if c.get("link"):
        body += f'<div class="link">→ {H(str(c["link"])[:140])}</div>'
    if c.get("quote"):
        body += f'<div class="q">“{H(c["quote"][:260])}”</div>'
    elif c.get("evidence") and not ok:
        body += f'<div class="q">{H(c["evidence"][:200])}</div>'
    img = f'<img src="{H(c["img"])}" alt="Screenshot of the {H(c["assistant"])} answer to {H(c["qid"])} tier {H(c["tier"])}">' if c.get("img") else ""
    txt = "" if c.get("img") else (f'<div class="txt">{H(c["text"])}</div>' if c.get("text") else "")
    return f'<div class="card">{img}<div class="b">{head}{body}{txt}</div></div>'


def section_md(title: str, sections: dict, heads: list[str], empty: str) -> str:
    parts = [f"<h2>{H(title)}</h2>"]
    if not heads:
        parts.append(f'<p class="empty">{H(empty)}</p>')
    for h in heads:
        if len(heads) > 1:
            parts.append(f"<h3>{inline(h)}</h3>")
        parts.append(md_html(sections[h]))
    return "\n".join(parts)


def build(it: int, cur: dict, prev: dict | None, out_dir: Path) -> Path:
    title, sections = read_iter_md(it)
    st = cur["manifest"].get("stamp") or {}
    v = verdict(cur, prev)
    pa = per_assistant(cur)
    cost = usage_and_time(cur)
    shots, texts = responses(cur, out_dir)
    loop = cur["manifest"].get("loop") or {}
    date = (cur["manifest"].get("started_at") or "")[:10]

    heads_thesis = pick(sections, "hypothesis", "thesis", exclude=("new thesis",)) or pick(sections, "diagnosis")
    heads_diag = [h for h in pick(sections, "diagnosis") if h not in heads_thesis]
    heads_change = pick(sections, "change", exclude=("next",))
    heads_outcome = pick(sections, "re-evaluation", "outcome", "numbers", "result", exclude=("design",))
    heads_design = pick(sections, "design")
    heads_next = [h for h in pick(sections, "decision", "next", "new thesis") if not h.lower().startswith("harness")]
    used = set(heads_thesis + heads_diag + heads_change + heads_outcome + heads_design + heads_next) | {"_intro"}
    heads_rest = [h for h in sections if h not in used]

    rule_cls = "bad" if "drop" in v["rule"] or "FAILURE" in v["rule"] else ("flat" if "flat" in v["rule"] or "baseline" in v["rule"] else "")
    tiles = []
    phase2 = PHASE >= 2 or v["cal_ui"][1] or v["cal_api"][1]
    if phase2:
        tiles.append(tile("Code-and-link, apps (ui), tiers D+E", ci_text(*v["cal_ui"]),
                          f"{v['delta_cal_ui']:+.1f} pts vs iteration {prev['iteration']}" if v.get("delta_cal_ui") is not None else ("the phase-2 metric" if v["cal_ui"][1] else "no app rows")))
    tiles.append(tile("Pooled TLR, apps (ui)", ci_text(*v["ui"]),
                      f"{v['delta_ui']:+.1f} pts vs iteration {prev['iteration']}" if v.get("delta_ui") is not None else ("primary reading" if v["ui"][1] else "no app rows")))
    tiles.append(tile("Pooled TLR, api", ci_text(*v["api"]),
                      f"{v['delta_api']:+.1f} pts vs iteration {prev['iteration']}" if v.get("delta_api") is not None else ("regression check" if v["api"][1] else "no api rows")))
    c = v["controls"]
    tiles.append(tile("Controls", f"{c['pass']}/{c['n']} pass", "a failure voids the numbers" if c["fail"] else "positive and negative"))
    tiles.append(tile("Decision rule", f'<span class="verdict {rule_cls}">{H(v["rule"])}</span>', "≥ 5 points pooled, ui not contradicting"))

    rows_html = []
    for a in pa:
        f = ", ".join(f"{k} {n}" for k, n in sorted(a["fails"].items(), key=lambda x: -x[1])) or "–"
        if phase2:
            rows_html.append(f"<tr><td>{H(a['assistant'])}<div class='who'>{H(a['model'])}</div></td><td>{H(a['reading'])}</td>"
                             f"<td>{ci_text(*a['tlr'])}</td><td>{pct(*a['tlr_B'])}</td><td>{pct(*a['tlr_D'])}</td><td>{pct(*a['tlr_E'])}</td>"
                             f"<td>{pct(*a['cal_D'])}</td><td>{pct(*a['cal_E'])}</td><td>{pct(*a['code_D'])}</td><td>{pct(*a['code_E'])}</td>"
                             f"<td>{pct(*a['bypass'])}</td><td>{H(f)}</td></tr>")
        else:
            rows_html.append(f"<tr><td>{H(a['assistant'])}<div class='who'>{H(a['model'])}</div></td><td>{H(a['reading'])}</td>"
                             f"<td>{ci_text(*a['tlr'])}</td><td>{pct(*a['tlr_B'])}</td><td>{pct(*a['tlr_C'])}</td>"
                             f"<td>{ci_text(*a['tlr_ui_csv']) if a['tlr_ui_csv'][1] else '–'}</td>"
                             f"<td>{pct(*a['bypass'])}</td><td>{pct(*a['coupon'])}</td><td>{H(f)}</td></tr>")
    if phase2:
        numbers = ('<div class="scroll"><table><thead><tr><th>assistant</th><th>reading</th><th>TLR B+D+E</th><th>TLR B</th><th>TLR D</th><th>TLR E</th>'
                   '<th>code+link D</th><th>code+link E</th><th>right code D</th><th>right code E</th><th>bypass</th><th>failure classes</th></tr></thead><tbody>'
                   + "".join(rows_html) + "</tbody></table></div>")
    else:
        numbers = ('<div class="scroll"><table><thead><tr><th>assistant</th><th>reading</th><th>TLR B+C</th><th>tier B</th><th>tier C</th>'
                   '<th>spot-check CSV</th><th>bypass</th><th>coupon (C)</th><th>failure classes</th></tr></thead><tbody>'
                   + "".join(rows_html) + "</tbody></table></div>")

    cost_rows = []
    for a, u in cost["per"].items():
        if u.get("app"):
            cost_rows.append(f"<tr><td>{H(a)}</td><td>{u['calls']}</td><td colspan='5' class='who'>consumer app, no token accounting</td>"
                             f"<td>{u['agent_hours']}</td><td>{u['median_s'] or '–'}</td></tr>")
        else:
            cost_rows.append(f"<tr><td>{H(a)}</td><td>{u['calls']}</td><td>{fmt_int(u.get('input_tokens'))}</td><td>{fmt_int(u.get('output_tokens'))}</td>"
                             f"<td>{fmt_int(u.get('cache_read_input_tokens'))}</td><td>{fmt_int(u.get('cache_creation_input_tokens'))}</td>"
                             f"<td>{('$%.2f' % u['total_cost_usd_list']) if u.get('total_cost_usd_list') else '–'}</td>"
                             f"<td>{u['agent_hours']}</td><td>{u['median_s'] or '–'}</td></tr>")
    j = cost["judge"]
    if j:
        cost_rows.append(f"<tr><td>LLM judge<div class='who'>{H(j.get('model', ''))} via {H(j.get('backend', ''))}</div></td><td>{j.get('calls', 0)}</td>"
                         f"<td>{fmt_int(j.get('input_tokens'))}</td><td>{fmt_int(j.get('output_tokens'))}</td><td>{fmt_int(j.get('cache_read_input_tokens'))}</td>"
                         f"<td>{fmt_int(j.get('cache_creation_input_tokens'))}</td><td>{('$%.2f' % j['total_cost_usd_list']) if j.get('total_cost_usd_list') else '–'}</td><td>–</td><td>–</td></tr>")
    else:
        cost_rows.append("<tr><td>LLM judge</td><td colspan='8' class='who'>no judge-usage.json for this run (recorded by grade.py from 2026-10-20 on)</td></tr>")
    cost_tbl = ('<div class="scroll"><table><thead><tr><th>assistant</th><th>calls</th><th>input</th><th>output</th><th>cache read</th>'
                '<th>cache write</th><th>list price</th><th>agent hours</th><th>median s</th></tr></thead><tbody>' + "".join(cost_rows) + "</tbody></table></div>")
    wall = f"{cost['wall_hours']} h wall clock ({H(cost['started'] or '?')} → {H(cost['finished'] or '?')})" if cost["wall_hours"] is not None else "wall clock unknown"

    subset = ", ".join(f"{x['id']}={x['primary']}{'' if x.get('fresh', True) else '*'}" for x in loop.get("questions", [])) if loop else "full question set"
    stamp = (f"Iteration {it} · {H(date)} · run <code>{H(cur['run_id'])}</code> · site commit <code>{H((st.get('site_commit') or '?')[:10])}</code> · "
             f"Worker <code>{H((st.get('worker_version') or '?')[:8])}</code>" + (f" deployed {H(st['worker_deployed_at'][:16])}Z" if st.get("worker_deployed_at") else "")
             + f" · assistants {H(', '.join(cur['manifest'].get('assistants', [])))} · tiers {H(', '.join(cur['manifest'].get('tiers', [])))}"
             + (f" · compared with iteration {prev['iteration']} (run <code>{H(prev['run_id'])}</code>)" if prev else " · baseline, nothing to compare")
             + f"<br>Subset: {H(subset)}")

    resp_html = []
    if shots:
        resp_html.append('<div class="cards">' + "".join(card_html(c) for c in shots) + "</div>")
    if texts:
        if shots:
            resp_html.append("<h3>Without a screenshot (answer text and spot-check notes)</h3>")
        else:
            resp_html.append('<p class="empty">No screenshots in this run (ui.py saves them from iteration 1 on); the answer text stands in.</p>')
        resp_html.append('<div class="cards">' + "".join(card_html(c) for c in texts) + "</div>")
    if not shots and not texts:
        resp_html.append('<p class="empty">No tier B or C answers in this run.</p>')
    rest = [c for c in ALL_SHOTS if c not in shots]
    if rest:
        rest.sort(key=lambda c: (c["qid"], c["tier"], str(c["n"])))
        gallery = "".join(
            f'<figure class="g"><a href="{H(c["img"])}"><img src="{H(c["img"])}" loading="lazy" alt="{H(c["assistant"])} {H(c["qid"])}-{H(c["tier"])}-{H(str(c["n"]))}"></a>'
            f'<figcaption><span class="pill{"" if c["level"].startswith("L4") and "WRONG" not in c["level"] else " bad"}">{H(c["cls"] or c["level"].split(" · ")[0])}</span> '
            f'{H(c["qid"])}-{H(c["tier"])}-{H(str(c["n"]))} · {H(c["level"])}</figcaption></figure>' for c in rest)
        resp_html.append(f'<details><summary>Every other chat of this run, prompt and answer ({len(rest)} screenshots)</summary><div class="gallery">{gallery}</div></details>')

    page = f"""<title>Dealectric Loop · {'Phase 2 · ' if PHASE >= 2 else ''}Iteration {it}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<div class="wrap">
<h1>{inline(title)}</h1>
<div class="stamp">{stamp}</div>

<h2>Did it work</h2>
<div class="tiles">{''.join(tiles)}</div>
{md_html(sections.get('_intro', [])) if sections.get('_intro') and any(l.strip() for l in sections['_intro']) else ''}

{section_md('Thesis tested', sections, heads_thesis, 'Baseline iteration: no change under test.')}
{section_md('Diagnosis it came from', sections, heads_diag, '') if heads_diag else ''}
{section_md('The change', sections, heads_change, 'No site change in this iteration.')}

<h2>Numbers</h2>
{numbers}
{section_md('Outcome, in the iteration file', sections, heads_outcome, '') if heads_outcome else ''}
{section_md('Run design', sections, heads_design, '') if heads_design else ''}

<h2>What the shopper saw</h2>
{''.join(resp_html)}

{section_md('New thesis and next run', sections, heads_next, 'Not written yet.')}

<h2>Tokens and time</h2>
<p>{wall}. Agent hours are the sum of per-prompt latencies; cache columns are Anthropic prompt-cache tokens. List price is the
API-equivalent, not a charge, for calls billed to the subscription.</p>
{cost_tbl}

{('<details><summary>Notes from the iteration file</summary>' + ''.join(f'<h3>{inline(h)}</h3>' + md_html(sections[h]) for h in heads_rest) + '</details>') if heads_rest else ''}
</div>
"""
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.html"
    out.write_text(page, encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--iteration", type=int, required=True)
    ap.add_argument("--prev", type=int, default=None, help="iteration to compare with (default: N-1 when it has a run)")
    ap.add_argument("--run-id", default=None, help="run id for this iteration (default: the latest run stamped with it)")
    ap.add_argument("--prev-run-id", default=None)
    ap.add_argument("--out", default=None, help="output folder (default growth/evals/loop/reports/iter-NN)")
    ap.add_argument("--phase", type=int, default=1, help="loop phase: 2 reads phase2-iter-NN.md, matches phase-2 run stamps and writes reports/phase2-iter-NN")
    args = ap.parse_args()
    global PHASE
    PHASE = args.phase

    cur = load_iteration(args.iteration, args.run_id)
    if not cur:
        raise SystemExit(f"no graded run for iteration {args.iteration}; run grade.py first")
    prev_it = args.prev if args.prev is not None else (args.iteration - 1 if args.iteration > 0 else None)
    prev = load_iteration(prev_it, args.prev_run_id) if prev_it is not None else None
    if prev_it is not None and not prev:
        print(f"no run for iteration {prev_it}; building without a comparison")
    out_dir = Path(args.out) if args.out else REPORTS_DIR / f"{iter_prefix()}{args.iteration:02d}"
    if out_dir.exists():
        shutil.rmtree(out_dir / "shots", ignore_errors=True)
    out = build(args.iteration, cur, prev, out_dir)
    shots = sorted((out_dir / "shots").glob("*.jpg")) if (out_dir / "shots").exists() else []
    print(f"wrote {out} ({out.stat().st_size // 1024} KB) and {len(shots)} screenshots")
    print("publish: Artifact file_path=" + str(out) + (" with files {" + ", ".join(f"'shots/{s.name}': '{s}'" for s in shots[:3]) + (", …}" if len(shots) > 3 else "}") if shots else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
