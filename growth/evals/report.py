#!/usr/bin/env python3.12
"""Turn grades.jsonl (+ grades-ui.jsonl) into results.csv and a markdown scorecard, or compare two iterations.

    python3.12 growth/evals/report.py                        # today's run -> results.csv + growth/probes/<run-id>-eval.md
    python3.12 growth/evals/report.py --run-id 2026-10-19
    python3.12 growth/evals/report.py --compare 0 1          # iterations (from manifest stamps) or run ids
    python3.12 growth/evals/report.py --compare 0 1 --out growth/evals/loop/compare-00-01.md

Rates per assistant (question cells only, controls excluded):
  tracked-link rate (TLR)  share of tier B+C answers at L4; L4-api from the API response, L4-ui from the UI CSV
  discovery     tier A runs at L2 or higher (dealectric.com cited without being named)
  retrieval     tier B runs at L3 or higher
  bypass        tier B+C runs with a merchant-site or awin1/tkqlhce link instead of /go/
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

CSV_COLUMNS = ["run_id", "iteration", "site_commit", "worker_version", "gsc_indexed", "bing_indexed", "assistant", "model",
               "qid", "kind", "tier", "n", "level", "level_label", "l4_api", "l4_evidence", "failure_class", "failure_evidence",
               "explanation", "explanation_verbatim", "brand_hits", "expected_hits", "product_hits", "dealectric_urls_shown",
               "page_slugs", "go_slugs", "go_unknown_slugs", "other_our_slugs", "bypass", "merchant_links", "network_links",
               "click_ids", "coupon_surfaced", "coupon_codes_found", "code_class", "codes_right", "codes_wrong", "codes_unknown",
               "code_and_link", "our_rank", "catalog_rank", "picks", "consulted_ours",
               "d1_fetched_slugs", "domains_shown", "n_shown_urls", "n_consulted_urls", "n_raw_citations", "control_pass",
               "stop_reason", "latency_s", "error", "judge_error", "queries", "primary", "expected", "prompt", "file"]
IMPROVEMENT_POINTS = 5.0


def pct(num: int, den: int) -> str:
    return "n/a" if den == 0 else f"{100 * num / den:.0f}% ({num}/{den})"


def ci(num: int, den: int) -> str:
    if den == 0:
        return "n/a"
    p, lo, hi = E.wilson(num, den)
    return f"{100 * p:.0f}% [{100 * lo:.0f}–{100 * hi:.0f}] ({num}/{den})"


def cell(v) -> str:
    if isinstance(v, list):
        return "; ".join(json.dumps(x, ensure_ascii=False) if isinstance(x, dict) else str(x) for x in v)
    return "" if v is None else str(v)


def load_run(run_id: str) -> tuple[list[dict], list[dict], dict]:
    rdir = E.run_dir(run_id)
    gp = rdir / "grades.jsonl"
    if not gp.exists():
        raise SystemExit(f"{gp} missing; run grade.py first")
    rows = [json.loads(l) for l in open(gp, encoding="utf-8") if l.strip()]
    up = rdir / "grades-ui.jsonl"
    ui = [json.loads(l) for l in open(up, encoding="utf-8") if l.strip()] if up.exists() else []
    manifest = E.read_json(rdir / "manifest.json") if (rdir / "manifest.json").exists() else {}
    return rows, ui, manifest


def tlr(rows: list[dict], assistant: str | None = None, tiers=E.LINK_TIERS) -> tuple[int, int]:
    r = [x for x in rows if x["kind"] == "question" and x["tier"] in tiers and not x.get("error")
         and (assistant is None or x["assistant"] == assistant)]
    return sum(x["level"] == 4 for x in r), len(r)


def code_and_link(rows: list[dict], assistant: str | None = None, tiers=E.CODE_TIERS) -> tuple[int, int]:
    """Phase 2: answers that carry the /go/ link of an expected product AND a code we publish for it."""
    r = [x for x in rows if x["kind"] == "question" and x["tier"] in tiers and not x.get("error")
         and (assistant is None or x["assistant"] == assistant)]
    return sum(bool(x.get("code_and_link")) for x in r), len(r)


def code_surfaced(rows: list[dict], assistant: str | None = None, tiers=E.CODE_TIERS) -> tuple[int, int]:
    r = [x for x in rows if x["kind"] == "question" and x["tier"] in tiers and not x.get("error")
         and (assistant is None or x["assistant"] == assistant)]
    return sum(x.get("code_class") == "RIGHT_CODE" for x in r), len(r)


def tlr_ui(ui: list[dict], assistant: str | None = None) -> tuple[int, int]:
    r = [x for x in ui if x.get("tier") in E.LINK_TIERS and (assistant is None or x["assistant"] == assistant)]
    return sum(bool(x["l4_ui"]) for x in r), len(r)


def tiers_present(rows: list[dict]) -> list[str]:
    return [t for t in ("A", "B", "C", "D", "E") if any(r["tier"] == t for r in rows)]


def rates(rows: list[dict]) -> dict:
    q = [r for r in rows if r["kind"] == "question" and not r["error"]]
    a = [r for r in q if r["tier"] == "A"]
    b = [r for r in q if r["tier"] == "B"]
    c = [r for r in q if r["tier"] == "C"]
    link = [r for r in q if r["tier"] in E.LINK_TIERS]
    ranks = [r["our_rank"] for r in a + b if r.get("our_rank")]
    out = {
        "tlr": tlr(rows), "tlr_B": (sum(r["level"] == 4 for r in b), len(b)), "tlr_C": (sum(r["level"] == 4 for r in c), len(c)),
        "discovery": (sum(r["level"] >= 2 for r in a), len(a)),
        "brand_named_A": (sum(r["level"] >= 1 for r in a), len(a)),
        "retrieval": (sum(r["level"] >= 3 for r in b), len(b)),
        "bypass": (sum(bool(r["bypass"]) for r in link), len(link)),
        "coupon_C": (sum(bool(r["coupon_surfaced"]) for r in c), len(c)),
        "consulted_not_cited_A": (sum(bool(r["consulted_ours"]) and r["level"] < 2 for r in a), len(a)),
        "rank_judged": len(ranks), "rank_top1": sum(x == 1 for x in ranks), "rank_top3": sum(x <= 3 for x in ranks),
        "errors": (sum(bool(r["error"]) for r in rows), len(rows)),
    }
    for t in ("B", "C", "D", "E"):   # per-tier tracked link, code shown, code-and-link (phase 2 reads D and E against B)
        tr = [r for r in q if r["tier"] == t]
        out[f"tlr_{t}"] = (sum(r["level"] == 4 for r in tr), len(tr))
        out[f"code_{t}"] = (sum(r.get("code_class") == "RIGHT_CODE" for r in tr), len(tr))
        out[f"wrong_code_{t}"] = (sum(r.get("code_class") == "WRONG_CODE" for r in tr), len(tr))
        out[f"cal_{t}"] = (sum(bool(r.get("code_and_link")) for r in tr), len(tr))
    out["cal"] = code_and_link(rows)
    return out


def failure_table(rows: list[dict], ui: list[dict], assistants: list[str]) -> list[str]:
    """assistant × class counts for tier B+C question answers that are not L4 (API), plus UI rows if any."""
    md = []
    api = [r for r in rows if r["kind"] == "question" and r["tier"] in E.LINK_TIERS and r.get("failure_class")]
    md.append("| class | " + " | ".join(assistants) + " | all |")
    md.append("|---|" + "---|" * (len(assistants) + 1))
    for cls in E.FAILURE_CLASSES:
        if cls == "PLAIN_TEXT":
            continue
        counts = [sum(r["failure_class"] == cls for r in api if r["assistant"] == a) for a in assistants]
        md.append(f"| {cls} | " + " | ".join(str(c) for c in counts) + f" | {sum(counts)} |")
    tot = [sum(r["assistant"] == a for r in api) for a in assistants]
    md.append("| **non-L4 answers (api)** | " + " | ".join(str(c) for c in tot) + f" | {sum(tot)} |")
    coded = [r for r in rows if r["kind"] == "question" and r["tier"] in E.CODE_TIERS and not r.get("error")]
    if coded:   # phase 2: the code dimension on tiers D/E, whatever the link level
        wrong = [sum(r.get("code_class") == "WRONG_CODE" for r in coded if r["assistant"] == a) for a in assistants]
        none_ = [sum(r.get("code_class") == "NO_CODE" for r in coded if r["assistant"] == a) for a in assistants]
        l4nocode = [sum(r["level"] == 4 and r.get("code_class") != "RIGHT_CODE" for r in coded if r["assistant"] == a) for a in assistants]
        md.append("| WRONG_CODE (tiers D+E, any level) | " + " | ".join(str(c) for c in wrong) + f" | {sum(wrong)} |")
        md.append("| NO_CODE (tiers D+E, any level) | " + " | ".join(str(c) for c in none_) + f" | {sum(none_)} |")
        md.append("| L4 link without the right code (D+E) | " + " | ".join(str(c) for c in l4nocode) + f" | {sum(l4nocode)} |")
    if ui:
        uif = [r for r in ui if r.get("failure_class")]
        for cls in E.FAILURE_CLASSES:
            counts = [sum(r["failure_class"] == cls for r in uif if r["assistant"] == a) for a in assistants]
            if sum(counts):
                md.append(f"| {cls} (ui) | " + " | ".join(str(c) for c in counts) + f" | {sum(counts)} |")
        tot = [sum(r["assistant"] == a for r in uif) for a in assistants]
        md.append("| **non-L4 answers (ui)** | " + " | ".join(str(c) for c in tot) + f" | {sum(tot)} |")
    return md


def explanation_samples(rows: list[dict], assistants: list[str], per_class: int = 2) -> list[str]:
    md = []
    for a in assistants:
        for cls in E.FAILURE_CLASSES:
            quotes = [r for r in rows if r["assistant"] == a and r.get("failure_class") == cls and r.get("explanation")]
            for r in quotes[:per_class]:
                mark = "" if r.get("explanation_verbatim") else " (not verbatim, treat with care)"
                md.append(f"- **{a} · {cls}** ({r['qid']}-{r['tier']}-{r['n']}): “{r['explanation'][:300]}”{mark}")
    return md


def stamp_line(manifest: dict) -> str:
    st = manifest.get("stamp") or {}
    parts = [f"iteration {st.get('iteration') if st.get('iteration') is not None else '–'}",
             f"site commit `{(st.get('site_commit') or '?')[:10]}`",
             f"Worker `{st.get('worker_version') or '?'}`" + (f" deployed {st['worker_deployed_at']}" if st.get("worker_deployed_at") else ""),
             f"GSC indexed {st.get('gsc_indexed') if st.get('gsc_indexed') is not None else '–'}",
             f"Bing indexed {st.get('bing_indexed') if st.get('bing_indexed') is not None else '–'}"]
    return "Stamp: " + " · ".join(parts) + "."


# ---------------------------------------------------------------- scorecard

def scorecard(args) -> int:
    rows, ui, manifest = load_run(args.run_id)
    rdir = E.run_dir(args.run_id)
    q = E.load_questions()
    qtext = {x["id"]: x["text"] for x in q["questions"]}
    for kind in ("positive", "negative"):
        for x in q.get("controls", {}).get(kind, []):
            qtext[x["id"]] = x["text"]

    csv_path = rdir / "results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["assistant"], r["qid"], r["tier"], r["n"])):
            w.writerow({k: cell(r.get(k)) for k in CSV_COLUMNS})

    assistants = [a for a in E.ASSISTANTS if any(r["assistant"] == a for r in rows)]
    by_a = {a: [r for r in rows if r["assistant"] == a] for a in assistants}
    R = {a: rates(by_a[a]) for a in assistants}
    skipped = manifest.get("skipped", {})
    models = manifest.get("models", {})
    loop = manifest.get("loop")

    md = [f"# Assistant-citation eval — {args.run_id}\n"]
    md.append(f"Run `{args.run_id}` from `growth/evals/` (questions v{q.get('version')}, {manifest.get('n', '?')} runs per cell, "
              f"tiers {', '.join(manifest.get('tiers', []))}" + (", **loop subset**" if loop else "")
              + (", **MOCK data, not real assistants**" if manifest.get("mock") else "") + "). "
              f"Window {manifest.get('started_at', '?')} → {manifest.get('finished_at', '?')} UTC. "
              f"Raw answers: `growth/evals/runs/{args.run_id}/<assistant>/`, per-run grades: `results.csv` next to them.\n")
    md.append(stamp_line(manifest) + "\n")
    md.append("Tiers: **A** the question verbatim · **B** \"Use dealectric.com to find … and give me Dealectric's buy link\" · "
              "**C** \"Open https://dealectric.com/<slug> and give me the verified price and the exact buy link\" · "
              "**D** \"Does dealectric.com have a working discount code for …? Give me the code and Dealectric's buy link\" · "
              "**E** \"Use dealectric.com to find the best current discount on …\". "
              "Ladder: L0 none · L1 our brand/product named · L2 dealectric.com cited · L3 our product page linked · "
              "L4 `/go/<slug>` linked. Levels use the links the shopper sees (inline citations + links in the answer). "
              "**Tracked-link rate (TLR)** = L4 on the tiers that name us (B, C, D, E); L4-api from the API response, L4-ui from the browser spot-check. "
              "**Code-and-link** (phase 2) = L4 and a code we publish for that product in the same answer.\n")
    if loop:
        md.append("Loop subset: " + ", ".join(f"{x['id']}={x['primary']}{'' if x['fresh'] else '*'}" for x in loop["questions"])
                  + " (* slug fetched by an assistant in the previous 7 days" + (f"; D1: {loop['d1_error']}" if loop.get("d1_error") else "") + ")\n")
    if skipped:
        md.append("Skipped: " + "; ".join(f"**{a}** ({why})" for a, why in skipped.items()) + "\n")
    if not assistants:
        md.append("No assistant produced run files, so there are no rates. Set API keys (see growth/evals/README.md) and re-run.\n")

    if assistants:
        md.append("## Tracked-link rate (the loop metric)\n")
        md.append("| reading | " + " | ".join(assistants) + " | pooled |")
        md.append("|---|" + "---|" * (len(assistants) + 1))
        present = [t for t in tiers_present(rows) if t in E.LINK_TIERS]
        md.append(f"| L4-api, tiers {'+'.join(present)} (Wilson 95%) | " + " | ".join(ci(*tlr(by_a[a])) for a in assistants) + f" | {ci(*tlr(rows))} |")
        for t in present:
            md.append(f"| L4-api, tier {t} | " + " | ".join(pct(*R[a][f'tlr_{t}']) for a in assistants) + " | "
                      + pct(sum(R[a][f"tlr_{t}"][0] for a in assistants), sum(R[a][f"tlr_{t}"][1] for a in assistants)) + " |")
        if any(t in E.CODE_TIERS for t in present):
            md.append(f"| **code-and-link**, tiers {'+'.join(t for t in present if t in E.CODE_TIERS)} (Wilson 95%) | "
                      + " | ".join(ci(*code_and_link(by_a[a])) for a in assistants) + f" | {ci(*code_and_link(rows))} |")
            for t in present:
                md.append(f"| code-and-link, tier {t} | " + " | ".join(pct(*R[a][f'cal_{t}']) for a in assistants) + " | "
                          + pct(sum(R[a][f"cal_{t}"][0] for a in assistants), sum(R[a][f"cal_{t}"][1] for a in assistants)) + " |")
            for t in present:
                md.append(f"| right code shown, tier {t} | " + " | ".join(pct(*R[a][f'code_{t}']) for a in assistants) + " | "
                          + pct(sum(R[a][f"code_{t}"][0] for a in assistants), sum(R[a][f"code_{t}"][1] for a in assistants)) + " |")
        if ui:
            md.append("| L4-ui, browser spot-check | " + " | ".join(ci(*tlr_ui(ui, a)) for a in assistants) + f" | {ci(*tlr_ui(ui))} |")
        else:
            md.append("| L4-ui | no UI CSV merged | " * 1 + " |" * len(assistants))
        md.append("")

        md.append("## Scorecard\n")
        md.append("| rate | " + " | ".join(f"{a} ({models.get(a, '?')})" for a in assistants) + " |")
        md.append("|---|" + "---|" * len(assistants))
        for key, label in [("discovery", "discovery (tier A, L2+)"), ("brand_named_A", "our brand named (tier A, L1+)"),
                           ("retrieval", "retrieval (tier B, L3+)"), ("tlr_C", "tracked link (tier C, L4)"),
                           ("bypass", "bypass (link tiers, merchant/network link, no /go/)"),
                           ("coupon_C", "coupon surfaced (tier C)"),
                           ("consulted_not_cited_A", "saw our site but did not cite it (tier A)"),
                           ("errors", "API errors (all cells)")]:
            md.append(f"| {label} | " + " | ".join(pct(*R[a][key]) for a in assistants) + " |")
        md.append("| our product rank among picks (A+B, judged) | " + " | ".join(
            f"top-1 {R[a]['rank_top1']}, top-3 {R[a]['rank_top3']} of {R[a]['rank_judged']} judged" for a in assistants) + " |")
        md.append("")

        md.append("## Failures (non-L4 answers on the link tiers, assistant × class)\n")
        md.extend(failure_table(rows, ui, assistants))
        md.append("")
        ex = explanation_samples(rows, assistants)
        if ex:
            md.append("In the assistants' own words (verbatim quotes extracted by the LLM pass):\n")
            md.extend(ex)
            md.append("")

        md.append("## Controls\n")
        md.append("Positive = the expected outside source (RTINGS, Anker, Wirecutter) is cited on tier A. "
                  "Negative = a product we do not list gets no Dealectric product page or /go/ link (tiers A and B). "
                  "A control failure invalidates the iteration's numbers.\n")
        md.append("| control | tier | " + " | ".join(assistants) + " |")
        md.append("|---|---|" + "---|" * len(assistants))
        for qid, tier in sorted({(r["qid"], r["tier"]) for r in rows if r["kind"] in ("positive", "negative")}):
            cells = []
            for a in assistants:
                rs = [r for r in by_a[a] if r["qid"] == qid and r["tier"] == tier and not r["error"]]
                passed = sum(bool(r["control_pass"]) for r in rs)
                cells.append("n/a" if not rs else f"{'PASS' if passed == len(rs) else 'FAIL'} {passed}/{len(rs)}")
            md.append(f"| {qid} {qtext.get(qid, '')} | {tier} | " + " | ".join(cells) + " |")
        md.append("")

        tp = tiers_present([r for r in rows if r["kind"] == "question"])
        md.append(f"## Per question (best level over the runs; {'/'.join(tp)})\n")
        md.append("| id | question | primary slug | " + " | ".join(assistants) + " |")
        md.append("|---|---|---|" + "---|" * len(assistants))
        qids_run = [x["id"] for x in q["questions"] if any(r["qid"] == x["id"] for r in rows)]
        for qid in qids_run:
            prim = next((r.get("primary") for r in rows if r["qid"] == qid and r["kind"] == "question"), "")
            cells = []
            for a in assistants:
                parts = []
                for t in tp:
                    rs = [r for r in by_a[a] if r["qid"] == qid and r["tier"] == t]
                    if not rs:
                        parts.append("–"); continue
                    best = max(r["level"] for r in rs)
                    flag = ("†" if any(r["bypass"] for r in rs) else "") + ("¢" if any(r.get("code_class") == "RIGHT_CODE" for r in rs) else "") \
                        + ("✗" if any(r.get("code_class") == "WRONG_CODE" for r in rs) else "") + ("!" if any(r["error"] for r in rs) else "")
                    parts.append(f"L{best}{flag}")
                cells.append("/".join(parts))
            md.append(f"| {qid} | {qtext.get(qid, '')} | {prim or ''} | " + " | ".join(cells) + " |")
        md.append("\n† bypass seen in at least one run · ¢ the right code surfaced · ✗ a wrong or invented code · ! an API error in at least one run\n")

        md.append("## Links the shopper got on tier C (what the buy link was)\n")
        md.append("| assistant | /go/ (expected) | /go/ other or unknown slug | merchant site | awin1/tkqlhce | nothing of ours |")
        md.append("|---|---|---|---|---|---|")
        for a in assistants:
            c = [r for r in by_a[a] if r["tier"] == "C" and r["kind"] == "question" and not r["error"]]
            md.append(f"| {a} | {sum(r['level'] == 4 for r in c)} | {sum(bool(r['other_our_slugs'] or r['go_unknown_slugs']) for r in c)} | "
                      f"{sum(bool(r['merchant_links']) for r in c)} | {sum(bool(r['network_links']) for r in c)} | {sum(r['level'] < 2 for r in c)} |")
        md.append("")

        if ui:
            md.append("## Browser spot-check rows (L4-ui)\n")
            md.append("| assistant | qid | tier | hyperlink? | link text | href | class |")
            md.append("|---|---|---|---|---|---|---|")
            for r in ui:
                md.append(f"| {r['assistant']} | {r['qid']} | {r['tier']} | {'yes' if r['href_found'] else 'no'} | "
                          f"{(r['link_text'] or '')[:40]} | {(r['href'] or '')[:80]} | {'L4' if r['l4_ui'] else r['failure_class']} |")
            md.append("")

        d1 = E.read_json(rdir / "d1-ai-fetch.json") if (rdir / "d1-ai-fetch.json").exists() else {}
        md.append("## /go/ fetches logged by the Worker during the run (D1 `clicks`, kind = ai_fetch)\n")
        if d1.get("note"):
            md.append(f"Not joined: {d1['note']}\n")
        else:
            md.append(f"Window {d1.get('window')}: {len(d1.get('rows', []))} rows. Stale-cache cutoff: {d1.get('stale_cutoff', 'n/a')}; "
                      f"stale click ids seen: {', '.join(d1.get('stale_click_ids', [])) or 'none'}.\n")
            for a, slugs in sorted(d1.get("by_assistant", {}).items()):
                md.append(f"- **{a}**: {', '.join(slugs) if slugs else '(none)'}")
            md.append("")
            matched = [r for r in rows if r.get("d1_fetched_slugs")]
            if matched:
                md.append("Runs with a matching fetch: " + ", ".join(
                    f"{r['assistant']} {r['qid']}-{r['tier']}-{r['n']} ({', '.join(r['d1_fetched_slugs'])})" for r in matched) + "\n")

        errs = [r for r in rows if r["error"]]
        if errs:
            md.append("## Errors\n")
            for r in errs[:40]:
                md.append(f"- {r['assistant']} {r['qid']}-{r['tier']}-{r['n']}: {str(r['error'])[:200]}")
            if len(errs) > 40:
                md.append(f"- … {len(errs) - 40} more in results.csv")
            md.append("")
        jerr = sorted({str(r["judge_error"]) for r in rows if r.get("judge_error")})
        if jerr:
            md.append("LLM-pass notes: " + "; ".join(jerr[:5]) + "\n")

    md.append("## Method notes\n")
    md.append("- API runs, fresh context per call, same system prompt for every assistant (see `questions.yaml`). "
              "US location set where the API allows it (OpenAI, Anthropic); Gemini and xAI have no location parameter.")
    md.append("- The browser spot-check (hrefs read from the DOM in the agent's Chrome) is a manual step whose CSV grade.py merges; "
              "see `growth/evals/README.md`. API answers and app answers can differ in link handling, which is why both readings exist.")
    if "claude-code" in assistants:
        md.append("- **claude-code** is Claude as an agent through the Claude Code CLI (`claude -p`, WebSearch + WebFetch tools, "
                  "claude.ai subscription login), not the Anthropic API: no citation annotations, so its levels come from the links "
                  "in the answer text; its fetches reach the Worker as Claude-User. It stands in for `anthropic` until an API key exists.")
    md.append("- Rank and the explanation quotes are the only LLM-judged fields (Anthropic API, or the claude CLI when there is no key); "
              "everything else is string and URL matching.")

    default_out = rdir / "scorecard.md" if manifest.get("mock") else E.PROBES_DIR / f"{args.run_id}-eval.md"
    out = Path(args.out) if args.out else default_out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {csv_path} ({len(rows)} rows) and {out}")
    return 0


# ---------------------------------------------------------------- comparison

def resolve_iteration(arg: str, phase: int | None = None) -> str:
    ids = E.run_ids_for_iteration(arg, phase)
    if not ids:
        raise SystemExit(f"no run found for iteration or run id '{arg}'")
    if len(ids) > 1:
        print(f"iteration {arg}: {len(ids)} runs, using the latest ({ids[-1]})")
    return ids[-1]


def compare(args) -> int:
    ra, rb = resolve_iteration(args.compare[0], args.phase), resolve_iteration(args.compare[1], args.phase)
    rows_a, ui_a, man_a = load_run(ra)
    rows_b, ui_b, man_b = load_run(rb)
    assistants = [a for a in E.ASSISTANTS if any(r["assistant"] == a for r in rows_a + rows_b)]
    it_a = (man_a.get("stamp") or {}).get("iteration", ra)
    it_b = (man_b.get("stamp") or {}).get("iteration", rb)

    def delta(ka, na, kb, nb):
        if not na or not nb:
            return None
        return 100 * (kb / nb - ka / na)

    md = [f"# Iteration comparison — {it_a} ({ra}) → {it_b} ({rb})\n"]
    md.append(f"- {it_a}: {stamp_line(man_a)}")
    md.append(f"- {it_b}: {stamp_line(man_b)}\n")
    tp = sorted({r["tier"] for r in rows_a + rows_b if r["kind"] == "question" and r["tier"] in E.LINK_TIERS})
    md.append(f"## Tracked-link rate, L4-api (tiers {'+'.join(tp)}, Wilson 95%)\n")
    md.append(f"| assistant | iteration {it_a} | iteration {it_b} | delta (points) |")
    md.append("|---|---|---|---|")
    for a in assistants:
        ka, na = tlr(rows_a, a); kb, nb = tlr(rows_b, a)
        d = delta(ka, na, kb, nb)
        md.append(f"| {a} | {ci(ka, na)} | {ci(kb, nb)} | {'n/a' if d is None else f'{d:+.1f}'} |")
    ka, na = tlr(rows_a); kb, nb = tlr(rows_b)
    d_api = delta(ka, na, kb, nb)
    md.append(f"| **pooled** | {ci(ka, na)} | {ci(kb, nb)} | {'n/a' if d_api is None else f'**{d_api:+.1f}**'} |")
    for t in tp:
        ka_, na_ = tlr(rows_a, None, (t,)); kb_, nb_ = tlr(rows_b, None, (t,))
        d = delta(ka_, na_, kb_, nb_)
        md.append(f"| tier {t} (pooled) | {ci(ka_, na_)} | {ci(kb_, nb_)} | {'n/a' if d is None else f'{d:+.1f}'} |")
    md.append("")
    if any(t in E.CODE_TIERS for t in tp):
        md.append("## Code-and-link rate (phase 2: L4 and the right code in one answer)\n")
        md.append(f"| reading | iteration {it_a} | iteration {it_b} | delta (points) |")
        md.append("|---|---|---|---|")
        for a in assistants:
            ka_, na_ = code_and_link(rows_a, a); kb_, nb_ = code_and_link(rows_b, a)
            d = delta(ka_, na_, kb_, nb_)
            md.append(f"| {a}, tiers D+E | {ci(ka_, na_)} | {ci(kb_, nb_)} | {'n/a' if d is None else f'{d:+.1f}'} |")
        for t in tp:
            ka_, na_ = code_and_link(rows_a, None, (t,)); kb_, nb_ = code_and_link(rows_b, None, (t,))
            d = delta(ka_, na_, kb_, nb_)
            md.append(f"| pooled, tier {t} | {ci(ka_, na_)} | {ci(kb_, nb_)} | {'n/a' if d is None else f'{d:+.1f}'} |")
        for t in tp:
            ka_, na_ = code_surfaced(rows_a, None, (t,)); kb_, nb_ = code_surfaced(rows_b, None, (t,))
            d = delta(ka_, na_, kb_, nb_)
            md.append(f"| right code shown, tier {t} | {ci(ka_, na_)} | {ci(kb_, nb_)} | {'n/a' if d is None else f'{d:+.1f}'} |")
        md.append("")

    d_ui = None
    if ui_a or ui_b:
        md.append("## Tracked-link rate, L4-ui (browser spot-check)\n")
        md.append(f"| assistant | iteration {it_a} | iteration {it_b} | delta (points) |")
        md.append("|---|---|---|---|")
        for a in assistants:
            ka_, na_ = tlr_ui(ui_a, a); kb_, nb_ = tlr_ui(ui_b, a)
            d = delta(ka_, na_, kb_, nb_)
            md.append(f"| {a} | {ci(ka_, na_)} | {ci(kb_, nb_)} | {'n/a' if d is None else f'{d:+.1f}'} |")
        ka_, na_ = tlr_ui(ui_a); kb_, nb_ = tlr_ui(ui_b)
        d_ui = delta(ka_, na_, kb_, nb_)
        md.append(f"| **pooled** | {ci(ka_, na_)} | {ci(kb_, nb_)} | {'n/a' if d_ui is None else f'**{d_ui:+.1f}**'} |")
        md.append("")

    md.append("## Decision rule\n")
    if d_api is None:
        verdict = "cannot apply: one side has no tier B+C question answers"
    elif d_api >= IMPROVEMENT_POINTS:
        if d_ui is not None and d_ui <= -IMPROVEMENT_POINTS:
            verdict = f"api +{d_api:.1f} points but ui {d_ui:+.1f}: **contradicted by the UI reading, not an improvement**"
        else:
            verdict = f"**improvement**: pooled L4-api {d_api:+.1f} points (≥ {IMPROVEMENT_POINTS:.0f})" + \
                      (f", ui {d_ui:+.1f} does not contradict" if d_ui is not None else ", no UI reading to check against")
    elif d_api <= -IMPROVEMENT_POINTS:
        verdict = f"**drop** of {abs(d_api):.1f} points: revert the change before anything else"
    else:
        verdict = f"flat ({d_api:+.1f} points, under the {IMPROVEMENT_POINTS:.0f}-point rule): keep the change only if it cost nothing elsewhere"
    md.append(verdict + "\n")
    _, lo_a, hi_a = E.wilson(ka, na) if na else (math.nan,) * 3
    _, lo_b, hi_b = E.wilson(kb, nb) if nb else (math.nan,) * 3
    if na and nb:
        overlap = not (hi_a < lo_b or hi_b < lo_a)
        md.append(f"Wilson intervals {'overlap' if overlap else 'do not overlap'} "
                  f"([{100*lo_a:.0f}–{100*hi_a:.0f}] vs [{100*lo_b:.0f}–{100*hi_b:.0f}]); "
                  f"with n={na} and n={nb} differences under ~{100*(hi_b-lo_b)/2:.0f} points are within noise.\n")

    ctrl_fail = [r for r in rows_b if r["kind"] in ("positive", "negative") and r["control_pass"] is False and not r["error"]]
    if ctrl_fail:
        md.append(f"**Controls failed in iteration {it_b}** ({len(ctrl_fail)} runs: "
                  + ", ".join(sorted({f"{r['assistant']} {r['qid']}-{r['tier']}" for r in ctrl_fail})) + "), which invalidates its numbers.\n")

    md.append(f"## Failures in iteration {it_b} (non-L4 answers on tiers {'+'.join(tp)})\n")
    md.extend(failure_table(rows_b, ui_b, assistants))
    md.append("")
    ex = explanation_samples(rows_b, assistants)
    if ex:
        md.append("In the assistants' own words:\n")
        md.extend(ex)
        md.append("")

    st_b = man_b.get("stamp") or {}
    per_a = ", ".join(f"{a} {100 * tlr(rows_b, a)[0] / tlr(rows_b, a)[1]:.0f}%" if tlr(rows_b, a)[1] else f"{a} n/a" for a in assistants)
    ui_pooled = f"{100 * tlr_ui(ui_b)[0] / tlr_ui(ui_b)[1]:.0f}%" if tlr_ui(ui_b)[1] else "–"
    md.append("## LOOP.md row for this iteration (fill in change and decision)\n")
    if any(t in E.CODE_TIERS for t in tp):
        def _p(fn, t):
            k, n = fn(rows_b, None, (t,)); return f"{100 * k / n:.0f}% ({k}/{n})" if n else "–"
        md.append("| iteration | date | commit | TLR B / D / E | code-and-link D / E | per-assistant TLR | change made | decision |")
        md.append("|---|---|---|---|---|---|---|---|")
        md.append(f"| 2.{it_b} | {(man_b.get('started_at') or '')[:10]} | {(st_b.get('site_commit') or '?')[:10]} | "
                  f"{_p(tlr, 'B')} / {_p(tlr, 'D')} / {_p(tlr, 'E')} | {_p(code_and_link, 'D')} / {_p(code_and_link, 'E')} | {per_a} | _change_ | _decision_ |")
    else:
        md.append("| iteration | date | commit | pooled TLR api | pooled TLR ui | per-assistant TLR | change made | decision |")
        md.append("|---|---|---|---|---|---|---|---|")
        md.append(f"| {it_b} | {(man_b.get('started_at') or '')[:10]} | {(st_b.get('site_commit') or '?')[:10]} | "
                  f"{100 * kb / nb:.0f}% ({kb}/{nb}) | {ui_pooled} | {per_a} | _change_ | _decision_ |")
    md.append("")

    text = "\n".join(md) + "\n"
    print(text)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-id", default=E.today())
    ap.add_argument("--out", default=None, help="scorecard path (default growth/probes/<run-id>-eval.md), or comparison path")
    ap.add_argument("--compare", nargs=2, metavar=("ITER_A", "ITER_B"), help="compare two iterations (numbers from manifest stamps, or run ids)")
    ap.add_argument("--phase", type=int, default=None, help="loop phase the iteration numbers belong to (phase-2 iterations restart at 0); '2:1' in --compare also works")
    args = ap.parse_args()
    return compare(args) if args.compare else scorecard(args)


if __name__ == "__main__":
    sys.exit(main())
