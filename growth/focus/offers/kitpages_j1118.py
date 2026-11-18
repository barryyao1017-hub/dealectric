#!/usr/bin/env python3.12
"""Kit comparison pages by size and budget, second set (2026-11-18, Barry: "situation pages are not worth building
more of. The kit-by-size and kit-by-budget pages are what shoppers reach"). Same driver and rules as kitpages.py
(DLC-293 step 3); this file only points it at this set's questions and harvest run. Folders are j1118-<variant>; the
variants are the ones the k1117 run and its kits2 candidates do not cover.

    python3.12 growth/focus/offers/kitpages_j1118.py harvest|research|links|apply|status|kits [folder...]
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "growth/focus/offers"))
import kitpages as K  # noqa: E402

K.RUN = "kits-1118j"
K.HARVEST_RUN = "2026-11-18-jkits-harvest"
K.QUESTIONS = ROOT / "growth/focus/ab-harvest-new-2026-11-18-jkits.json"
K.register()

if __name__ == "__main__":
    sys.exit(K.main())
