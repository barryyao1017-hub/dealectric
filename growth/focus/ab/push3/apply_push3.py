"""Third A push (DLC-208, Barry 11-12): on every group A record set "all_links" (a buy link on every row: our program,
else our tagged Amazon link, else the maker's page; the pick is always a product we link), "buy_compare" where a
product's link is the cheapest way to buy and its discount was cart-tested on that exact item, a row "asin" where
Amazon lists the exact product, and "updated". Edits gaps.py in place by AST position, bottom-up.
    python3.12 apply_push3.py <repo root> <date>"""
import ast, json, sys
root, date = sys.argv[1], sys.argv[2]
here = '/Users/j0y0825/code/dealectric/growth/focus/ab/push3/'
A = {l.strip().strip('/') for l in open(here + '../A-slugs.txt') if l.strip()}
elig = set(json.load(open(here + 'eligible.json')))
asins = {}
for n in (1, 2, 3):
    try:
        for x in json.load(open(here + f'asin-done-{n}.json')):
            if x.get('asin'):
                asins[(x['brand'], x['model'])] = x['asin']
    except FileNotFoundError:
        pass
gp = f'{root}/src/gaps.py'
src = open(gp).read()
lines = src.splitlines(keepends=True)
offs = [0]
for l in lines:
    offs.append(offs[-1] + len(l))
pos = lambda ln, col: offs[ln - 1] + len(lines[ln - 1].encode()[:col].decode())
edits = []   # (start, end, text)
seen = set()
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
    m = node.values[keys.index("method")]
    ins = ' "all_links": True,' + (' "buy_compare": True,' if slug in elig else '')
    if "all_links" not in keys:
        e = pos(m.end_lineno, m.end_col_offset)
        edits.append((e + 1, e + 1, ins))   # after the comma that ends the method line
    u = node.values[keys.index("updated")]
    edits.append((pos(u.lineno, u.col_offset), pos(u.end_lineno, u.end_col_offset), repr(date)))
    for row in node.values[keys.index("rows")].elts:
        rk = [k.value for k in row.keys]
        if "slug" in rk or "kit" in rk or "asin" in rk:
            continue
        a = asins.get((row.values[rk.index("brand")].value, row.values[rk.index("model")].value))
        if a:
            s = pos(row.lineno, row.col_offset) + 1
            edits.append((s, s, f'"asin": {a!r}, '))
for s, e, t in sorted(edits, reverse=True):
    src = src[:s] + t + src[e:]
open(gp, 'w').write(src)
print('records', len(seen), 'of', len(A), '| comparison', len(elig & seen), '| asins', sum(1 for x in edits if x[2].startswith('"asin"')))
