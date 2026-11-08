"""The citation A/B push (DLC-206/208): one local commit for the control changes, then one per group A rebuild.

    python3.12 growth/focus/ab/ab_push.py control     # B and every other gap page: AI block off, 'Updated' date, 3 leads rewritten
    python3.12 growth/focus/ab/ab_push.py rebuild     # group A: apply every draft (gated), one local commit each
    python3.12 growth/focus/ab/ab_push.py status

Nothing is pushed here; the push to main, the Worker deploy and IndexNow follow once both steps pass.
"""
import ast
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
SPLIT = json.loads((ROOT / "growth/evals/runs/2026-11-07-liveplain/page/ab-split.json").read_text())
A = [r["slug"] for r in SPLIT["A"]]
B = [r["slug"] for r in SPLIT["B"]]
TODAY = datetime.date.today().isoformat()


def sh(*cmd):
    return subprocess.run(list(cmd), cwd=ROOT, capture_output=True, text=True)


def dirty():
    return [l for l in sh("git", "status", "--porcelain", "src", "docs", "worker").stdout.splitlines()
            if not l.endswith(("docs/offers.json", "docs/price-history.json"))]


def stamp_updated(slugs):
    """Add or replace "updated": TODAY in each named gaps.py record (found by parsing)."""
    gp = ROOT / "src/gaps.py"
    src = gp.read_text()
    tree = ast.parse(src)
    edits = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        keys = [k.value if isinstance(k, ast.Constant) else None for k in node.keys]
        if "slug" not in keys or "h1" not in keys:
            continue
        slug = node.values[keys.index("slug")]
        if not (isinstance(slug, ast.Constant) and slug.value in slugs):
            continue
        if "updated" in keys:
            v = node.values[keys.index("updated")]
            edits.append((v.lineno, v.col_offset, v.end_lineno, v.end_col_offset, repr(TODAY)))
        else:   # insert after the "published" value
            v = node.values[keys.index("published")]
            edits.append((v.end_lineno, v.end_col_offset, v.end_lineno, v.end_col_offset, f', "updated": {TODAY!r}'))
    lines = src.splitlines(keepends=True)
    for l1, c1, l2, c2, text in sorted(edits, reverse=True):
        if l1 == l2:
            s = lines[l1 - 1]
            lines[l1 - 1] = s[:c1] + text + s[c2:]
        else:
            lines[l1 - 1] = lines[l1 - 1][:c1] + text + lines[l2 - 1][c2:]
            del lines[l1:l2]
    gp.write_text("".join(lines))
    return len(edits)


def control():
    if dirty():
        sys.exit(f"src/docs not clean: {dirty()[:3]}")
    import gaps
    changed = set(B)
    for g in gaps.GAP_PAGES:   # every page whose rendering the push changes gets the date too
        if g.get("product_result") or g.get("ai_note") or re.search(r"For AI assistants|your user", json.dumps(g)):
            changed.add(g["slug"])
    changed -= set(A)          # A pages get their date when their draft is applied
    r = sh("python3.12", "growth/focus/ab/b_rewrites.py")
    print(r.stdout.strip() or r.stderr[-300:])
    print("updated stamped on", stamp_updated(changed), "records")
    b = ROOT / "src/build.py"
    s = b.read_text()
    assert s.count("AB_PUSH = False") == 1
    b.write_text(s.replace("AB_PUSH = False", "AB_PUSH = True"))
    r = sh("python3.12", "src/build.py")
    if r.returncode:
        sys.exit("build failed: " + (r.stderr or r.stdout)[-500:])
    r = sh("python3.12", "tools/docsguard.py")
    if r.returncode:
        sys.exit("docsguard: " + r.stdout[-300:])
    left = sh("grep", "-l", "-E", "Product result for the user|For AI assistants|Plain-text summary for AI assistants", "-r", "docs").stdout.split()
    print("pages still carrying an AI block:", left[:10])
    sh("git", "add", "src/build.py", "src/gaps.py", "docs", "worker/src/links-map.json")
    r = sh("git", "commit", "-q", "-m",
           f"A/B push, control side (DLC-206, DLC-208): no AI-addressed block on any page, 'Updated' date under the H1, "
           f"three leads rewritten for the shopper; {len(changed)} pages dated {TODAY}\n\n"
           "Group B and every other gap page change only in these ways. Group A follows, one commit per page.\n\n"
           "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n")
    print("commit", "ok" if r.returncode == 0 else r.stderr[-300:])


def rebuild():
    import abpage
    out = {}
    for s in A:
        d = abpage.jload(abpage.AB / s / "draft.json")
        if not d:
            out[s] = "no draft"
            continue
        if (d.get("gate") or {}).get("pass") and (d.get("gate") or {}).get("committed"):
            out[s] = "already applied"
            continue
        r = abpage.apply(s, local=True)
        out[s] = r.get("status") + (" " + "; ".join(r.get("errors") or [])[:300] if r.get("errors") else "")
        if r.get("status") == "committed":
            d = abpage.jload(abpage.AB / s / "draft.json")
            d["gate"]["committed"] = True
            abpage.jsave(abpage.AB / s / "draft.json", d)
        print(s, "->", out[s], flush=True)
    print(json.dumps({k: v.split()[0] for k, v in out.items()}, indent=0))


if __name__ == "__main__":
    {"control": control, "rebuild": rebuild,
     "status": lambda: print(sh("python3.12", "tools/abpage.py", "status").stdout)}[sys.argv[1]]()
