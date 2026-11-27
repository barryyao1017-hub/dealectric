"""`claude -p` calls for the weekly upkeep (plan usage, no API spend), with the token use of every call added up so the
run's report can say what it cost. Isolated from the repo's CLAUDE.md and settings (evallib.CLI_ISOLATION)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "growth" / "evals"))
import evallib as E  # noqa: E402

CHEAP = [("claude-sonnet-5-5", None)]                                   # reading a page's stock notes
DEEP = [("claude-fable-5-2", "high"), ("claude-opus-5-5", "high")]      # research and page rewrites (Barry 11-17: research on Fable)
USAGE: dict = {}
_out_of_usage: set[str] = set()
LIMIT = re.compile(r"usage limit|limit reached|reached your \w+ limit|out of (extra )?usage|weekly limit|session limit|usage credits", re.I)


def ask(prompt: str, models=CHEAP, schema: dict | None = None, tools: list[str] | None = None,
        allowed: list[str] | None = None, timeout: int = 3600, system: str | None = None) -> dict:
    """One call; returns the JSON object the model answered with, or {"status": "error", "reason": ...}."""
    exe = E.claude_cli()
    if not exe:
        return {"status": "error", "reason": "claude CLI not found"}
    last = {"status": "error", "reason": "no model answered"}
    for model, effort in models:
        if model in _out_of_usage:
            continue
        cmd = [exe, "-p", prompt, "--model", model, "--output-format", "json"]
        if effort:
            cmd += ["--effort", effort]
        if system:
            cmd += ["--system-prompt", system]
        if schema:
            cmd += ["--json-schema", json.dumps(schema)]
        cmd += (["--tools", ",".join(tools)] + (["--allowedTools", *allowed] if allowed else [])) if tools else ["--tools", ""]
        d = {}
        for attempt in range(4):
            try:
                p = subprocess.run(cmd + list(E.CLI_ISOLATION), capture_output=True, text=True, timeout=timeout, cwd=E.cli_cwd(),
                                   env={**__import__('os').environ, 'AMZ_CHROME': '1'})   # amzcheck.py reads Amazon in the Agent Chrome
                d = json.loads(p.stdout)
            except subprocess.TimeoutExpired:
                d = {"is_error": True, "result": f"timed out after {timeout} s"}
            except ValueError:
                d = {"is_error": True, "result": (p.stderr or p.stdout)[-600:]}
            msg = str(d.get("result") or "")
            if d.get("is_error") and re.search(r"overloaded|\b429\b|rate limit|try again", msg, re.I) and not LIMIT.search(msg):
                time.sleep(90 * (attempt + 1))
                continue
            break
        msg = str(d.get("result") or "")
        E.add_usage(USAGE.setdefault(model, {}), d.get("usage") or {}, d.get("total_cost_usd"))
        if d.get("is_error") and LIMIT.search(msg):
            _out_of_usage.add(model)
            last = {"status": "error", "reason": msg[:300], "model": model}
            continue
        if d.get("is_error"):
            return {"status": "error", "reason": msg[:400], "model": model}
        out = d.get("structured_output")
        if out is None:
            dec = json.JSONDecoder()
            for i in [m.start() for m in re.finditer(r"\{", msg)][:60]:
                try:
                    obj, _ = dec.raw_decode(msg[i:])
                except ValueError:
                    continue
                if isinstance(obj, dict):
                    out = obj
                    break
        if not isinstance(out, dict):
            return {"status": "error", "reason": "no JSON in the reply", "raw": msg[-1500:], "model": model}
        out.setdefault("_model", model)
        return out
    return last


def usage_line() -> str:
    parts = []
    for m, u in USAGE.items():
        fresh = sum(u.get(k, 0) for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens"))
        parts.append(f"{m}: {u.get('calls', 0)} calls, {fresh:,} new tokens + {u.get('cache_read_input_tokens', 0):,} cache reads")
    return "; ".join(parts) or "no model calls"
