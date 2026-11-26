"""Was a product ever seen in ChatGPT's catalog? (2026-11-15) Evidence across every saved chat of the discovery, repeat
and probe runs: (1) an inline catalog card whose title names the product, with its seller and price; (2) a seller in
the product panel behind a typed name (panelprobe); (3) panels that opened with no seller; (4) how often ChatGPT typed
the name. A product counts as a catalog gap only if (1) and (2) were never seen and (3) was seen."""
import json, glob, re, collections, sys, os
sys.path.insert(0, 'growth/evals'); sys.path.insert(0, 'src')
import openscan as O
RUNS = ['2026-11-14-openq', '2026-11-15-openq-confirm', '2026-11-15-openq-third', '2026-11-15-panelprobe', '2026-11-15-productprobe', '2026-11-15-shortlist', '2026-11-14-top-bottom']
EXT = {'ultra', 'plus', 'max', 'x', 'v2', 'gen', 'pro', 'mini', 'classic', 'l', 'p', 't', 'na', 'd', 'dc', '2', '3'}
norm = lambda s: re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
def names():
    top = [k for k, v in json.load(open('growth/focus/open-queries/report/typed-products.json')) if v >= 2]
    q = [n for l in open('growth/focus/open-queries/product-queue.jsonl') for n in json.loads(l)['names']]
    return list(dict.fromkeys(q + top))
def in_title(name, title):
    n, t = norm(name), norm(title)
    i = t.find(n)
    if i < 0 or (i > 0 and t[i - 1] != ' '):
        return False
    rest = t[i + len(n):].split()
    return not (rest and (rest[0] in EXT or re.fullmatch(r'\d{1,2}', rest[0])))
ev = {n: {"typed": 0, "cards": [], "panel_seller": [], "panel_none": 0} for n in names()}
for run in RUNS:
    for f in glob.glob(f'growth/evals/runs/{run}/chatgpt/*.json') + glob.glob(f'growth/evals/runs/{run}/*.json'):
        try: d = json.load(open(f))
        except Exception: continue
        if not isinstance(d, dict) or 'response' not in d or d.get('downgraded'): continue
        rd = O.reading(d)
        for tn in rd['typed_names']:
            for n in ev:
                if norm(re.sub(r'\s*\(.*?\)', '', tn)) == norm(n): ev[n]["typed"] += 1
        if not rd['carded']: continue
        lines = [l.strip() for l in (d.get('text') or '').split('\n') if l.strip()]
        for i, l in enumerate(lines):
            if len(l) < 18 or len(l) > 140 or '$' in l: continue
            nxt = lines[i + 1:i + 6]
            price = next((x for x in nxt if re.fullmatch(r'\$[\d,]+(\.\d\d)?', x)), None)
            if not price: continue
            for n in ev:
                if in_title(n, l) and len(norm(l)) >= len(norm(n)) + 8:      # a catalog title is longer than the bare name
                    seller = next((x for x in nxt if not x.startswith('$') and len(x) < 45 and not re.search(r'Wh|W\b|·|•', x)), '')
                    ev[n]["cards"].append({"title": l[:80], "seller": seller, "price": price, "run": run, "qid": d.get('qid')})
    p = f'growth/evals/runs/{run}/panels.jsonl'
    if os.path.exists(p):
        for l in open(p):
            for x in json.loads(l)['panels']:
                for n in ev:
                    if norm(x['name']) == norm(n) or norm(x['name']).startswith(norm(n) + ' portable'):
                        if x.get('visit'): ev[n]["panel_seller"] += x.get('sellers') or ['?']
                        elif x.get('panel'): ev[n]["panel_none"] += 1
import products as PR
recs = [v for v in vars(PR).values() if isinstance(v, list) and v and isinstance(v[0], dict)][0]
BR = {"bluetti": "our BLUETTI program (Awin)", "allpowers": "our ALLPOWERS program (CJ)", "anker": "our Anker SOLIX program (Rakuten)", "oscal": "our OSCAL program (Awin)",
      "growatt": "our Growatt program", "mango": "our Mango Power program", "nature": "our Nature's Generator program", "zendure": "our Zendure program",
      "ecoflow": "Amazon tag only", "jackery": "Amazon tag only", "goal": "Amazon tag only", "dji": "Amazon tag only", "pecron": "Amazon tag only", "oupes": "Amazon tag only", "dabbsson": "Amazon tag only", "vtoman": "Amazon tag only"}
out = []
for n, e in ev.items():
    seen = bool(e["cards"] or e["panel_seller"])
    status = "in catalog" if seen else "gap" if e["panel_none"] else "not checked"
    rec = next((r for r in recs if norm(r.get('name') or '').endswith(norm(n)) or norm(n) in norm(r.get('name') or '')), None)
    out.append({"product": n, "status": status, "typed": e["typed"], "cards": len(e["cards"]), "card_sellers": sorted({c["seller"] for c in e["cards"]})[:4],
                "panel_sellers": sorted(set(e["panel_seller"])), "panel_none": e["panel_none"], "link": BR.get(norm(n).split()[0], "none"),
                "our_record": (rec.get('slug') or rec.get('id')) if rec else None, "our_program": rec.get('program') if rec else None})
json.dump(out, open('growth/focus/open-queries/report/catalog-presence.json', 'w'), indent=1)
c = collections.Counter(o["status"] for o in out); print(dict(c))
for st in ("gap", "in catalog", "not checked"):
    print('==', st)
    for o in sorted([o for o in out if o["status"] == st], key=lambda o: -o["typed"]):
        print(f"  typed {o['typed']:3} cards {o['cards']:2} {str(o['card_sellers'])[:50]:50} panel seller {str(o['panel_sellers'])[:28]:28} none {o['panel_none']} | {o['product'][:42]:42} | {o['link'][:28]:28} | {o['our_record']}")
