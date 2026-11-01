#!/usr/bin/env python3.12
"""ESR run, step 7: write the winning draft into src/gaps.py (G06) and add the tier-1 internal links (home, the wireless
charging guide section, /discount-codes). Usage: publish.py <draft key>. Idempotent: an existing G06 record is replaced."""
import importlib.util, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
spec = importlib.util.spec_from_file_location("drafts", HERE / "drafts.py")
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)

key = sys.argv[1]
rec = D.draft(key) if key in "ABC" else D.draft2(key)


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


HEADER = ("# ---------------- G06: which wireless charger gets an iPhone 17 the full 25W (ESR run, 2026-11-01) ----------------\n"
          "# ChatGPT's search (11-01 harvest, growth/evals/runs/2026-11-01-harvest-esr): \"iPhone 17 25W wireless charging requirements\n"
          "# MagSafe Qi2.2 2026\"; gap vote open 3/3. Facts and sources: growth/focus/fastloop-runs/esr-25w/open-concern.md;\n"
          f"# draft {key} of growth/focus/fastloop-runs/esr-25w/drafts.py (scores in that folder). Run log: claude.ai/artifact/T47hmobnM6QfbRUqPFkH7f.\n")

g = REPO / "src" / "gaps.py"
s = g.read_text()
s = re.sub(r"# -{16} G06:.*?\"checked\": \"[0-9-]+\"\},\n", "", s, flags=re.S)   # replace an earlier G06
end = s.rindex("\n]")
s = s[:end] + "\n\n" + HEADER + lit(rec) + s[end:]
g.write_text(s)

LINK = '<a href="/iphone-17-25w-wireless-charger">which wireless charger gets an iPhone 17 the full 25W</a>'
c = REPO / "src" / "content.py"
t = c.read_text()
if "/iphone-17-25w-wireless-charger" not in t:
    home = '<p class="small">New comparison: <a href="/best-2kwh-power-station-for-rv">'
    assert t.count(home) == 1
    t = t.replace(home, f'<p class="small">New comparison: {LINK}, with the 30W adapter rule and why an old MagSafe or Qi2 charger stops at 15W.</p>\n' + home)
    guide = '<p class="small">Compared across brands, with the watts each iPhone gets: <a href="/compare/qi2-vs-qi2-2-vs-magsafe-chargers/">'
    assert t.count(guide) == 1
    t = t.replace(guide, f'<p class="small">iPhone 17 charging slowly on an old wireless charger: {LINK}, and the adapter 25W needs.</p>\n' + guide)
    c.write_text(t)
b = REPO / "src" / "build.py"
t = b.read_text()
if "/iphone-17-25w-wireless-charger" not in t:
    a = ' and <a href="/best-2kwh-power-station-for-rv">the best 2kWh portable power station for an RV</a>.</p>'
    assert t.count(a) == 1
    t = t.replace(a, ', <a href="/best-2kwh-power-station-for-rv">the best 2kWh portable power station for an RV</a> and '
                     '<a href="/iphone-17-25w-wireless-charger">which wireless charger gets an iPhone 17 the full 25W</a>.</p>')
    b.write_text(t)
print(f"G06 written from draft {key}; links in place")
