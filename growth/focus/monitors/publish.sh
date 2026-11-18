#!/bin/bash
# Screen extender run (DLC-290): publish what this worktree has committed. Merge origin/main (other sessions push there
# all day), rebuild docs/ from the merged src/, push to main; retried when main moves during the build.
# Usage: bash growth/focus/monitors/publish.sh     (then: bash worker/deploy.sh when worker/src/links-map.json changed)
set -u
cd "$(dirname "$0")/../../.."
log(){ echo "[publish $(date +%H:%M:%S)] $*"; }
if [ -n "$(git status --porcelain src docs worker/src)" ]; then log "src/ or docs/ dirty: commit or finish the apply first"; exit 2; fi
for try in 1 2 3 4; do
  git fetch -q origin || { log "fetch failed"; exit 3; }
  if ! git merge-base --is-ancestor origin/main HEAD; then
    python3.12 tools/repolock.py run monitors-publish -- bash -c '
      set -u
      git merge -q --no-commit origin/main >/dev/null 2>&1
      for f in $(git diff --name-only --diff-filter=U); do
        case "$f" in
          docs/*|worker/src/links-map.json|worker/src/dash-meta.json) git checkout --theirs -- "$f" 2>/dev/null || git rm -q --cached "$f"; git add -A -- "$f" ;;   # rebuilt below
          growth/focus/ab/LIBRARY.md|growth/focus/ab/library.json) git checkout --theirs -- "$f"; git add -- "$f"; REINDEX=1 ;;   # generated index: rebuilt below
          *) echo "UNRESOLVED $f"; git merge --abort; exit 4 ;;
        esac
      done
      python3.12 -c "import ast; [ast.parse(open(f).read()) for f in (\"src/gaps.py\",\"src/products.py\")]" || { echo "merged src does not parse"; git merge --abort; exit 5; }
      REPOLOCK_HELD=1 python3.12 src/build.py > /tmp/claude-502/monitors-publish-build.log 2>&1 || { echo "build failed after merge"; tail -5 /tmp/claude-502/monitors-publish-build.log; git merge --abort; exit 6; }
      python3.12 tools/docsguard.py | tail -1
      if [ "${REINDEX:-}" = 1 ]; then python3.12 tools/research_library.py build >/dev/null 2>&1; git add growth/focus/ab/LIBRARY.md growth/focus/ab/library.json; fi
      git add -A src docs worker/src
      git commit -q --no-edit -m "Merge main into the screen extender run (DLC-290); docs rebuilt from the merged src" || true
    ' || { log "merge failed ($?)"; exit 1; }
  fi
  if git push -q origin HEAD:main; then log "pushed $(git rev-parse --short HEAD)"; exit 0; fi
  log "push rejected (main moved), try $try"
done
exit 7
