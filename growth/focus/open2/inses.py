#!/usr/bin/env python3.12
"""In-session research steps for the open2 pages while `claude -p` is at its weekly limit (until 2026-11-18 16:00 PT).
abpage's prompts, unchanged, are written to files that in-session Opus 5.5 subagents read; their JSON answers are saved
back into growth/focus/ab/<folder>/ exactly where abpage.research would put them.

    inses.py angles <folder> E F        write angle prompts      -> <scratch>/<folder>-angle-<X>.txt
    inses.py save-angles <folder>       read <scratch>/<folder>-out-<X>.json into angle-<X>.json
    inses.py reuse <folder> <src dir>   copy existing angle reports (paid for earlier) into the folder
    inses.py compose <folder>           write the compose prompt  -> <scratch>/<folder>-compose.txt
    inses.py save-compose <folder>; inses.py verify <folder>; inses.py save-verify <folder>   (assembles draft.json)
"""
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "src"))
import pages2  # noqa: F401,E402  (registers the pages)
import abpage as A  # noqa: E402

S = Path("/private/tmp/claude-502/-Users-j0y0825-code-dealectric--claude-worktrees-open-query-pages-56ca47/9d747739-0114-401f-b740-2701d9e8c810/scratchpad/inses")
S.mkdir(parents=True, exist_ok=True)
META = {"model": "claude-opus-5-5 (in-session subagent; claude -p at its weekly limit until 2026-11-18)"}


def hq(f):
    h = A.jload(A.AB / f / "harvest.json")
    return h, A.query_for(f, h)


def angles_present(f):
    d = A.AB / f
    return {x: {k: v for k, v in A.jload(d / f"angle-{x}.json", {}).items() if k != "_meta"}
            for x in "ABCDEF" if (d / f"angle-{x}.json").exists() and A.jload(d / f"angle-{x}.json", {}).get("findings")}


def main():
    cmd, f, *rest = sys.argv[1:]
    d = A.AB / f
    if cmd == "angles":
        h, q = hq(f)
        for x in rest:
            (S / f"{f}-angle-{x}.txt").write_text(A.angle_prompt(f, x, h, q))
        print([str(S / f"{f}-angle-{x}.txt") for x in rest])
    elif cmd == "save-angles":
        for p in sorted(S.glob(f"{f}-out-[A-F].json")):
            x = p.stem[-1]
            o = json.loads(p.read_text()); o["_meta"] = META
            A.jsave(d / f"angle-{x}.json", o)
            print(x, o.get("standout"), len(o.get("findings") or []))
    elif cmd == "reuse":
        src = Path(rest[0])
        for p in sorted(src.glob("angle-*.json")):
            if A.jload(p, {}).get("findings"):
                shutil.copy(p, d / p.name)
        print(sorted(angles_present(f)))
    elif cmd == "compose":
        h, q = hq(f)
        (S / f"{f}-compose.txt").write_text(A.compose_prompt(f, h, q, angles_present(f), True))
        print(S / f"{f}-compose.txt", sorted(angles_present(f)))
    elif cmd == "save-compose":
        c = json.loads((S / f"{f}-out-compose.json").read_text()); c["_meta"] = META
        A.jsave(d / "compose.json", c)
        print(c.get("status"), c.get("angle"), c.get("slug"), (c.get("page") or {}).get("title"))
        if c.get("status") == "ok":
            (S / f"{f}-verify.txt").write_text(A.verify_prompt({k: v for k, v in c.items() if k != "_meta"}))
    elif cmd == "save-verify":
        import products as P, gaps
        ver = json.loads((S / f"{f}-out-verify.json").read_text()); ver["_meta"] = META
        A.jsave(d / "verify.json", ver)
        comp = A.jload(d / "compose.json"); h, q = hq(f)
        draft = ver["draft"]
        taken = {p["slug"] for p in P.PRODUCTS} | {g["slug"] for g in gaps.GAP_PAGES}
        assert draft["slug"] not in taken and re.fullmatch(r"[a-z0-9-]{8,90}", draft["slug"]), draft["slug"]
        draft.update({"status": "ok", "new_page": True, "searched_as": h["searched_as"], "angle": comp.get("angle"),
                      "why_angle": comp.get("why_angle"), "query": q, "verified_changes": len(ver.get("changed") or []),
                      "verified_removed": len(ver.get("removed") or []),
                      "research_note": "claude -p at its weekly limit; angles, compose and verify ran as in-session Opus 5.5 subagents with abpage's prompts"})
        A.jsave(d / "draft.json", draft)
        print(draft["slug"], [r.get("slug") or r.get("model") for r in draft["page"]["rows"]])


if __name__ == "__main__":
    main()
