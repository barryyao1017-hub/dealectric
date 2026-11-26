"""Add a research file's questions to the discovery queue, interleaved at the front of what is still pending."""
import json, re, sys, os
from pathlib import Path
Q = Path('growth/focus/open-queries/queue.jsonl'); SCAN = Path('growth/evals/runs/2026-11-14-openq/scan.jsonl')
src, group, tag = sys.argv[1], sys.argv[2], sys.argv[3]
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:46]
rows = [json.loads(l) for l in Q.read_text().splitlines() if l.strip()]
done = {json.loads(l)['qid'] for l in SCAN.read_text().splitlines()} if SCAN.exists() else set()
have = {r['prompt'].lower() for r in rows}
new = []
for i, x in enumerate(sorted(json.load(open(src)), key=lambda x: -int(x.get('times_seen') or 0))):
    p = x['q'].strip()
    if p.lower() in have: continue
    new.append({"qid": f"{tag}{i:03d}-{slug(p)}", "prompt": p, "group": x.get('category') and 'other' or group, "shape": "use-case", "source": "forum",
                "use_case": x.get('use_case'), "category": x.get('category'), "evidence": x.get('evidence') or [], "times_seen": x.get('times_seen'),
                "why_open": x.get('why_open'), "answer_needs": x.get('answer_needs')})
head = [r for r in rows if r['qid'] in done]; pend = [r for r in rows if r['qid'] not in done]
keep = pend[:2]; pend = pend[2:]      # don't disturb the question being asked right now
mix = []
for i in range(max(len(new), len(pend))):
    if i < len(new): mix.append(new[i])
    if i < len(pend): mix.append(pend[i])
tmp = Q.with_suffix('.tmp'); tmp.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in head + keep + mix) + '\n'); os.replace(tmp, Q)
print('added', len(new), '| queue', len(head + keep + mix), '| done', len(done))
