"""Third A push (Barry 11-12): find the Amazon US listing for every product on a group A page that has no direct program,
so each table row can carry a buy link (our tagged Amazon link). Writes candidates for review; nothing is published."""
import json, re, sys, time
sys.path.insert(0, 'src'); sys.path.insert(0, 'tools')
import gaps, amzcheck
A = [l.strip().strip('/') for l in open('growth/focus/ab/A-slugs.txt') if l.strip()]
recs = {r['slug']: r for r in gaps.GAP_PAGES}
out_path = 'growth/focus/ab/push3/asin-candidates.jsonl'
done = set()
try:
    for l in open(out_path):
        done.add(tuple(json.loads(l)['key']))
except FileNotFoundError:
    pass
seen = set()
for s in A:
    for x in recs[s]['rows']:
        if x.get('slug') or x.get('kit'):
            continue
        key = (x['brand'], x['model'])
        if key in seen or key in done:
            continue
        seen.add(key)
        model = re.sub(r'\((?:\d{4}|Refurbished|used).*?\)', '', x['model'])
        q = f"{x['brand']} {model}".strip()
        res = []
        for attempt in range(3):
            res = amzcheck.search(q)
            if res:
                break
            time.sleep(20)
        with open(out_path, 'a') as f:
            f.write(json.dumps({'key': list(key), 'query': q, 'url': x.get('url'), 'results': res}) + '\n')
        print(len(seen), q, len(res), flush=True)
        time.sleep(6)
print('asin lookup done')
