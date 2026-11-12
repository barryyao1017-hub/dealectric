#!/usr/bin/env python3
"""One process at a time may change src/ and rebuild docs/ in a working tree (DLC-267, 2026-11-11).

Why: several Claude sessions and the page tools share one checkout. On 2026-11-11 a session's build ran while
tools/gappage.py had a draft inserted mid-gate; its `git add docs` committed and pushed pages whose source records were
not committed, and the live site linked to pages that did not exist for three minutes.

How: an flock on <git dir>/dealectric-build.lock (one per working tree, released by the kernel when the holder exits,
so a crash never leaves it stuck).
  - src/build.py takes it for the length of a build.
  - gappage.py, abpage.py, kitpage.py and codesweep.py hold it from their first edit of src/ to their commit or undo.
  - tools/githooks/pre-commit refuses a commit that stages src/, docs/ or worker/src/ while another process holds it.
A process started by the holder inherits DEALECTRIC_REPOLOCK and passes straight through, so a tool can run build.py
and git commit while it holds the lock.

    python3.12 tools/repolock.py status                 # who holds it, if anyone
    python3.12 tools/repolock.py check [--wait 90]      # exit 1 while another process holds it (the commit hook)
    python3.12 tools/repolock.py run <name> -- <cmd>    # hold it while <cmd> runs: a hand edit -> build -> commit

    import repolock
    with repolock.hold("gappage"): ...
    @repolock.locked("abpage")
"""
from __future__ import annotations

import contextlib
import fcntl
import functools
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = "DEALECTRIC_REPOLOCK"
WAIT = 1800.0          # a page gate (images, build, page check) takes a few minutes; a batch holds it per page

_fh = None             # this process's open, locked file
_depth = 0             # nested hold() calls in this process


class Busy(RuntimeError):
    """The lock stayed with another process for the whole wait."""


def path() -> Path:
    r = subprocess.run(["git", "rev-parse", "--absolute-git-dir"], cwd=ROOT, capture_output=True, text=True)
    d = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else ROOT
    return d / "dealectric-build.lock"


def _try(fh) -> bool:
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError:
        return False


def _info() -> dict:
    try:
        return json.loads(path().read_text() or "{}")
    except (OSError, ValueError):
        return {}


def describe(info: dict | None = None) -> str:
    i = info if info is not None else _info()
    return f"{i.get('tool', 'another process')} (pid {i.get('pid', '?')}, since {i.get('since', '?')})"


def holder() -> dict | None:
    """Who holds the lock, when it is neither this process nor one that started this process; else None."""
    if _fh is not None:
        return None
    with open(path(), "a+") as fh:
        if _try(fh):
            fcntl.flock(fh, fcntl.LOCK_UN)
            return None
    if os.environ.get(ENV):          # locked, and we were started by a holder: it is ours to use
        return None
    return _info() or {"tool": "another process"}


def acquire(tool: str, wait: float = WAIT) -> None:
    """Take the lock, waiting up to `wait` seconds. Nested calls and children of the holder pass straight through."""
    global _fh, _depth
    if _fh is not None:
        _depth += 1
        return
    fh = open(path(), "a+")
    t0, told = time.time(), False
    while not _try(fh):
        if os.environ.get(ENV):      # the process that started us holds it
            fh.close()
            return
        if time.time() - t0 >= wait:
            fh.close()
            raise Busy(f"repo lock still held by {describe()} after {int(wait)} s")
        if not told:
            print(f"repolock: {tool} is waiting for {describe()}", file=sys.stderr, flush=True)
            told = True
        time.sleep(2)
    fh.seek(0)
    fh.truncate()
    fh.write(json.dumps({"pid": os.getpid(), "tool": tool, "since": time.strftime("%Y-%m-%d %H:%M:%S")}))
    fh.flush()
    _fh, _depth = fh, 1
    os.environ[ENV] = f"{os.getpid()}:{tool}"


def release() -> None:
    global _fh, _depth
    if _fh is None:
        return
    _depth -= 1
    if _depth > 0:
        return
    try:
        _fh.seek(0)
        _fh.truncate()
        _fh.flush()
        fcntl.flock(_fh, fcntl.LOCK_UN)
    finally:
        _fh.close()
        _fh = None
        if os.environ.get(ENV, "").startswith(f"{os.getpid()}:"):
            del os.environ[ENV]


@contextlib.contextmanager
def hold(tool: str, wait: float = WAIT):
    acquire(tool, wait)
    try:
        yield
    finally:
        release()


def locked(tool: str, wait: float = WAIT):
    def deco(fn):
        @functools.wraps(fn)
        def inner(*a, **k):
            with hold(tool, wait):
                return fn(*a, **k)
        return inner
    return deco


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else "status"
    if cmd == "status":
        h = holder()
        print(f"held by {describe(h)}" if h else "free")
        return 0
    if cmd == "check":
        wait = float(argv[argv.index("--wait") + 1]) if "--wait" in argv else 0.0
        t0 = time.time()
        while True:
            h = holder()
            if not h:
                return 0
            if time.time() - t0 >= wait:
                print(f"repolock: {describe(h)} is changing src/ and docs/ in this checkout.", file=sys.stderr)
                return 1
            time.sleep(2)
    if cmd == "run" and "--" in argv:
        name, rest = (argv[1] if argv[1] != "--" else "manual"), argv[argv.index("--") + 1:]
        try:
            with hold(name):
                return subprocess.run(rest, cwd=os.getcwd()).returncode
        except Busy as e:
            print(e, file=sys.stderr)
            return 75
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
