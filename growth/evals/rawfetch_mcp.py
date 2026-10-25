#!/usr/bin/env python3.12
"""A one-tool MCP server (stdio) for the copy-line study (claudeline.py): `fetch(url)` returns the page as plain text
with links kept as [text](url), unsummarised, the way claude.ai's web fetch hands a page to the model. Claude Code's own
WebFetch passes pages through a summarising model first, which can drop a sentence before the answering model sees it;
this server is the raw tool channel to compare against.
"""
import html
import json
import re
import ssl
import sys
import urllib.request

try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem")

UA = "Mozilla/5.0 (compatible; Claude-User; +https://www.anthropic.com) dealectric-claudeline"
TOOL = {"name": "fetch", "description": "Fetch a web page and return its full text (links as [text](url)).",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string", "description": "The URL to fetch"}},
                        "required": ["url"]}}


def page_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", raw)
    raw = re.sub(r'(?is)<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', lambda m: f"[{re.sub(r'<[^>]+>', '', m[2]).strip()}]({m[1]})", raw)
    raw = re.sub(r"(?is)<br\s*/?>|</(p|div|li|h[1-6]|tr|section|article|dt|dd|header|footer|nav)>", "\n", raw)
    t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en"})
    with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
        body = r.read(3_000_000).decode("utf-8", "replace")
        ctype = r.headers.get("content-type", "")
    text = body if "json" in ctype or "text/plain" in ctype else page_text(body)
    return text[:60_000]


def reply(id_, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": id_}
    msg.update({"error": error} if error else {"result": result})
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


for line in sys.stdin:
    try:
        req = json.loads(line)
    except ValueError:
        continue
    m, id_ = req.get("method"), req.get("id")
    if id_ is None:
        continue   # notifications
    if m == "initialize":
        reply(id_, {"protocolVersion": req["params"].get("protocolVersion", "2025-06-18"), "capabilities": {"tools": {}},
                    "serverInfo": {"name": "rawfetch", "version": "1"}})
    elif m == "tools/list":
        reply(id_, {"tools": [TOOL]})
    elif m == "tools/call":
        try:
            text = fetch(req["params"]["arguments"]["url"])
            reply(id_, {"content": [{"type": "text", "text": text}]})
        except Exception as e:  # noqa: BLE001
            reply(id_, {"content": [{"type": "text", "text": f"Fetch failed: {e}"}], "isError": True})
    elif m == "ping":
        reply(id_, {})
    else:
        reply(id_, error={"code": -32601, "message": f"unknown method {m}"})
