#!/bin/zsh
# ask.sh <name> <prompt>: one Claude CLI answer with web search, prints searches, result URLs and the answer
claude -p "$2" --output-format stream-json --verbose --allowedTools WebSearch,WebFetch --tools WebSearch,WebFetch --model claude-sonnet-5-5 --no-session-persistence --setting-sources "" --strict-mcp-config > "$1.jsonl" 2>"$1.err"
python3.12 - "$1.jsonl" <<'PY'
import json, re, sys
for l in open(sys.argv[1]):
    d = json.loads(l)
    if d.get("type") == "assistant":
        for c in d["message"]["content"]:
            if c.get("type") == "tool_use": print("TOOL", c["name"], json.dumps(c["input"])[:160])
    if d.get("type") == "user":
        for c in d["message"].get("content", []):
            if isinstance(c, dict) and c.get("type") == "tool_result":
                t = c.get("content"); t = t if isinstance(t, str) else json.dumps(t)
                print("  urls:", [re.sub(r'^https?://(www\.)?', '', u)[:60] for u in re.findall(r'https?://[^\s"\\)\]]+', t)][:10])
    if d.get("type") == "result": print("ANSWER:", (d.get("result") or "")[:900])
PY
