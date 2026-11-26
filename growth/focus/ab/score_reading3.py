"""Score reading 3, the B replication (DLC-272), by the rule pre-registered in push.json b_replication.reading_rule:
B's paired change in cited-when-retrieved (reading 2 -> 3) minus A's same-window paired change on its non-comparison
pages; >= +13 pts replicated, 0 to +13 partial, <= 0 not replicated. Also: B reading 3 vs the 11-08 baseline next to
A reading 2 vs 11-08, and handover (/go/ or the dealectric-20 Amazon tag in the answer) on comparison pages.
    python3.12 growth/focus/ab/score_reading3.py"""
import json, collections, math, subprocess

Q = json.load(open('growth/focus/ab-reading3.json'))['questions']
grp = {q['slug']: q['group'] for q in Q}
PUSH = json.loads(subprocess.run(['git', 'show', 'origin/main:growth/focus/ab/push.json'], capture_output=True, text=True).stdout)
BUY_A = set(PUSH['third_push']['buy_compare_pages'])
BUY_B = set(PUSH['b_replication']['pushed']['comparison_pages'])
R2, R3 = '2026-11-13-ab-reading2', '2026-11-17-ab-reading3'


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


def handed(run, cell):
    try:
        d = json.load(open(f'growth/evals/runs/{run}/chatgpt/{cell}.json'))
    except FileNotFoundError:
        return False
    s = json.dumps([d.get('text'), d.get('ui')])
    return 'dealectric.com/go/' in s or 'tag=dealectric-20' in s


cited = lambda r: int(r.get('tier') or 0) >= 4
ranked = lambda r: r.get('our_rank') not in (None, '', 'None')
base = load('2026-11-08-ab-harvest-A') + load('2026-11-08-ab-baseline-B')
r2, r3 = load(R2), load(R3)

print('pages: A', sum(v == 'A' for v in grp.values()), 'B', sum(v == 'B' for v in grp.values()))
for lab, rows in [('baseline 11-08', base), ('reading 2', r2), ('reading 3', r3)]:
    for g in 'AB':
        rs = [r for r in rows if grp[r['slug']] == g]
        ret = [r for r in rs if ranked(r)]
        c = sum(map(cited, ret))
        print(f"{lab:15} {g}: chats {len(rs):3} retrieved {len(ret):3} ({len(ret) / max(1, len(rs)):.0%}) cited {c:3} "
              f"({c / max(1, len(ret)):.0%} when retrieved)")


def per_page(rows):
    pp = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        if ranked(r):
            pp[r['slug']][1] += 1
            pp[r['slug']][0] += cited(r)
    return pp


def paired(a, b, keep):
    pa, pb = per_page(a), per_page(b)
    d = [pb[s][0] / pb[s][1] - pa[s][0] / pa[s][1] for s in grp if keep(s) and pa[s][1] and pb[s][1]]
    if not d:
        return 0, 0, 0
    m = sum(d) / len(d)
    sd = math.sqrt(sum((x - m) ** 2 for x in d) / max(1, len(d) - 1))
    return m, sd / math.sqrt(len(d)), len(d)


mb, sb, nb = paired(r2, r3, lambda s: grp[s] == 'B')
ma, sa, na = paired(r2, r3, lambda s: grp[s] == 'A' and s not in BUY_A)
mac, sac, nac = paired(r2, r3, lambda s: grp[s] == 'A' and s in BUY_A)
print(f"B change r2 -> r3: {mb * 100:+.0f} pts over {nb} pages (SE {sb * 100:.0f})")
print(f"A change r2 -> r3, non-comparison pages (time control): {ma * 100:+.0f} pts over {na} pages (SE {sa * 100:.0f})")
print(f"A change r2 -> r3, comparison pages (changed 11-13, reported apart): {mac * 100:+.0f} pts over {nac} pages (SE {sac * 100:.0f})")
net = mb - ma
call = 'REPLICATED' if net >= 0.13 else 'PARTIAL' if net > 0 else 'NOT REPLICATED'
print(f"NET B - A: {net * 100:+.0f} pts (SE {math.hypot(sb, sa) * 100:.0f}) -> {call}")
m1, s1, n1 = paired(base, r3, lambda s: grp[s] == 'B')
m2, s2, n2 = paired(base, r2, lambda s: grp[s] == 'A')
print(f"vs 11-08 baseline: B reading 3 {m1 * 100:+.0f} pts over {n1} pages (SE {s1 * 100:.0f}); "
      f"A reading 2 {m2 * 100:+.0f} pts over {n2} pages (SE {s2 * 100:.0f})")

for g, buy in (('A', BUY_A), ('B', BUY_B)):
    rs = [r for r in r3 if grp[r['slug']] == g]
    hb = [r for r in rs if r['slug'] in buy and ranked(r)]
    print(f"handover {g}: {sum(handed(R3, r['cell']) for r in rs)} of {len(rs)} chats; on comparison pages with our page "
          f"retrieved: {sum(handed(R3, r['cell']) for r in hb)} of {len(hb)}")
