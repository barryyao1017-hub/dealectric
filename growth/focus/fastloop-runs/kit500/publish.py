#!/usr/bin/env python3.12
"""kit500 run, step 7: write the winning draft into src/gaps.py (G13) and add the tier-1 internal links (home, the
portable power stations guide, the solar-kits page, /discount-codes). Usage: publish.py <draft key>. Idempotent: an
existing G13 record is replaced."""
import importlib.util, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
spec = importlib.util.spec_from_file_location("drafts", HERE / "drafts.py")
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
sys.path.insert(0, str(REPO / "growth" / "focus" / "fastloop-runs" / "esr-25w"))
key = sys.argv[1]
rec = D.draft(key)


def lit(rec: dict) -> str:
    out = ["{" + f'"slug": {rec["slug"]!r}, "question": {rec["question"]!r}, "lead_first": True,'.replace("'", '"')]
    for k in ("title", "h1", "desc"):
        out.append(f' "{k}": {rec[k]!r},')
    out.append(f' "intro": """{rec["intro"]}""",')
    out.append(' "columns": [' + ", ".join(f"({a!r}, {b!r})" for a, b in rec["columns"]) + "],")
    out.append(' "rows": [')
    out += [f"  {r!r}," for r in rec["rows"]]
    out.append(" ],")
    out.append(f' "after": """{rec["after"]}""",')
    out.append(' "sources": [')
    out += [f"  ({a!r}, {b!r})," for a, b in rec["sources"]]
    out.append(" ],")
    out.append(f' "published": {rec["published"]!r}, "checked": {rec["checked"]!r}}},')
    return "\n".join(out)


HEADER = ("# ---------------- G13: best solar generator kit under $500 (kit500 run, 2026-11-02) ----------------\n"
          "# ChatGPT's searches (11-02 harvest, growth/evals/runs/2026-11-02-harvest-kit500): 'best portable solar generator kits\n"
          "# under $500 2026 ...'; gap vote open 3/3 on five of six brand-free searches. Facts and sources:\n"
          "# growth/focus/fastloop-runs/kit500/open-concern.md; draft " + key + " of drafts.py (scores in that folder).\n"
          "# Run log: claude.ai/artifact/91GeUEUX5cEe9fkXdJdNeD.\n")

g = REPO / "src" / "gaps.py"
s = g.read_text()
s = re.sub(r"# -{16} G13:.*?\"checked\": \"[0-9-]+\"\},\n", "", s, flags=re.S)   # replace an earlier G13
end = s.rindex("\n]")
s = s[:end] + "\n\n" + HEADER + lit(rec) + s[end:]
g.write_text(s)

LINK = '<a href="/best-solar-generator-kit-under-500">the best solar generator kit under $500</a>'
c = REPO / "src" / "content.py"
t = c.read_text()
if "/best-solar-generator-kit-under-500" not in t:
    home = '<p class="small">New comparison: <a href="/iphone-17-25w-wireless-charger">'
    assert t.count(home) == 1
    t = t.replace(home, f'<p class="small">New comparison: {LINK}, power station and solar panel bundles priced, with how long the panel takes to refill the battery.</p>\n' + home)
    guide = '<p class="small">Compared across brands: <a href="/compare/solar-watts-to-recharge-power-station/">'
    assert t.count(guide) == 1
    t = t.replace(guide, f'<p class="small">On a budget: {LINK}, with the watt hours and solar panel each kit includes.</p>\n' + guide)
    c.write_text(t)
b = REPO / "src" / "build.py"
t = b.read_text()
if "/best-solar-generator-kit-under-500" not in t:
    a = '<a href="/solar-generator-with-panels-included">the best solar generator with panels included</a> (portable power station and solar panel kits), '
    assert t.count(a) == 1
    t = t.replace(a, a + LINK + ", ")
    b.write_text(t)
gp = REPO / "src" / "gaps.py"
t = gp.read_text()
if 'href="/best-solar-generator-kit-under-500"' not in t.split("# ---------------- G13:")[0]:
    a = "Smallest budgets: <strong>ALLPOWERS VOLIX P300 + 100 W</strong>"
    assert t.count(a) == 1
    t = t.replace(a, 'Under $500, compared on its own page: <a href="/best-solar-generator-kit-under-500">solar generator kits under $500</a>. ' + a)
    gp.write_text(t)
print(f"G13 written from draft {key}; links in place")
