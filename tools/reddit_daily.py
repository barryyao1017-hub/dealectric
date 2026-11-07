#!/usr/bin/env python3.12
"""Daily Reddit reply drafts for u/Dealectric_ (DLC-38). Claude drafts; Barry edits and posts.

Steps (the daily scheduled task runs them in order):
  quota                 how many drafts today and whether one may carry a link
  scan [--days 3]       fresh question threads in our subs, minus threads already in the log -> candidates.json
  read <id> [<id> ...]  full post + top comments + the sub's rules -> threads/<id>.json
  fill drafts.json      open one Agent Chrome tab per draft with the text in the reply box (never submits), log it

Reads Reddit only through the Agent Chrome (localhost:9222): plain HTTP gets 403/429 on the work network.
Rules: growth/outreach/reddit-brand-account.md. Log: growth/outreach/reddit-log.jsonl.
"""
import json, re, sys, time, datetime, pathlib, urllib.request
import websocket  # websocket-client

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "growth/outreach/reddit-daily"
LOG = ROOT / "growth/outreach/reddit-log.jsonl"
CDP = "http://localhost:9222"
START = datetime.date(2026, 11, 7)          # day 1 of the ramp (Barry 2026-11-07)
LINKS_PER = (2, 22)                         # at most 2 linked replies per 22, cumulative
SUBS = ("SolarDIY preppers homestead camping RVLiving overlanding bluetti Jackery anker UsbCHardware "
        "Generators OffGrid AskElectricians powerbanks CarCamping CPAP vandwellers homeowners").split()
NO_LINK = {"bluetti", "CPAP", "UsbCHardware", "preppers", "Jackery", "SolarDIY"}   # rules read 2026-11-06
SKIP = {"GoRVing"}                          # removes product recs from brand-related accounts
KW = re.compile(r"power station|generator|solar|batter(y|ies)|power ?bank|charger|charging|ecoflow|bluetti|jackery|"
                r"anker|backup|outage|\bwh\b|kwh|usb-?c|magsafe|qi2|inverter|lifepo|cpap|fridge|freezer|\bups\b", re.I)
ASK = re.compile(r"\?|recommend|which|should i|help|advice|looking for|best|worth|vs\.?|thoughts", re.I)


def tab(url="about:blank"):
    t = json.load(urllib.request.urlopen(urllib.request.Request(f"{CDP}/json/new?{url}", method="PUT")))
    return t, websocket.create_connection(t["webSocketDebuggerUrl"], suppress_origin=True)


def ev(ws, expr, _n=[0]):
    _n[0] += 1
    ws.send(json.dumps({"id": _n[0], "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}))
    while True:
        r = json.loads(ws.recv())
        if r.get("id") == _n[0]:
            return r["result"].get("result", {}).get("value")


def go(ws, url, wait=7):
    ev(ws, f"location.href={json.dumps(url)}")
    time.sleep(wait)


def close(t):
    urllib.request.urlopen(f"{CDP}/json/close/{t['id']}")


def log_rows():
    return [json.loads(l) for l in LOG.read_text().splitlines() if l.strip()] if LOG.exists() else []


def quota():
    day = (datetime.date.today() - START).days + 1
    n = 5 if day <= 7 else 10 if day <= 14 else 22
    rows = log_rows()
    total, linked = len(rows), sum(r.get("linked", False) for r in rows)
    may_link = (linked + 1) * LINKS_PER[1] <= (total + n) * LINKS_PER[0]
    today = sum(r["date"] == str(datetime.date.today()) for r in rows)
    q = {"day": day, "drafts_today": max(n - today, 0), "already_today": today, "logged_total": total,
         "linked_total": linked, "may_link_one_today": may_link}
    print(json.dumps(q, indent=1))
    return q


def scan(days=3):
    seen = {r["id"] for r in log_rows()}
    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H")
    js = ("[...document.querySelectorAll('#siteTable .thing.link')].map(t=>({t:t.querySelector('time')?.getAttribute('datetime'),"
          "title:t.querySelector('a.title')?.textContent,p:t.dataset.permalink,c:+t.dataset.commentsCount,"
          "locked:t.classList.contains('locked'),sticky:t.classList.contains('stickied')}))")
    t, ws = tab()
    out = []
    for s in SUBS:
        go(ws, f"https://old.reddit.com/r/{s}/new/", 6)
        for r in ev(ws, js) or []:
            if not r["t"] or r["t"] < cutoff or r["locked"] or r["sticky"] or not r["title"]:
                continue
            tid = r["p"].split("/comments/")[1].split("/")[0]
            if tid in seen or not KW.search(r["title"]) or not ASK.search(r["title"]):
                continue
            out.append({"id": tid, "sub": s, "title": r["title"], "comments": r["c"], "posted": r["t"],
                        "url": "https://old.reddit.com" + r["p"], "link_allowed_by_rules": s not in NO_LINK})
    close(t)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "candidates.json").write_text(json.dumps(out, indent=1))
    print(f"{len(out)} candidates -> {OUT/'candidates.json'}")
    for c in out:
        print(f"{c['id']} r/{c['sub']} c={c['comments']} | {c['title']}")


def read(ids):
    cands = {c["id"]: c for c in json.loads((OUT / "candidates.json").read_text())}
    (OUT / "threads").mkdir(parents=True, exist_ok=True)
    t, ws = tab()
    rules = {}
    for i in ids:
        c = cands[i]
        go(ws, c["url"])
        body = ev(ws, "(document.querySelector('#siteTable .usertext-body')?.innerText||'')")
        comments = ev(ws, "[...document.querySelectorAll('.commentarea .comment')].slice(0,25).map(c=>"
                          "(c.querySelector('.usertext-body')?.innerText||'').replace(/\\s+/g,' ').slice(0,400))")
        locked = ev(ws, "!!document.querySelector('.thing.link.locked')")
        if c["sub"] not in rules:
            go(ws, f"https://old.reddit.com/r/{c['sub']}/about/rules", 6)
            txt = ev(ws, "document.body.innerText") or ""
            k = txt.find("Rules for r/")
            rules[c["sub"]] = txt[k:k + 3000] if k >= 0 else "(rules not found)"
        rec = dict(c, body=body, comments_text=comments, locked=locked, rules=rules[c["sub"]])
        (OUT / "threads" / f"{i}.json").write_text(json.dumps(rec, indent=1))
        print(f"== {i} r/{c['sub']} locked={locked}\n{body[:1200]}\n-- comments --")
        print("\n".join("- " + x for x in comments[:15]))
    for s, r in rules.items():
        print(f"\n== RULES r/{s}\n{r[:1500]}")
    close(t)


def fill(path):
    drafts = json.loads(pathlib.Path(path).read_text())
    q = quota()
    linked = [d for d in drafts if d.get("linked")]
    if len(linked) > (1 if q["may_link_one_today"] else 0):
        sys.exit("refused: more linked drafts than the 2-per-22 budget allows today")
    for d in drafts:
        if d.get("linked") and d["sub"] in NO_LINK | SKIP:
            sys.exit(f"refused: r/{d['sub']} bans links")
        if not d.get("linked") and "dealectric.com" in d["text"]:
            sys.exit(f"refused: unlinked draft {d['id']} contains dealectric.com")
    with LOG.open("a") as f:
        for d in drafts:
            t = json.load(urllib.request.urlopen(urllib.request.Request(f"{CDP}/json/new?{d['url']}", method="PUT")))
            time.sleep(7)
            ws = websocket.create_connection(t["webSocketDebuggerUrl"], suppress_origin=True)
            res = ev(ws, "(()=>{const f=document.querySelector('.commentarea > form.usertext textarea');"
                         "if(!f)return 'NO REPLY BOX';f.focus();f.value=%s;f.dispatchEvent(new Event('input',{bubbles:true}));"
                         "f.scrollIntoView({block:'center'});return 'ok'})()" % json.dumps(d["text"]))
            ws.close()
            print(res, d["url"])
            if res == "ok":
                f.write(json.dumps({"date": str(datetime.date.today()), "id": d["id"], "sub": d["sub"], "url": d["url"],
                                    "linked": bool(d.get("linked")), "page": d.get("page"), "status": "tab_open"}) + "\n")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "quota":
        quota()
    elif cmd == "scan":
        scan(int(args[1]) if args[:1] == ["--days"] else 3)
    elif cmd == "read":
        read(args)
    elif cmd == "fill":
        fill(args[0])
    else:
        sys.exit(__doc__)
