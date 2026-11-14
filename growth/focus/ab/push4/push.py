"""Group A's third-push treatment on the 66 retrieved gap pages (Barry 11-13, DLC-272; the 11-12 version for group A is
growth/focus/ab/push3/). Run from the repo root, in order:

    python3.12 growth/focus/ab/push4/push.py lookup      # Amazon search for every row with no program link -> candidates.jsonl
    python3.12 growth/focus/ab/push4/push.py match       # pick the exact listing per row -> asin-picks.json
    python3.12 growth/focus/ab/push4/push.py products    # product slugs the pages link (for tools/buycheck.py)
    python3.12 growth/focus/ab/push4/push.py eligible <buycheck report>   # pages with a linked product cheapest through the link
    python3.12 growth/focus/ab/push4/push.py apply <date>                 # all_links, buy_compare, row asin, updated

lookup and match read Amazon in a background tab of the Agent Chrome (localhost:9222) through tools/amzcheck.py.
The match rule: the brand and every model-number token in the listing title, and no edition word (Plus, Pro, Max, ...)
the row's model lacks; used and refurbished rows get no link. apply edits src/gaps.py in place by AST position.
"""
import ast, json, re, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'src')); sys.path.insert(0, str(ROOT / 'tools'))
SLUGS = [l.strip() for l in open(HERE / 'slugs.txt') if l.strip()]
CAND, PICKS, ELIG = HERE / 'candidates.jsonl', HERE / 'asin-picks.json', HERE / 'eligible.json'
ACCESSORY = re.compile(r"\b(replacement|remote|case|cover|sleeve|bag|mount|screen protector|(extra|expansion|smart extra) battery|for use with|compatible with)\b", re.I)
EDITIONS = {"plus", "pro", "max", "ultra", "gt", "mini", "lite", "se", "uc", "x", "air", "2", "3", "4", "5", "6", "7"}


def recs():
    import gaps
    return {r['slug']: r for r in gaps.GAP_PAGES if r['slug'] in SLUGS}


def open_rows():
    seen = []
    for s, r in recs().items():
        g = (json.loads((ROOT / 'growth/focus/ab' / s / 'draft.json').read_text()).get('gate') or {})
        if not g.get('pass'):   # only the researched record, once abpage apply has put it in gaps.py
            continue
        for x in r.get('rows') or []:
            if x.get('slug') or x.get('kit') or x.get('asin'):
                continue
            k = (x['brand'], x['model'])
            if k not in seen:
                seen.append(k)
    return seen


def lookup():
    import amzcheck
    done = {tuple(json.loads(l)['key']) for l in open(CAND)} if CAND.exists() else set()
    todo = [k for k in open_rows() if k not in done]
    for i, (brand, model) in enumerate(todo):
        if re.search(r"used|refurb", model, re.I):
            continue
        q = f"{brand} {re.sub(r'\((?:\d{4}|Refurbished|used).*?\)', '', model)}".strip()
        res = []
        for _ in range(3):
            res = amzcheck.search(q)
            if res:
                break
            time.sleep(20)
        with open(CAND, 'a') as f:
            f.write(json.dumps({'key': [brand, model], 'query': q, 'results': res}) + '\n')
        print(i + 1, len(todo), q, len(res), flush=True)
        time.sleep(6)


norm = lambda t: re.sub(r"[^a-z0-9+]", "", t.lower())
words = lambda t: set(re.findall(r"[a-z0-9]+", t.lower()))


def tokens(model):
    m = re.sub(r"\(.*?\)", " ", model)
    return [norm(w) for w in re.split(r"[\s,/]+", m) if re.search(r"\d", w) and len(norm(w)) >= 2]


def match():
    import amzcheck
    out = json.loads(PICKS.read_text()) if PICKS.exists() else {}
    for l in open(CAND):
        c = json.loads(l); brand, model = c['key']; key = f"{brand}|{model}"
        if key in out:
            continue
        toks, mw, pick, li = tokens(model), words(brand + " " + model), None, {}
        for r in c['results']:
            t = r.get('title') or ''
            if not t:
                continue
            nt, tw = norm(t), words(t)
            if toks and not all(x in nt for x in toks):
                continue
            if not toks and not all(w in tw for w in words(model) - {"the", "with", "and"}):
                continue
            if (tw & EDITIONS) - mw:
                continue
            li = amzcheck.listing(r['asin']); time.sleep(4)   # search titles drop the brand: check it on the listing
            if li.get('found') and norm(brand.split()[0]) in norm(li.get('title') or '') \
                    and (not toks or all(x in norm(li['title']) for x in toks)) and not ((words(li['title']) & EDITIONS) - mw) \
                    and not (ACCESSORY.search(li['title']) and not ACCESSORY.search(model)):
                pick = r; break
        if not pick:
            out[key] = {"asin": None, "why": "no title match", "seen": [r.get('title', '')[:90] for r in c['results'][:4]]}
            continue
        out[key] = {"asin": pick['asin'], "title": li.get('title'), "search_title": pick['title'], "why": ""}
        PICKS.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    PICKS.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for k, v in out.items():
        print(('OK ' if v.get('asin') else '-- '), k[:60].ljust(60), v.get('asin') or v['why'], '|', (v.get('title') or '')[:80])


def products():
    ps = []
    for r in recs().values():
        for x in r.get('rows') or []:
            if x.get('slug') and x['slug'] not in ps:
                ps.append(x['slug'])
    print(' '.join(ps))


def eligible(report):
    """A page gets buy_compare when one of its linked products is cheapest through our link (buycheck verdict) and its
    discount was cart-tested on that exact item (build.lowest_parts re-checks this and hides a line that no longer holds)."""
    import build as B
    rep = json.load(open(report))
    rows = rep.get('products') if isinstance(rep, dict) else rep
    cheap = {x['slug'] for x in rows if x.get('verdict') == 'cheapest'}
    out = {}
    for s, r in recs().items():
        hit = [x['slug'] for x in r.get('rows') or [] if x.get('slug') in cheap and B.lowest_parts(B.BY_SLUG[x['slug']])]
        if hit:
            out[s] = hit
    ELIG.write_text(json.dumps(out, indent=1) + '\n')
    print(len(out), 'pages eligible:', json.dumps(out)[:1500])


def apply(date):
    picks = json.loads(PICKS.read_text()) if PICKS.exists() else {}
    elig = set(json.loads(ELIG.read_text())) if ELIG.exists() else set()
    A = set(SLUGS)
    gp = ROOT / 'src/gaps.py'
    src = gp.read_text()
    lines = src.splitlines(keepends=True)
    offs = [0]
    for l in lines:
        offs.append(offs[-1] + len(l))
    pos = lambda ln, col: offs[ln - 1] + len(lines[ln - 1].encode()[:col].decode())
    edits, seen = [], set()
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.Dict):
            continue
        keys = [k.value if isinstance(k, ast.Constant) else None for k in node.keys]
        if "slug" not in keys or "h1" not in keys:
            continue
        slug = node.values[keys.index("slug")].value
        if slug not in A:
            continue
        seen.add(slug)
        ins = (' "all_links": True,' if "all_links" not in keys else '') + \
              (' "buy_compare": True,' if slug in elig and "buy_compare" not in keys else '')
        if ins:
            m = node.values[keys.index("method" if "method" in keys else "slug")]
            e = pos(m.end_lineno, m.end_col_offset)
            edits.append((e + 1, e + 1, ins))   # after the comma that ends the method (else slug) entry
        if "updated" in keys:
            u = node.values[keys.index("updated")]
            edits.append((pos(u.lineno, u.col_offset), pos(u.end_lineno, u.end_col_offset), repr(date)))
        for row in node.values[keys.index("rows")].elts:
            rk = [k.value for k in row.keys]
            if "slug" in rk or "kit" in rk or "asin" in rk:
                continue
            a = (picks.get(f"{row.values[rk.index('brand')].value}|{row.values[rk.index('model')].value}") or {}).get('asin')
            if a:
                s = pos(row.lineno, row.col_offset) + 1
                edits.append((s, s, f'"asin": {a!r}, '))
    for s, e, t in sorted(edits, reverse=True):
        src = src[:s] + t + src[e:]
    gp.write_text(src)
    print('records', len(seen), 'of', len(A), '| comparison', len(elig & seen),
          '| asins', sum(1 for x in edits if x[2].startswith('"asin"')), '| missing', sorted(A - seen))


if __name__ == '__main__':
    cmd = sys.argv[1]
    {'lookup': lookup, 'match': match, 'products': products}.get(cmd, lambda: None)()
    if cmd == 'eligible':
        eligible(sys.argv[2])
    if cmd == 'apply':
        apply(sys.argv[2])
