"""Pick the Amazon listing for each row from asin-candidates.jsonl: the brand and every model-number token must be in
the listing title, and no edition word (Plus, Pro, Max, Ultra, GT, Gen 2, ...) the row's model lacks. The pick is then
re-read by ASIN (amzcheck.listing) so the stored title is the listing's own. Used and refurbished rows get no link."""
import json, re, sys, time
sys.path.insert(0, 'tools'); import amzcheck
EDITIONS = {"plus", "pro", "max", "ultra", "gt", "mini", "lite", "se", "uc", "x", "air", "2", "3", "4", "5", "6", "7"}
norm = lambda t: re.sub(r"[^a-z0-9+]", "", t.lower())
def tokens(model):
    m = re.sub(r"\(.*?\)", " ", model)
    return [norm(w) for w in re.split(r"[\s,/]+", m) if re.search(r"\d", w) and len(norm(w)) >= 2]
def words(t): return set(re.findall(r"[a-z0-9]+", t.lower()))
out = {}
try:
    out = json.load(open('growth/focus/ab/push3/asin-picks.json'))
except FileNotFoundError:
    pass
for l in open('growth/focus/ab/push3/asin-candidates.jsonl'):
    c = json.loads(l); brand, model = c['key']; key = f"{brand}|{model}"
    if key in out:
        continue
    if re.search(r"used|refurb", model, re.I):
        out[key] = {"asin": None, "why": "used or refurbished"}; continue
    toks = tokens(model); mw = words(brand + " " + model)
    pick = None
    for r in c['results']:
        t = r.get('title') or ''
        if not t:
            continue
        nt = norm(t); tw = words(t)
        if toks and not all(x in nt for x in toks):
            continue
        if not toks and not all(w in tw for w in words(model) - {"the", "with", "and"}):
            continue
        if norm(brand.split()[0]) not in nt and toks == []:
            continue
        extra = (tw & EDITIONS) - mw
        if extra:
            continue
        pick = r; break
    if not pick:
        out[key] = {"asin": None, "why": "no title match", "seen": [r.get('title', '')[:90] for r in c['results'][:4]]}; continue
    li = amzcheck.listing(pick['asin']); time.sleep(4)
    out[key] = {"asin": pick['asin'] if li.get('found') else None, "title": li.get('title') or pick['title'],
                "search_title": pick['title'], "why": "" if li.get('found') else "listing not readable"}
json.dump(out, open('growth/focus/ab/push3/asin-picks.json', 'w'), indent=1, ensure_ascii=False)
for k, v in out.items():
    print(('OK ' if v.get('asin') else '-- '), k[:60].ljust(60), v.get('asin') or v['why'], '|', (v.get('title') or '')[:80])
