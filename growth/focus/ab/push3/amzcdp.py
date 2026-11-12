"""Read Amazon titles in a background Agent Chrome tab. args: jobs.json out.jsonl. job: {"kind":"asin"|"search","q":...}"""
import json, sys, time, urllib.parse
sys.path.insert(0, "/Users/j0y0825/code/dealectric/growth/evals")
from ui import Tab
jobs = json.load(open(sys.argv[1])); out = open(sys.argv[2], "a")
tab = Tab()
JS_ASIN = """(()=>{const t=document.querySelector('#productTitle');const b=document.querySelector('#bylineInfo');
return {title:t?t.innerText.trim():null, byline:b?b.innerText.trim():null, captcha:/captcha|robot/i.test(document.title+document.body.innerText.slice(0,500)), page:document.title}})()"""
JS_SEARCH = """(()=>{return [...document.querySelectorAll('div[data-asin][data-component-type="s-search-result"]')].slice(0,8).map(d=>({asin:d.dataset.asin,title:(d.querySelector('h2')||{}).innerText||'', sponsored:/Sponsored/.test(d.innerText.slice(0,200))}))})()"""
try:
    for j in jobs:
        url = f"https://www.amazon.com/dp/{j['q']}" if j["kind"] == "asin" else "https://www.amazon.com/s?k=" + urllib.parse.quote(j["q"])
        tab.navigate(url); time.sleep(6)
        r = tab.eval(JS_ASIN if j["kind"] == "asin" else JS_SEARCH)
        out.write(json.dumps({**j, "res": r}) + "\n"); out.flush()
        time.sleep(4)
finally:
    tab.close()
