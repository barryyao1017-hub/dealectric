#!/usr/bin/env python3.12
"""Google Search Console URL inspection + Request indexing for one URL, in the agent's Chrome (localhost:9222, signed in
as barrryyao). Promote tier 2 (chatgpt-discoverability skill, step 7b).

    python3.12 tools/gscindex.py https://dealectric.com/<slug> [--skip-indexed]

The tab is brought to the front (a background tab never focuses the inspect box), the URL is typed into the property
home's inspect bar (the direct /search-console/inspect URL 404s), and the button is pressed with CDP mouse events (a
JS click does nothing). Prints Google's status line and the result ("Indexing requested ... priority crawl queue")."""
import sys, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import codesweep as C
url = next(a for a in sys.argv[1:] if not a.startswith("--"))
# authuser picks barrryyao, the property's owner: the agent's Chrome holds more than one Google account, and the default
# one gets "you don't have access to this property" (2026-11-02)
t = C.Tab("https://search.google.com/search-console?resource_id=sc-domain%3Adealectric.com&authuser=barrryyao%40gmail.com")
def click_xy(x, y):
    for typ in ("mousePressed", "mouseReleased"):
        t.call("Input.dispatchMouseEvent", type=typ, x=x, y=y, button="left", clickCount=1)
def find(js):
    return t.eval(js)
t.call("Page.bringToFront")
time.sleep(10)
print("page:", t.eval("document.title"), t.eval("location.href")[:100])
inp = t.eval("""(()=>{const i=[...document.querySelectorAll('input')].find(e=>/inspect/i.test(e.getAttribute('aria-label')||e.placeholder||''));
 if(!i) return null; const r=i.getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height/2]})()""")
print("input at", inp)
if not inp: sys.exit(1)
click_xy(*inp); time.sleep(0.5)
t.eval("(()=>{const i=[...document.querySelectorAll('input')].find(e=>/inspect/i.test(e.getAttribute('aria-label')||e.placeholder||'')); i.focus(); return 1})()")
t.call("Input.insertText", text=url); time.sleep(0.3)
for typ in ("keyDown", "keyUp"):
    t.call("Input.dispatchKeyEvent", type=typ, key="Enter", code="Enter", windowsVirtualKeyCode=13, nativeVirtualKeyCode=13, **({"text": "\r"} if typ == "keyDown" else {}))
time.sleep(2)
print("after enter:", t.eval("location.href")[:160], "| input value:", t.eval("(document.activeElement||{}).value"))
for i in range(40):
    time.sleep(3)
    txt = t.eval("document.body.innerText")
    if "REQUEST INDEXING" in txt.upper():
        break
print("status:", [l for l in txt.splitlines() if any(k in l for k in ("URL is", "not on Google", "on Google", "unknown"))][:4])
if "--skip-indexed" in sys.argv and any(l.strip() == "URL is on Google" for l in txt.splitlines()):
    print("result: skipped, already on Google (no quota spent)")   # a recrawl request costs a slot (2026-11-07: tn438)
    sys.exit(0)
btn = t.eval("""(()=>{const b=[...document.querySelectorAll('span,div,button')].filter(e=>e.innerText&&e.innerText.trim().toUpperCase()==='REQUEST INDEXING'&&e.children.length===0).pop();
 if(!b) return null; b.scrollIntoView({block:'center'}); const r=b.getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height/2]})()""")
print("button at", btn)
if not btn: print(txt[-1500:])
if not btn: sys.exit(2)
time.sleep(1); click_xy(*btn)
for i in range(40):
    time.sleep(3)
    txt = t.eval("document.body.innerText")
    if "Indexing requested" in txt or "added to a priority crawl queue" in txt or "Quota exceeded" in txt:
        break
print("result:", [l for l in txt.splitlines() if any(k in l for k in ("Indexing requested", "priority crawl", "Quota", "error"))][:3])
t.close()
