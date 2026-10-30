#!/usr/bin/env python3.12
"""DLC-67 (W1 of growth/first-sale-plan.md): which products does ChatGPT already show Dealectric for?

    python3.12 growth/evals/visibility_scan.py --bank                 # (re)write growth/focus/questions.json, no chats
    python3.12 growth/evals/visibility_scan.py --run-id 2026-10-28-visibility --limit 60
    python3.12 growth/evals/visibility_scan.py --run-id 2026-10-28-visibility --retest   # n=2 for every T2+ question
    python3.12 growth/evals/visibility_scan.py --run-id 2026-10-28-visibility --report   # growth/focus/visibility.md

Four shopper phrasings per product, none naming Dealectric: a deal or code question, "worth buying, where to buy",
"best alternatives", and "best <category> under $<price>". Each runs once in a fresh temporary chat on chatgpt.com,
signed in (Barry's Free account, agent Chrome on port 9222, same driver as ui.py; it refuses to run logged out).

Every answer is scored on the plan's cascade: T5 a /go/ link, T4 a link or source pill to one of our pages, T3
Dealectric named (or our code relayed while our page was in the results), T2 our page in ChatGPT's search results
only, T1 absent. Per chat the summary line (runs/<run>/scan.jsonl) also keeps ChatGPT's queries, our rank in its
results, the model that answered and the cart dates the answer quotes.

Limit test (Barry, 2026-10-28): the run goes back to back and logs every throttle notice and every change of the
answering model to runs/<run>/events.jsonl. A Free plan drops to a smaller model after a quota without any error, so a
chat whose resolved_model_slug is not --model (gpt-6) counts as "downgraded": it is logged, the run sleeps
--cooldown seconds and asks the same question again until the original model is back. The events file is the
evidence for the scan's safe pace. Screenshots are kept only for T3 and up (about 200 KB each).
"""
from __future__ import annotations

import argparse, json, math, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ui  # noqa: E402
import evallib as E  # noqa: E402

ROOT = E.EVALS_DIR.parent.parent
BANK = ROOT / "growth" / "focus" / "questions.json"
OFFERS = ROOT / "docs" / "offers.json"

# Short name a shopper would type, and the category phrase for the "best ... under $X" question.
NAMES = {
    "baseus-blade-h1-100w-20000mah": ("Baseus Blade H1 power bank", "slim 100W laptop power bank"),
    "baseus-gan5-pro-65w-2c-u": ("Baseus GaN5 Pro 65W charger", "65W USB-C charger"),
    "baseus-nomos-5-in-1-140w-qi2": ("Baseus Nomos 5-in-1 charger", "desktop charging station with Qi2"),
    "baseus-picogo-am52-qi2-2-10000mah-45w": ("Baseus PicoGo AM52 power bank", "Qi2.2 magnetic power bank"),
    "baseus-usb-c-cable-100w": ("Baseus 100W USB-C cable", "100W USB-C to USB-C cable"),
    "baseus-enerfill-fc41-25000mah-145w": ("Baseus EnerFill FC41 power bank", "power bank with built-in cables"),
    "esr-cryoboost-3-in-1-qi2-2-25w-stand": ("ESR CryoBoost 3-in-1 Qi2.2 charging station", "3-in-1 iPhone charging station"),
    "esr-100w-6-in-1-magsafe-cryoboost-station": ("ESR 100W 6-in-1 MagSafe charging station", "MagSafe desk charging station"),
    "esr-halolock-15w-wireless-car-charger-cryoboost": ("ESR HaloLock 15W wireless car charger", "MagSafe car charger"),
    "esr-qi2-mini-wireless-charger-15w": ("ESR Qi2 Mini wireless charger", "Qi2 wireless charging pad"),
    "tenergy-tn480u-8-bay-nimh-charger": ("Tenergy TN480U 8-bay charger", "AA/AAA NiMH battery charger"),
    "tenergy-tn438-16-bay-nimh-charger": ("Tenergy TN438 16-bay charger", "16-bay AA/AAA battery charger"),
    "tenergy-premium-pro-aa-2800mah-20-pack": ("Tenergy Premium PRO AA 2800mAh batteries", "rechargeable AA batteries"),
    "tenergy-tn270-li-ion-18650-charger": ("Tenergy TN270 18650 charger", "18650 battery charger"),
    "tenergy-t320-300wh-power-station": ("Tenergy T320 power station", "300Wh portable power station"),
    "bluetti-elite-200-v2": ("BLUETTI Elite 200 V2", "2kWh portable power station"),
    "bluetti-ac200l": ("BLUETTI AC200L", "2kWh portable power station for an RV"),
    "bluetti-elite-30-v2": ("BLUETTI Elite 30 V2", "small portable power station for camping"),
    "bluetti-elite-300": ("BLUETTI Elite 300", "3kWh portable power station"),
    "bluetti-ac180": ("BLUETTI AC180", "1kWh portable power station"),
    "allpowers-p1800-1024wh": ("ALLPOWERS P1800", "1kWh portable power station"),
    "allpowers-r600-299wh": ("ALLPOWERS R600", "300Wh portable power station"),
    "allpowers-s2000-pro-1451wh": ("ALLPOWERS S2000 Pro", "1.5kWh portable power station"),
    "allpowers-r4000-3456wh": ("ALLPOWERS R4000", "home backup power station"),
    "allpowers-sp037-400w-solar-panel": ("ALLPOWERS SP037 400W solar panel", "400W portable solar panel"),
    "soundcore-liberty-4-pro": ("soundcore Liberty 4 Pro", "noise cancelling earbuds"),
    "soundcore-space-one-pro": ("soundcore Space One Pro", "noise cancelling headphones"),
    "soundcore-space-one": ("soundcore Space One", "noise cancelling headphones"),
    "soundcore-aerofit-2": ("soundcore AeroFit 2", "open-ear earbuds"),
    "soundcore-boom-2-plus": ("soundcore Boom 2 Plus", "outdoor party speaker"),
    "soundcore-motion-x600": ("soundcore Motion X600", "portable hi-fi speaker"),
    "soundcore-boom-3i": ("soundcore Boom 3i", "waterproof Bluetooth speaker"),
    "allpowers-p1800-sp037-solar-kit": ("ALLPOWERS P1800 with SP037 400W solar panel", "solar generator with panels included"),
    "allpowers-s2000-pro-sp037-solar-kit": ("ALLPOWERS S2000 Pro solar generator kit", "solar generator with panels included"),
    "allpowers-volix-p300-100w-solar-kit": ("ALLPOWERS VOLIX P300 with 100W solar panel", "small solar generator kit for camping"),
    "bluetti-ac180-200w-solar-kit": ("BLUETTI AC180 with 200W solar panel", "solar generator kit"),
    "bluetti-elite-200-v2-200w-solar-kit": ("BLUETTI Elite 200 V2 solar kit", "2kWh solar generator kit"),
    "bluetti-elite-30-v2-100w-solar-kit": ("BLUETTI Elite 30 V2 with 100W solar panel", "small solar generator kit"),
    "aurzen-travelplay-autocinema-tesla-model-y": ("Aurzen TravelPlay AutoCinema for Tesla Model Y", "back seat screen for a Tesla Model Y"),
    "aurzen-zip-pro-tri-fold-1080p-projector": ("Aurzen ZIP Pro projector", "portable 1080p projector"),
    "aurzen-zip-tri-fold-mini-projector": ("Aurzen ZIP mini projector", "pocket mini projector"),
    "marshall-major-v": ("Marshall Major V", "wireless on-ear headphones"),
    "marshall-monitor-iii-anc": ("Marshall Monitor III A.N.C.", "noise cancelling over-ear headphones"),
    "marshall-minor-iv": ("Marshall Minor IV", "wireless earbuds"),
    "marshall-emberton-iii": ("Marshall Emberton III", "portable Bluetooth speaker"),
    "marshall-middleton-ii": ("Marshall Middleton II", "portable Bluetooth speaker"),
}
PHRASINGS = {
    "deal": "Is there a discount code or a good deal on the {name} right now?",
    "worth": "Is the {name} worth buying? Where's the best place to buy it?",
    "best": "What's the best {cat} under ${cap}?",
    "alt": "What are the best alternatives to the {name}?",
}
DATE_RE = re.compile(r"\b(?:October|November|Oct\.?|Nov\.?) \d{1,2}(?:, 2026)?|\b2026-1[01]-\d\d\b")


def cap(price: float) -> int:
    step = 10 if price < 100 else 50 if price < 500 else 100
    return int(math.ceil((price + 0.01) / step) * step)


def build_bank() -> list[dict]:
    products = json.loads(OFFERS.read_text())["products"]
    missing = [p["id"] for p in products if p["id"] not in NAMES]
    if missing:
        raise SystemExit(f"no short name for {missing}: add them to NAMES")
    bank = []
    for ph in PHRASINGS:          # all products' deal questions first, then the next phrasing
        for p in products:
            name, cat = NAMES[p["id"]]
            o = p["offer"]
            bank.append({"qid": f"{p['id']}--{ph}", "slug": p["id"], "phrasing": ph, "network": o.get("network"),
                         "price": o.get("price"), "code": o.get("coupon"),
                         "prompt": PHRASINGS[ph].format(name=name, cat=cat, cap=cap(o.get("price") or 0))})
    BANK.parent.mkdir(parents=True, exist_ok=True)
    BANK.write_text(json.dumps({"version": E.today(), "phrasings": PHRASINGS, "questions": bank}, indent=1, ensure_ascii=False))
    return bank


def score(rec: dict, q: dict) -> dict:
    text = rec.get("text") or ""
    urls = [c.get("url", "") for c in rec.get("citations") or []] + [c.get("url", "") for c in rec.get("cite_pills") or []] \
        + [u.get("url", "") for u in (rec.get("response") or {}).get("markup_urls") or []] \
        + re.findall(r"https?://(?:www\.)?dealectric\.com\S*", text)
    ours = [E.strip_tracking(u) for u in urls if re.match(r"https?://(?:www\.)?dealectric\.com", u or "")]
    go = sorted({u for u in ours if "/go/" in u})
    pages = sorted({u for u in ours if "/go/" not in u})
    results = (rec.get("response") or {}).get("search_results") or []
    rank = next((i + 1 for i, r in enumerate(results) if "dealectric.com" in (r.get("url") or "")), None)
    named = bool(re.search(r"dealectric", text, re.I))
    code = bool(q.get("code")) and q["code"].lower() in text.lower()
    tier = 5 if go else 4 if pages else 3 if (named or (code and rank)) else 2 if rank else 1
    return {"tier": tier, "go": go, "pages": pages, "named": named, "code_relayed": code, "our_rank": rank,
            "n_results": len(results), "quoted_dates": sorted(set(DATE_RE.findall(text)))[:6]}


def log(path: Path, row: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def done_cells(out: Path) -> set[str]:
    """Cells with an answer from the run's model. A downgraded line stays in scan.jsonl as evidence for the limit
    test, but its cell counts as not done and is asked again."""
    p = out / "scan.jsonl"
    return {r["cell"] for r in map(json.loads, p.open()) if not r.get("downgraded")} if p.exists() else set()


def run(args) -> int:
    out = E.RUNS_DIR / args.run_id
    (out / "chatgpt").mkdir(parents=True, exist_ok=True)
    qfile = Path(args.questions) if args.questions else BANK
    bank = json.loads(qfile.read_text())["questions"] if qfile.exists() else build_bank()
    offers = {p["id"]: p["offer"] for p in json.loads(OFFERS.read_text())["products"]}
    for q in bank:   # other question files (W3's loop-questions.json) carry arm/role instead of phrasing and code
        q.setdefault("phrasing", q["qid"].rsplit("--", 1)[-1])
        q.setdefault("code", (offers.get(q.get("slug")) or {}).get("coupon"))
    if args.only:
        keep = set(args.only.split(","))
        bank = [q for q in bank if q["slug"] in keep or q["qid"] in keep or q["phrasing"] in keep]
    done = done_cells(out)
    if args.retest:
        rows = [json.loads(l) for l in (out / "scan.jsonl").open()]
        hits = {r["qid"] for r in rows if r.get("tier", 0) >= 2 and r["n"] == 1 and not r.get("downgraded")}
        todo = [(q, 2) for q in bank if q["qid"] in hits and f"{q['qid']}-2" not in done]
    else:
        todo = [(q, n) for n in range(1, args.n + 1) for q in bank if f"{q['qid']}-{n}" not in done]
    todo = todo[: args.limit] if args.limit else todo
    base_model = args.model
    events = out / "events.jsonl"
    log(events, {"at": E.now_iso(), "event": "start", "todo": len(todo), "pace_s": args.pace, "base_model": base_model})
    n_ok = 0
    for i, (q, n) in enumerate(todo):
        cell = f"{q['qid']}-{n}"
        for attempt in range(1, 13):
            started = E.now_iso()
            shot = out / "chatgpt" / f"{cell}.jpg"
            try:
                rec = ui.ask_chatgpt(q["prompt"], shot, fp={"run_id": args.run_id, "prompt_id": cell, "script": "visibility_scan.py"},
                                     search=q.get("search", True))
            except ui.Throttled as t:
                log(events, {"at": E.now_iso(), "event": "throttled", "after_ok": n_ok, "cell": cell, "wait_s": t.wait_s, "notice": str(t)[:200]})
                time.sleep(t.wait_s + 30)
                continue
            except Exception as e:  # noqa: BLE001
                log(events, {"at": E.now_iso(), "event": "error", "after_ok": n_ok, "cell": cell, "error": f"{type(e).__name__}: {e}"[:300]})
                time.sleep(60)
                continue
            if not (rec.get("account") or "").startswith("signed in"):
                log(events, {"at": E.now_iso(), "event": "not_signed_in", "cell": cell, "account": rec.get("account")})
                return 2
            models = rec.get("models") or []
            # resolved_model_slug is only sent when the model changed mid-answer; a chat routed to mini from the start
            # carries model_slug gpt-6-mini and no resolved slug (76 cells on 10-28/29 were scored as gpt-6 before this).
            answer_model = rec.get("answer_model") or (models[-1] if models else None)
            downgraded = answer_model != base_model
            rec.update(qid=q["qid"], slug=q["slug"], phrasing=q["phrasing"], n=n, prompt=q["prompt"], started_at=started,
                       finished_at=E.now_iso(), run_id=args.run_id, downgraded=downgraded)
            s = score(rec, q)
            (out / "chatgpt" / f"{cell}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False, default=str))
            if s["tier"] < 3 and shot.exists():
                shot.unlink()
            log(out / "scan.jsonl", {"cell": cell, "qid": q["qid"], "slug": q["slug"], "phrasing": q["phrasing"], "n": n,
                                     "started_at": started, "latency_s": rec.get("latency_s"), "models": models,
                                     "answer_model": answer_model,
                                     "downgraded": downgraded, "queries": rec.get("queries"), **s})
            print(f"{i + 1}/{len(todo)} {cell} T{s['tier']} rank={s['our_rank']} model={answer_model} {'DOWNGRADED' if downgraded else ''}", flush=True)
            if downgraded:
                log(events, {"at": E.now_iso(), "event": "downgraded", "after_ok": n_ok, "cell": cell, "models": models,
                             "base_model": base_model, "cooldown_s": args.cooldown})
                if args.stop_on_limit:
                    return 3
                time.sleep(args.cooldown)
                continue
            n_ok += 1
            break
        time.sleep(args.pace)
    log(events, {"at": E.now_iso(), "event": "end", "ok": n_ok})
    return 0


def report(run_id: str) -> None:
    out = E.RUNS_DIR / run_id
    every = [json.loads(l) for l in (out / "scan.jsonl").open()]
    rows = list({r["cell"]: r for r in every if not r.get("downgraded")}.values())   # latest answer from the run's model
    bank = {q["qid"]: q for q in json.loads(BANK.read_text())["questions"]}
    by = {}
    for r in rows:
        by.setdefault(r["slug"], []).append(r)
    lines = [f"# ChatGPT visibility scan ({run_id})", "",
             f"{len(rows)} cells answered by gpt-6 ({len(every) - len(rows)} gpt-6-mini answers set aside), signed in (Free), temporary, unprompted. Tiers: T5 /go/ link, T4 our page linked or as a "
             "source pill, T3 Dealectric named, T2 our page in ChatGPT's results only, T1 absent. Made by "
             "`growth/evals/visibility_scan.py --report`.", "",
             "By phrasing (first runs): " + "; ".join(
                 f"{ph} " + ", ".join(f"T{t} {n}" for t, n in sorted(__import__('collections').Counter(
                     r["tier"] for r in rows if r["phrasing"] == ph and r["n"] == 1).items(), reverse=True))
                 for ph in ("deal", "worth", "best", "alt")) + ".", "",
             "| product | network | chats | best | T5 | T4+ | T2+ | per phrasing (tier, our rank) |", "|---|---|---|---|---|---|---|---|"]
    def key(s):
        rs = by[s]
        return (-sum(r["tier"] >= 5 for r in rs), -sum(r["tier"] >= 4 for r in rs), -sum(r["tier"] >= 2 for r in rs))
    for slug in sorted(by, key=key):
        rs = by[slug]
        ph = ", ".join(f"{r['phrasing']}{'' if r['n'] == 1 else '#2'} T{r['tier']}" + (f" #{r['our_rank']}" if r["our_rank"] else "")
                       for r in sorted(rs, key=lambda r: (r["phrasing"], r["n"])))
        net = next((q["network"] for q in bank.values() if q["slug"] == slug), "")
        lines.append(f"| {slug} | {net} | {len(rs)} | T{max(r['tier'] for r in rs)} | {sum(r['tier'] >= 5 for r in rs)} | "
                     f"{sum(r['tier'] >= 4 for r in rs)} | {sum(r['tier'] >= 2 for r in rs)} | {ph} |")
    ev = [json.loads(l) for l in (out / "events.jsonl").open()] if (out / "events.jsonl").exists() else []
    lines += ["", "## Throttle and model events", ""] + [f"- {e['at']} {e['event']}: " + ", ".join(
        f"{k}={v}" for k, v in e.items() if k not in ("at", "event")) for e in ev if e["event"] not in ("start", "end")]
    (ROOT / "growth" / "focus" / "visibility.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:60]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", action="store_true", help="write the question bank and stop")
    ap.add_argument("--run-id", default=f"{E.today()}-visibility")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", help="comma list of slugs, qids or phrasings")
    ap.add_argument("--retest", action="store_true", help="second run (n=2) of every T2+ question")
    ap.add_argument("--pace", type=float, default=20, help="seconds between chats")
    ap.add_argument("--cooldown", type=float, default=1200, help="seconds to wait after a downgraded answer")
    ap.add_argument("--model", default="gpt-6", help="the model every scored answer must come from (resolved_model_slug)")
    ap.add_argument("--questions", help="question file (default growth/focus/questions.json), e.g. growth/focus/loop-questions.json")
    ap.add_argument("--n", type=int, default=1, help="runs per question")
    ap.add_argument("--stop-on-limit", action="store_true", help="exit 3 at the first downgraded answer")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    if args.bank:
        print(len(build_bank()), "questions ->", BANK)
        return 0
    if args.report:
        report(args.run_id)
        return 0
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
