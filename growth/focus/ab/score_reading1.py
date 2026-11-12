"""Score A/B reading 1 (DLC-208): pages OAI-SearchBot re-fetched after the second push, same pages' 11-08 baseline."""
import json, collections, math
f = json.load(open('growth/focus/ab/fetched-reading1.json'))
grp = {p[1:]: g for g in 'AB' for p in f[g]}

def load(run):
    out = {}
    try:
        for l in open(f'growth/evals/runs/{run}/scan.jsonl'):
            r = json.loads(l)
            if r['answer_model'] == 'gpt-6' and r['slug'] in grp:
                out[r['cell']] = r
    except FileNotFoundError:
        pass
    return list(out.values())

now = load('2026-11-09-ab-early') + load('2026-11-10-ab-reading1') + load('2026-11-10-ab-reading1b') + load('2026-11-11-ab-reading1c') + load('2026-11-12-ab-reading1d')
base = load('2026-11-08-ab-harvest-A') + load('2026-11-08-ab-baseline-B')
cited = lambda r: (r.get('tier') or 0) >= 4

print('pages: A', sum(v == 'A' for v in grp.values()), 'B', sum(v == 'B' for v in grp.values()))
for lab, rows in [('baseline 11-08', base), ('reading 1', now)]:
    for g in 'AB':
        rs = [r for r in rows if grp[r['slug']] == g]
        ret = [r for r in rs if r.get('our_rank')]
        c = sum(map(cited, ret))
        print(f"{lab:15} {g}: chats {len(rs):3} retrieved {len(ret):3} cited {c:3} "
              f"({c / max(1, len(ret)):.0%} when retrieved) /go/ {sum(1 for r in rs if r.get('go'))}")

pp = collections.defaultdict(lambda: {'b': [0, 0], 'n': [0, 0]})
for k, rows in (('b', base), ('n', now)):
    for r in rows:
        if r.get('our_rank'):
            pp[r['slug']][k][1] += 1
            pp[r['slug']][k][0] += cited(r)
diffs = {}
for g in 'AB':
    d = [v['n'][0] / v['n'][1] - v['b'][0] / v['b'][1] for s, v in pp.items()
         if grp[s] == g and v['b'][1] and v['n'][1]]
    m = sum(d) / len(d)
    sd = math.sqrt(sum((x - m) ** 2 for x in d) / max(1, len(d) - 1))
    diffs[g] = (m, sd / math.sqrt(len(d)), len(d))
    print(f"paired change {g}: {m * 100:+.0f} pts over {len(d)} pages (SE {sd / math.sqrt(len(d)) * 100:.0f})")
(ma, sa, _), (mb, sb, _) = diffs['A'], diffs['B']
print(f"net A - B: {(ma - mb) * 100:+.0f} pts (SE {math.hypot(sa, sb) * 100:.0f})")
