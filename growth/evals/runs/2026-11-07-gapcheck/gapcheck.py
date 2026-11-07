"""One OpenAI web search per gap page's own query; where does dealectric.com rank? (Barry, 2026-11-07)"""
import json, sys, concurrent.futures as cf, re
ROOT = "/Users/j0y0825/code/dealectric"
sys.path.insert(0, ROOT + "/growth/evals")
import apiprobe as A, evallib as E, serpsources as SS
S = sys.argv[1]
pages = json.load(open(S + "/gapq.json"))
k = SS.key("openai")
def one(p):
    q = p["query"]; started = E.now_iso()
    for attempt in range(3):
        st, resp = A.post({"model": "gpt-6-luna", "input": f'Run exactly one web search with this exact query, word for word: "{q}". '
                       "Do not search again and do not open any page. Then reply only with the word DONE.",
                       "store": False, "max_tool_calls": 1, "include": ["web_search_call.action.sources"],
                       "tools": [{"type": "web_search", "user_location": {"type": "approximate", "country": "US"}}]}, k)
        if st == 200: break
    srcs = [s.get("url") for it in resp.get("output", []) if it.get("type") == "web_search_call"
            for s in ((it.get("action") or {}).get("sources") or [])]
    qs = [((it.get("action") or {}).get("query")) for it in resp.get("output", []) if it.get("type") == "web_search_call"]
    E.footprint("openai-api", started, E.now_iso(), prompt=q, script="gapcheck.py", run_id="gapcheck-1107",
                retrieved=[{"url": u} for u in srcs], error=None if st == 200 else str(resp.get("error"))[:200])
    ours = [(i + 1, u) for i, u in enumerate(srcs) if u and "dealectric.com" in u]
    return dict(p, status=st, searched=qs, n=len(srcs), ours=ours, results=srcs, usage=resp.get("usage"))
out = []
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(one, pages):
        out.append(r); print(r["status"], r["n"], r["ours"][:2], r["slug"], flush=True)
json.dump(out, open(S + "/gapcheck.json", "w"), indent=1)
print("DONE", len(out))
