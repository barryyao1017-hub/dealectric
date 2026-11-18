#!/usr/bin/env python3.12
"""Resolve a conflict where both sides appended records to the same list (src/gaps.py): keep both, ours first.
git ends each side's hunk before the lines the two last records share (published / checked / updated / all_links),
so a plain union leaves our last record without its closing lines. Here the shared tail that follows the conflict
(up to the first line ending in "},") is copied after our side when our side's last line doesn't close a record.

    python3.12 growth/combo/merge_appended.py <file with conflict markers>     (rewrites it in place; exit 1 if none)
"""
import sys
from pathlib import Path
p = Path(sys.argv[1])
L = p.read_text().split("\n")
out, i, n = [], 0, 0
while i < len(L):
    if L[i].startswith("<<<<<<< "):
        j = next(k for k in range(i, len(L)) if L[k].startswith("======="))
        e = next(k for k in range(j, len(L)) if L[k].startswith(">>>>>>> "))
        ours, theirs = L[i + 1:j], L[j + 1:e]
        out += ours
        last = next((x for x in reversed(ours) if x.strip()), "")
        if not last.rstrip().endswith("},"):
            t = next(k for k in range(e + 1, len(L)) if L[k].rstrip().endswith("},"))
            out += L[e + 1:t + 1] + [""]
        out += theirs
        i, n = e + 1, n + 1
    else:
        out.append(L[i]); i += 1
p.write_text("\n".join(out))
print(f"{n} conflicts resolved in {p}")
sys.exit(0 if n else 1)
