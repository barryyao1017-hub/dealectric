#!/usr/bin/env python3.12
"""Panel probe (Barry, 2026-11-15): a product row ChatGPT typed itself (no inline catalog card) still shows the product
name as a link. Clicking it opens ChatGPT's own product panel. Does that panel offer a seller, a price and a Visit
button, i.e. is the product in the catalog after all?

    python3.12 growth/evals/panelprobe.py --run-id 2026-11-15-panelprobe --queries <file.jsonl> [--max-clicks 5]

One plain temporary chat per query (Agent Chrome, ui.ask_chatgpt, search not forced). After the answer settles, each
typed product name is clicked with a real mouse event; the panel's text, any price and "Visit" button, and a
screenshot are saved under runs/<run>/. Stops at the first answer that is not from --model.
"""
from __future__ import annotations

import argparse, base64, json, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ui  # noqa: E402
import evallib as E  # noqa: E402
import openscan as O  # noqa: E402

PANEL_JS = """(() => { const n=%s; const c=[...document.querySelectorAll('div,aside,section')].filter(e=>{const r=e.getBoundingClientRect();
  const cs=getComputedStyle(e); return r.width>300&&r.width<700&&r.height>300&&r.x>window.innerWidth*0.45&&(e.innerText||'').includes(n.slice(0,18))});
  c.sort((a,b)=>a.innerText.length-b.innerText.length); if(!c.length) return null; const e=c[0];
  return JSON.stringify({text:(e.innerText||'').slice(0,2500), buttons:[...e.querySelectorAll('button,a')].map(b=>(b.innerText||'').trim()).filter(Boolean).slice(0,30),
    links:[...e.querySelectorAll('a[href]')].map(a=>a.href.slice(0,200)).slice(0,20)}) })()"""
FIND_JS = """(() => { const n=%s; const vis=e=>{const r=e.getBoundingClientRect(); return r.width>0&&r.height>0};
  let els=[...document.querySelectorAll('main *')].filter(e=>vis(e)&&(e.innerText||'').trim()===n);
  if(!els.length) els=[...document.querySelectorAll('main a, main button, main span, main strong, main td, main h3')].filter(e=>vis(e)&&(e.innerText||'').includes(n)&&(e.innerText||'').length<n.length+40);
  if(!els.length) return null;
  const depth=e=>{let d=0;while(e.parentElement){d++;e=e.parentElement}return d};
  els.sort((a,b)=>depth(b)-depth(a));                       // deepest element that carries the name
  const inRow=els.find(e=>{let p=e;for(let i=0;i<8&&p;i++){p=p.parentElement;if(p&&p.querySelector&&p.querySelector('img'))return true}return false});
  const el=inRow||els[0]; el.scrollIntoView({block:'center'}); const r=el.getBoundingClientRect();
  return JSON.stringify({x:r.x,y:r.y,w:r.width,h:r.height,n:els.length,tag:el.tagName}) })()"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", default="2026-11-15-panelprobe")
    ap.add_argument("--queries", required=True)
    ap.add_argument("--max-clicks", type=int, default=5)
    ap.add_argument("--model", default="gpt-6-2")   # gpt-6.2 answers ChatGPT app chats since ~2026-11-23
    args = ap.parse_args()
    out = E.RUNS_DIR / args.run_id
    out.mkdir(parents=True, exist_ok=True)
    res_f = out / "panels.jsonl"
    done = {json.loads(l)["qid"] for l in res_f.read_text().splitlines()} if res_f.exists() else set()
    kept, orig_close = [], ui.Tab.close
    ui.Tab.close = lambda self: kept.append(self)      # keep the chat's tab open for the clicks
    for q in [json.loads(l) for l in Path(args.queries).read_text().splitlines() if l.strip()]:
        if q["qid"] in done:
            continue
        rec = ui.ask_chatgpt(q["prompt"], out / f"{q['qid']}.jpg", fp={"run_id": args.run_id, "prompt_id": q["qid"], "script": "panelprobe.py"}, search=False)
        tab = kept[-1]
        if (rec.get("answer_model") or "") != args.model:
            orig_close(tab)
            print("stopped: answer from", rec.get("answer_model"))
            return 3
        rd = O.reading(rec)
        (out / f"{q['qid']}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False, default=str))
        panels = []
        for name in (q.get("names") or rd["typed_names"])[: args.max_clicks]:      # "names": products to look up, whatever the row type
            box = tab.eval(FIND_JS % json.dumps(name))
            if not box:
                panels.append({"name": name, "found": False})
                continue
            b = json.loads(box)
            x, y = b["x"] + min(b["w"] / 2, 60), b["y"] + b["h"] / 2
            tab.call("Input.dispatchMouseEvent", type="mouseMoved", x=x, y=y, button="none")
            time.sleep(0.5)
            for t in ("mousePressed", "mouseReleased"):
                tab.call("Input.dispatchMouseEvent", type=t, x=x, y=y, button="left", clickCount=1)
            time.sleep(8)
            raw = tab.eval(PANEL_JS % json.dumps(name))
            p = json.loads(raw) if raw else {"text": "", "buttons": [], "links": []}
            price = re.findall(r"\$\s?[\d,]+(?:\.\d\d)?", p["text"])
            visit = any(re.search(r"\bVisit\b", bt) for bt in p["buttons"])      # a seller row reads "<seller>\n<price>\nVisit"
            sellers = [bt.split("\n")[0] for bt in p["buttons"] if re.search(r"\bVisit\b", bt)]
            shot = out / f"{q['qid']}-{len(panels)}.jpg"
            try:
                shot.write_bytes(base64.b64decode(tab.call("Page.captureScreenshot", format="jpeg", quality=60)["data"]))
            except Exception:  # noqa: BLE001
                pass
            panels.append({"name": name, "found": True, "panel": bool(raw), "prices": price[:6], "visit": visit, "sellers": sellers, "buttons": p["buttons"][:12],
                           "text": p["text"][:900], "links": p["links"][:8], "shot": shot.name})
            for t in ("keyDown", "keyUp"):
                tab.call("Input.dispatchKeyEvent", type=t, key="Escape", code="Escape", windowsVirtualKeyCode=27)
            time.sleep(1.5)
        orig_close(tab)
        row = {"qid": q["qid"], "prompt": q["prompt"], "carded": rd["carded"], "typed": rd["typed"], "panels": panels}
        with open(res_f, "a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(q["qid"], f"carded={rd['carded']} typed={rd['typed']}", [(p["name"][:28], "offer" if p.get("visit") else "no offer" if p.get("panel") else "no panel") for p in panels], flush=True)
        time.sleep(8)
    return 0


if __name__ == "__main__":
    sys.exit(main())
