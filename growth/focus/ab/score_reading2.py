"""Score A/B reading 2 (DLC-208): pages OAI-SearchBot re-fetched after the third push (2026-11-12T09:34:12Z),
same pages' 11-08 baseline. Handover = our /go/ or Amazon-tagged link in the answer text or its widgets."""
import json, collections, math, glob, sys
sys.path.insert(0, 'src')
import gaps
f = json.load(open('growth/focus/ab/fetched-reading2.json'))
grp = {s: g for g in 'AB' for s in f[g]}
import subprocess
PUSH = json.loads(subprocess.run(['git', 'show', 'origin/main:growth/focus/ab/push.json'], capture_output=True, text=True).stdout)
BUY = set(PUSH['third_push']['buy_compare_pages'])
PRICED = {l[5:-5] for l in subprocess.run(['git', 'show', '--name-only', '--format=', '6accf713'], capture_output=True, text=True).stdout.split() if l.startswith('docs/')}
RUN = '2026-11-13-ab-reading2'

def load(run):
    out = {}
    for l in open(f'growth/evals/runs/{run}/scan.jsonl'):
        r = json.loads(l)
        if r['answer_model'] == 'gpt-6' and r['slug'] in grp:
            out[r['cell']] = r
    return list(out.values())

def handed(cell):
    try:
        d = json.load(open(f'growth/evals/runs/{RUN}/chatgpt/{cell}.json'))
    except FileNotFoundError:
        return False
    s = json.dumps([d.get('text'), d.get('ui')])
    return 'dealectric.com/go/' in s or 'tag=dealectric-20' in s

now = load(RUN)
base = load('2026-11-08-ab-harvest-A') + load('2026-11-08-ab-baseline-B')
cited = lambda r: int(r.get('tier') or 0) >= 4
ranked = lambda r: r.get('our_rank') not in (None, '', 'None')

print('pages: A', sum(v == 'A' for v in grp.values()), 'B', sum(v == 'B' for v in grp.values()),
      '| buy_compare pages: A', sum(1 for s in BUY if grp.get(s) == 'A'), 'B', sum(1 for s in BUY if grp.get(s) == 'B'))
for lab, rows in [('baseline 11-08', base), ('reading 2', now)]:
    for g in 'AB':
        rs = [r for r in rows if grp[r['slug']] == g]
        ret = [r for r in rs if ranked(r)]
        c = sum(map(cited, ret))
        print(f"{lab:15} {g}: chats {len(rs):3} retrieved {len(ret):3} ({len(ret)/max(1,len(rs)):.0%}) cited {c:3} "
              f"({c / max(1, len(ret)):.0%} when retrieved)")
for g in 'AB':
    rs = [r for r in now if grp[r['slug']] == g]
    h = [r['cell'] for r in rs if handed(r['cell'])]
    hb = [r for r in rs if r['slug'] in BUY and ranked(r)]
    print(f"handover {g}: {len(h)} of {len(rs)} chats; on buy_compare pages with our page retrieved: "
          f"{sum(handed(r['cell']) for r in hb)} of {len(hb)}")

pp = collections.defaultdict(lambda: {'b': [0, 0], 'n': [0, 0]})
for k, rows in (('b', base), ('n', now)):
    for r in rows:
        if ranked(r):
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

for g in 'AB':
    for lab, keep in (('Amazon prices', True), ('no Amazon prices', False)):
        d = [v['n'][0] / v['n'][1] - v['b'][0] / v['b'][1] for s, v in pp.items()
             if grp[s] == g and v['b'][1] and v['n'][1] and ((s in PRICED) == keep)]
        if d:
            print(f"  {g} pages with {lab}: {sum(d) / len(d) * 100:+.0f} pts over {len(d)} pages")
