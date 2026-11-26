#!/usr/bin/env python3.12
"""Is ChatGPT signed in, in the Agent Chrome (9222)? If not, sign back in with "Continue with Google" as
barrryyao@gmail.com (CLAUDE.md "Logins": sign in without asking; never type credentials). Exit 0 signed in,
1 could not sign in, 2 Google asked for a password or another step (stop and tell Barry)."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "evals"))
import ui

ACCOUNT = "barrryyao@gmail.com"


def session(t) -> dict:
    try:
        return json.loads(t.eval("fetch('/api/auth/session').then(r=>r.text())") or "{}")
    except Exception:  # noqa: BLE001
        return {}


def click(t, js_find: str) -> bool:
    b = t.eval(js_find)
    if not b:
        return False
    b = json.loads(b)
    t.call("Input.dispatchMouseEvent", type="mouseMoved", x=b["x"], y=b["y"], button="none")
    for k in ("mousePressed", "mouseReleased"):
        t.call("Input.dispatchMouseEvent", type=k, x=b["x"], y=b["y"], button="left", clickCount=1)
    return True


def main() -> int:
    t = ui.Tab("about:blank")
    try:
        t.call("Page.enable")
        t.navigate("https://chatgpt.com/")
        time.sleep(8)
        if (session(t).get("user") or {}).get("email"):
            print("signed in")
            return 0
        t.navigate("https://chatgpt.com/auth/login")
        time.sleep(10)
        if not click(t, "(()=>{const e=[...document.querySelectorAll('button,a')].find(e=>/Continue with Google/.test(e.innerText||''));if(!e)return null;const r=e.getBoundingClientRect();return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2})})()"):
            print("no Continue with Google button")
            return 1
        time.sleep(9)
        if "accounts.google.com" in (t.eval("location.href") or ""):
            if not click(t, "(()=>{const e=[...document.querySelectorAll('[data-identifier]')].find(e=>e.getAttribute('data-identifier')===%s);if(!e)return null;const r=e.getBoundingClientRect();return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2})})()" % json.dumps(ACCOUNT)):
                print("Google did not offer", ACCOUNT)
                return 2
            time.sleep(10)
        url = t.eval("location.href") or ""
        if "accounts.google.com" in url:
            print("Google wants another step:", url[:100])
            return 2
        t.navigate("https://chatgpt.com/")
        time.sleep(6)
        email = (session(t).get("user") or {}).get("email")
        print("signed in again as", email if email else "nobody")
        return 0 if email == ACCOUNT else 1
    finally:
        t.close()


if __name__ == "__main__":
    sys.exit(main())
