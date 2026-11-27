#!/usr/bin/env python3.12
"""Page flow, the routine (DLC-369; growth/pageflow/README.md): one run reads the signals, refreshes the maps that are
due, gates their lines, builds the best few and reports. A run in which no line passes the gates builds nothing.

    python3.12 tools/pageflow/run.py daily [--pages 3] [--clusters 1] [--cluster <id>] [--publish] [--no-chats]
    python3.12 tools/pageflow/run.py sense [--clusters 1] [--cluster <id>]     # ledger, due maps, gates; builds nothing
    python3.12 tools/pageflow/run.py build <run> [--pages 3] [--cluster <id>] [--publish]
    python3.12 tools/pageflow/run.py publish <run>
    python3.12 tools/pageflow/run.py report [<run>]

  sense    1. ledger: every page's cluster, type, line and shopper traffic (what worked, what did not);
           2. for each cluster that is due (no map, or a map older than maps.REFRESH_DAYS; at most --clusters a run,
              proven clusters first): the choices ChatGPT offers shoppers (ask.py, when older than ASK_DAYS), then the
              decision map (maps.py: reviews, releases, breakpoints, the field, our products' honest places);
           3. gates (propose.py): real, ours in the top three, uncovered, demand; scored by prior x demand x value.
  build    plan (the next --pages lines by score, 70/20/10 across proven / adjacent / new clusters) -> product records
           -> re-read of our own products (tools/upkeep) -> two plain ChatGPT chats per question -> harvest -> openness
           gate -> research (six angles, compose, verify) -> Amazon links -> apply (validation, pick check, fastloop
           check, build, local commit) -> close.
  publish  only with --publish, or when growth/pageflow/AUTOPUBLISH exists: merge main, rebuild, push, deploy the Worker
           when the link map changed, IndexNow for the new pages. Without it the run stops after research: drafts only.
  retire   the retire rule's states advance (retire.py); nothing is retired while growth/pageflow/RETIRE_ON is absent.
Each run appends one line to growth/pageflow/log.jsonl (the daily update reads it) and writes runs/<run>/report.md.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import ledger as L  # noqa: E402
import maps as M  # noqa: E402
import propose as P  # noqa: E402
import retire as R  # noqa: E402

ROOT = C.ROOT
ASK_DAYS = 30
HERE = Path(__file__).resolve().parent
LOG = C.DATA / "log.jsonl"
SWITCH = C.DATA / "AUTOPUBLISH"
TIER_ORDER = {"proven": 0, "adjacent": 1, "new": 2}


def say(*a) -> None:
    print(f"[pageflow {time.strftime('%H:%M:%S')}]", *a, flush=True)


def sh(*cmd, timeout: int | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(list(cmd), cwd=ROOT, capture_output=True, text=True, timeout=timeout)


def step(name: str, *args, timeout: int | None = None) -> tuple[int, str]:
    """One driver step as its own process (each step re-reads the run's files, so a crash loses that step only)."""
    say(name, *args)
    r = sh("python3.12", str(HERE / "driver.py"), name, *args, timeout=timeout)
    tail = (r.stdout or "")[-3000:] + ((r.stderr or "")[-800:] if r.returncode else "")
    print(tail, flush=True)
    return r.returncode, tail


def due_clusters(limit: int, only: str | None) -> list[str]:
    if only:
        return [only]
    due = []
    for cid, c in C.clusters().items():
        m = C.jload(C.MAPS / f"{cid}.json")
        age = C.days_between(m["built"], C.today()) if m else 10 ** 6
        if age >= M.REFRESH_DAYS:
            due.append((TIER_ORDER.get(c.get("tier"), 3), -age, cid))
    return [cid for *_x, cid in sorted(due)][:limit]


def sense(n_clusters: int, only: str | None, chats: bool = True) -> dict:
    import ask
    out = {"refreshed": [], "errors": []}
    led = L.build()
    say(f"ledger: {len(led['pages'])} pages" + ("" if led["d1"] else f" (D1 not read: {led['errors']})"))
    for cid in due_clusters(n_clusters, only):
        o = C.jload(C.OPTIONS / f"{cid}.json")
        if chats and (not o or C.days_between(o["read"], C.today()) >= ASK_DAYS):
            say(f"{cid}: asking ChatGPT the broad questions")
            a = ask.run(cid)
            if a.get("status") == "error":
                out["errors"].append(f"{cid} ask: {a['reason']}")
        say(f"{cid}: building the decision map")
        m = M.build(cid, force=True)
        if m.get("status") == "error":
            out["errors"].append(f"{cid} map: {m['reason']}")
            continue
        items = P.gate(cid)
        q = [i for i in items if i["status"] == "queued"]
        out["refreshed"].append({"cluster": cid, "lines": len(m["lines"]), "queued": len(q),
                                 "failed": {k: sum(1 for i in items if i["status"] == "failed:" + k) for k in ("real", "ours", "uncovered", "demand")},
                                 "news": len(m.get("news", [])), "pages_to_fix": [p["page"] for p in m.get("pages_to_fix", [])]})
        say(f"{cid}: {len(m['lines'])} lines, {len(q)} queued")
    return out


def build(run: str, pages: int, cluster: str | None, publish: bool) -> dict:
    out = {"run": run}
    args = ["--n", str(pages)] + (["--cluster", cluster] if cluster else [])
    rc, tail = step("plan", run, *args)
    qs = (C.jload(C.RUNS / run / "questions.json") or {"questions": []})["questions"]
    out["planned"] = len(qs)
    if not qs:
        say("nothing queued: no page is built in this run")
        return out
    if publish and any(q["ptype"] == "product" for q in qs):   # new records first, so the pages researched next can use them
        step("products", run, timeout=3 * 3600)
    if publish:
        step("fresh", run, timeout=2 * 3600)   # our own prices and stock, re-read before any page is researched
    if any(q["ptype"] != "product" for q in qs):
        step("chats", run, timeout=3 * 3600)
        step("harvest", run)
        step("keep", run, timeout=1800)
        step("research", run, "--workers", "3", timeout=8 * 3600)
        step("links", run, timeout=2 * 3600)
    if publish:
        if any(q["ptype"] != "product" for q in qs):
            step("apply", run, timeout=4 * 3600)
        step("close", run)
        out.update(do_publish(run))
    else:
        say("drafts only (no --publish and no growth/pageflow/AUTOPUBLISH): research is saved, nothing is applied or pushed")
    return out


def commit_data(run: str) -> None:
    """The run's own records (maps, queue, ledger, chats, research folders): committed so the other checkouts see them."""
    sh("git", "add", "--", "growth/pageflow", "growth/focus/ab", "growth/evals/runs/fastloop")
    for d in ROOT.glob(f"growth/evals/runs/{run}-harvest"):
        sh("git", "add", "--", str(d))
    for d in ROOT.glob("growth/evals/runs/*-pageflow-ask-*"):
        sh("git", "add", "--", str(d))
    if sh("git", "diff", "--cached", "--quiet").returncode:
        sh("git", "commit", "-q", "-m", f"pageflow: run {run} (maps, queue, ledger, research)\n\nCo-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>\n")


def do_publish(run: str) -> dict:
    res = (C.jload(C.RUNS / run / "results.json") or {"results": []})["results"]
    pages = [p for r in res for p in r["pages"]]
    out = {"built": pages, "skipped": [{"question": r["question"], "why": r["why"]} for r in res if r["state"] in ("skipped", "failed")]}
    L.build()
    R.step()
    write_report(run)
    commit_data(run)
    if not pages and sh("git", "status", "-sb").stdout.count("ahead") == 0:
        return out
    before = sh("git", "rev-parse", "origin/main:worker/src/links-map.json").stdout.strip()
    r = sh("bash", str(HERE / "publish.sh"), timeout=3600)
    print((r.stdout or "")[-1200:], (r.stderr or "")[-400:], flush=True)
    out["pushed"] = r.returncode == 0
    if r.returncode:
        out["error"] = f"publish exit {r.returncode}"
        return out
    if sh("git", "rev-parse", "HEAD:worker/src/links-map.json").stdout.strip() != before:
        d = sh("bash", "worker/deploy.sh", timeout=900)
        out["worker"] = "deployed" if d.returncode == 0 else "deploy failed: " + (d.stderr or d.stdout)[-200:]
    extra = [p for r in res for p in r.get("new_records") or []]   # product pages a comparison page's research added
    out["new_records"] = extra
    urls = [f"https://dealectric.com/{p}" for p in dict.fromkeys(pages + extra)]
    if urls:
        live = False
        for _ in range(40):   # GitHub Pages takes a few minutes; IndexNow only once the page answers
            c = sh("curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-A", "dealectric-linkcheck-bot", urls[-1])
            if c.stdout.strip() == "200":
                live = True
                break
            time.sleep(30)
        out["live"] = live
        if live:
            i = sh("python3.12", "tools/indexnow.py", *urls)
            out["indexnow"] = (i.stdout or i.stderr).strip()[-120:]
    return out


def write_report(run: str) -> str:
    res = (C.jload(C.RUNS / run / "results.json") or {"results": []})["results"]
    q = (C.jload(C.QUEUE) or {"items": []})["items"]
    lines = [f"# Page flow run {run}", "", "| Line | Type | Result | Page or reason |", "|---|---|---|---|"]
    for r in res:
        what = ", ".join(f"[{p}](https://dealectric.com/{p})" for p in r["pages"]) or r["why"].replace("|", "/")
        lines.append(f"| {r['question']} | {r['ptype']} | {r['state']} | {what} |")
    lines += ["", f"Queue after the run: {sum(1 for i in q if i['status'] == 'queued')} queued, "
              + ", ".join(f"{sum(1 for i in q if i['status'].startswith(k))} {k}" for k in ("failed:real", "failed:ours", "failed:uncovered", "failed:demand", "skipped", "built")),
              "", R.report()]
    text = "\n".join(lines) + "\n"
    (C.RUNS / run).mkdir(parents=True, exist_ok=True)
    (C.RUNS / run / "report.md").write_text(text)
    return text


def summary() -> str:
    """The lines tools/dailyupdate.py prints: the last run, the queue, how the flow's pages read, the retire states."""
    rows = [json.loads(x) for x in LOG.read_text().splitlines() if x.strip()] if LOG.exists() else []
    led = C.jload(C.LEDGER) or {"pages": {}, "built": "?"}
    q = (C.jload(C.QUEUE) or {"items": []})["items"]
    flow = {s: p for s, p in led["pages"].items() if p.get("line")}
    old = [p for p in flow.values() if (p["age"] or 0) >= 14]
    out = []
    if rows:
        last = rows[-1]
        b = last.get("build") or {}
        built = ", ".join(f"/{p}" for p in b.get("built") or []) or "no page"
        out.append(f"  last run {last['run']} ({'published' if last.get('publish') else 'drafts only'}): {built}"
                   + (f"; skipped {len(b['skipped'])}" if b.get("skipped") else "") + (f"; {b['error']}" if b.get("error") else ""))
        for r in (last.get("sense") or {}).get("refreshed", []):
            out.append(f"  map refreshed: {r['cluster']} ({r['lines']} lines, {r['queued']} queued, {r['news']} news items)")
    else:
        out.append("  no run logged yet")
    out.append(f"  queue: {sum(1 for i in q if i['status'] == 'queued')} lines queued of {len(q)} gated; "
               f"maps: {len(list(C.MAPS.glob('*.json')))} of {len(C.clusters())} clusters")
    out.append(f"  pages built by the flow: {len(flow)}; of the {len(old)} that are 14+ days old, {sum(1 for p in old if p['v14'])} had a shopper "
               f"visit in their first 14 days (ledger {led['built']})")
    st = C.jload(R.STATE) or {"pages": {}}
    n = lambda s: sum(1 for v in st["pages"].values() if v.get("state") == s)   # noqa: E731
    out.append(f"  retire rule {'on' if R.SWITCH.exists() else 'off'}: {n('rework')} at zero awaiting a rework, {n('reworked')} reworked, {n('due')} due")
    return "\n".join(out)


def log(entry: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> int:
    a = sys.argv[1:]
    cmd = a[0] if a else "report"

    def opt(name, default=None):
        return a[a.index(name) + 1] if name in a else default
    cluster = opt("--cluster")
    publish = "--publish" in a or SWITCH.exists()
    if cmd == "sense":
        s = sense(int(opt("--clusters", 1)), cluster, "--no-chats" not in a)
        print(json.dumps(s, ensure_ascii=False, indent=1))
        return 0
    if cmd == "daily":
        run = f"{C.today()}-pf"
        entry = {"date": C.today(), "run": run, "publish": publish}
        entry["sense"] = sense(int(opt("--clusters", 1)), cluster, "--no-chats" not in a)
        entry["build"] = build(run, int(opt("--pages", 3)), cluster, publish)
        if not publish:
            L.build()
            R.step()
            write_report(run)
        q = (C.jload(C.QUEUE) or {"items": []})["items"]
        entry["queue"] = {"queued": sum(1 for i in q if i["status"] == "queued"), "total": len(q)}
        log(entry)
        say("done:", json.dumps(entry["build"], ensure_ascii=False)[:600])
        return 0
    if cmd == "build":
        out = build(a[1], int(opt("--pages", 3)), cluster, publish)
        log({"date": C.today(), "run": a[1], "publish": publish, "build": out})
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    if cmd == "publish":
        step("close", a[1])
        out = do_publish(a[1])
        log({"date": C.today(), "run": a[1], "publish": True, "build": {"run": a[1], **out}})
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0 if out.get("pushed", True) else 2
    if cmd == "report":
        runs = sorted(p.name for p in C.RUNS.glob("*") if (p / "results.json").exists())
        print(write_report(a[1] if len(a) > 1 else runs[-1]) if (len(a) > 1 or runs) else R.report())
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
