#!/usr/bin/env python3.12
"""Read store product pages in a background Agent Chrome tab (curl gets a 403 challenge) and save their visible text.
    python3.12 growth/focus/offers/readpages.py <out dir> <url> [<url> ...]
"""
import sys, time, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import codesweep as C
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
t = C.Tab("about:blank"); t.call("Page.enable")
try:
    for u in sys.argv[2:]:
        name = re.sub(r"[^a-z0-9]+", "-", u.split("/products/")[-1].lower())[:110]
        t.call("Page.navigate", url=u)
        txt = ""
        for _ in range(12):
            time.sleep(2.5)
            try:
                txt = t.eval("document.readyState=='complete' ? document.body.innerText : ''") or ""
            except Exception:
                txt = ""
            if len(txt) > 1500: break
        time.sleep(2)
        txt = t.eval("document.body.innerText") or ""
        (out / f"{name}.txt").write_text(txt)
        print(len(txt), t.eval("document.title")[:70], "|", name[:60], flush=True)
        time.sleep(3)
finally:
    t.close()
