#!/usr/bin/env python3
"""Claude Code PostToolUse hook (registered in .claude/settings.json, added 2026-10-28): logs the tool calls by which an
agent session in this repo makes an assistant, or itself, touch dealectric.com by hand, outside the eval scripts (which
log their own footprints through evallib.footprint). tools/fetchwho.py reads the entries ("source": "hook").

Logged, and nothing else:
  * WebFetch of a dealectric.com URL (settings `if` gate: WebFetch(domain:dealectric.com));
  * a Bash command that names a dealectric.com URL (`if` gate: Bash(*dealectric.com*)) and runs a network client
    (curl, wget, http ...) as a command word outside quotes, unless it runs one of our scripts (they log themselves or
    send their own user agent) or starts a child `claude` session (whose own tool calls get logged);
  * a browser-tool navigation (built-in browser or Claude in Chrome) to dealectric.com, or to the start of a chat on
    an assistant app (chatgpt.com, claude.ai, perplexity.ai, gemini.google.com, grok.com, copilot.microsoft.com); account,
    settings and login pages are not chats.
Only for sessions whose working directory is a checkout of this repo (docs/CNAME says dealectric.com); entries go to the
main checkout's growth/evals/footprint.jsonl. Standard library only, no network, always exits 0 and prints nothing, so it
can never block or slow a tool call (it also runs async).
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

SITE_HOSTS = {"dealectric.com", "www.dealectric.com"}
CHAT_APPS = {"chatgpt.com": "chatgpt-ui", "chat.openai.com": "chatgpt-ui", "claude.ai": "claude-ai", "perplexity.ai": "perplexity-ui",
             "gemini.google.com": "gemini-ui", "grok.com": "grok-ui", "copilot.microsoft.com": "copilot-ui"}
NOT_A_CHAT = re.compile(r"^/(auth|login|logout|signup|sign-in|settings|account|admin|pricing|plans|upgrade|download|gpts|apps|"
                        r"library|images|codex|sora|backend-api|api|oauth|cdn-cgi)\b", re.I)
SITE_URL = re.compile(r"https?://(?:www\.)?dealectric\.com[^\s'\"<>)\]}]*", re.I)
NET_CLIENT = re.compile(r"(^|[\s;&|(`$])(curl|wget|http|https|xh|httpie|lynx|links|w3m)(\s|$)")
OWN_SCRIPTS = re.compile(r"(growth/evals|tools)/[\w.-]+\.(py|sh)\b")
CHILD_CLAUDE = re.compile(r"(^|[\s;&|(`$])claude(\s|$)")   # a child Claude session logs its own tool calls
QUOTED = re.compile(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"")
BROWSER_TOOLS = {"mcp__Claude_Browser__navigate", "mcp__Claude_Browser__preview_start", "mcp__claude-in-chrome__navigate"}
BATCH_TOOLS = {"mcp__Claude_Browser__browser_batch", "mcp__claude-in-chrome__browser_batch"}


def host(url: str) -> str:
    try:
        h = (urlparse(url if "://" in url else "https://" + url).hostname or "").lower()
    except ValueError:
        return ""
    return h


def classify_url(url: str) -> tuple[str, str, str | None] | None:
    """(kind, app, prompt) for a navigation worth logging, else None."""
    if not url or url in ("back", "forward"):
        return None
    h = host(url)
    if h in SITE_HOSTS:
        return "fetch", "browser", None
    app = CHAT_APPS.get(h[4:] if h.startswith("www.") else h)
    if not app:
        return None
    p = urlparse(url if "://" in url else "https://" + url)
    if NOT_A_CHAT.match(p.path or "/") or "settings" in (p.fragment or "").lower():
        return None
    q = parse_qs(p.query)
    return "chat", app, ((q.get("q") or q.get("prompt") or [None])[0] or None)


def events(tool: str, inp: dict) -> list[dict]:
    out = []
    if tool == "WebFetch":
        url = inp.get("url") or ""
        if host(url) in SITE_HOSTS:
            out.append({"kind": "fetch", "app": "claude-code", "fetched": [url]})
    elif tool == "Bash":
        cmd = inp.get("command") or ""
        urls = SITE_URL.findall(cmd)
        bare = QUOTED.sub(" ", cmd)   # the client must be a command word, not text inside a quoted prompt or message
        if urls and NET_CLIENT.search(bare) and not OWN_SCRIPTS.search(bare) and not CHILD_CLAUDE.search(bare):
            out.append({"kind": "fetch", "app": "direct-fetch", "fetched": list(dict.fromkeys(urls)), "command": cmd[:300]})
    elif tool in BROWSER_TOOLS:
        c = classify_url(inp.get("url") or "")
        if c:
            out.append({"kind": c[0], "app": c[1], "prompt": c[2], "fetched": [inp["url"]] if c[0] == "fetch" else []})
    elif tool in BATCH_TOOLS:
        chat = None
        for a in inp.get("actions") or []:
            name, ai = a.get("name"), a.get("input") or {}
            if name == "navigate":
                c = classify_url(ai.get("url") or "")
                if c:
                    chat = {"kind": c[0], "app": c[1], "prompt": c[2], "fetched": [ai["url"]] if c[0] == "fetch" else []}
                    out.append(chat)
            elif name == "computer" and ai.get("action") == "type" and chat and chat["kind"] == "chat" and not chat.get("prompt"):
                chat["prompt"] = ai.get("text")
    return out


def footprint_file(cwd: str) -> Path | None:
    """The main checkout's footprint log when cwd is inside a checkout of this repo, else None."""
    try:
        common = subprocess.run(["git", "-C", cwd, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                capture_output=True, text=True, timeout=5).stdout.strip()
        top = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    if not common or not top:
        return None
    try:
        if (Path(top) / "docs" / "CNAME").read_text().strip() != "dealectric.com":
            return None
    except OSError:
        return None
    d = Path(common).parent / "growth" / "evals"
    return d / "footprint.jsonl" if d.is_dir() else None


def main() -> None:
    try:
        data = json.loads(sys.stdin.read() or "{}")
        evs = events(data.get("tool_name") or "", data.get("tool_input") or {})
        if not evs:
            return
        path = footprint_file(data.get("cwd") or ".")
        if not path:
            return
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        lines = []
        for e in evs:
            lines.append(json.dumps({"script": "claude-code-hook", "source": "hook", "via": data.get("tool_name"), "run_id": None,
                                     "app": e["app"], "kind": e["kind"], "account": None, "temporary_chat": None,
                                     "started_at": now, "finished_at": now, "prompt_id": None,
                                     "prompt": (e.get("prompt") or "")[:300] or None, "cited": [], "fetched": e.get("fetched") or [],
                                     "retrieved": [], "egress_country": None, "error": None, "session_id": data.get("session_id"),
                                     "cwd": data.get("cwd"), **({"command": e["command"]} if e.get("command") else {})},
                                    ensure_ascii=False) + "\n")
        with open(path, "a", encoding="utf-8") as f:
            f.write("".join(lines))
    except Exception:  # noqa: BLE001  (a hook must never fail a tool call)
        pass


if __name__ == "__main__":
    main()
