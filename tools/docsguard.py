"""Refuse to stage/commit docs/ when it looks broken (DLC-149: OneDrive can leave docs/ missing, truncated or
duplicated as "docs 2"; `git add docs` would then delete the live site). Import check() or run as a script."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOLERANCE = 5   # pages a legitimate build may drop in one go


def check(root: str = ROOT) -> None:
    """Exit non-zero with a clear message unless docs/ is present, complete and unduplicated."""
    docs = os.path.join(root, "docs")
    sib = [n for n in os.listdir(root) if n.startswith("docs ") ]
    if sib:
        raise SystemExit(f"REFUSING TO COMMIT: sibling folder(s) {sib} next to docs/ (OneDrive race, DLC-149). Do not commit; see CLAUDE.md.")
    if not os.path.isdir(docs):
        raise SystemExit("REFUSING TO COMMIT: docs/ is missing (OneDrive race, DLC-149). Re-run the build; do not `git add -A`.")
    tracked = subprocess.run(["git", "ls-files", "docs"], cwd=root, capture_output=True, text=True).stdout.split("\n")
    tracked = [t for t in tracked if t]
    have = sum(len(fs) for _, _, fs in os.walk(docs))
    if have < len(tracked) - TOLERANCE:
        raise SystemExit(f"REFUSING TO COMMIT: docs/ holds {have} files but git tracks {len(tracked)} (tolerance {TOLERANCE}); looks truncated (DLC-149).")


if __name__ == "__main__":
    check()
    print("docs/ ok")
