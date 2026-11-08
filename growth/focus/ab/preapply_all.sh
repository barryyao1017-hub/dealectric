#!/bin/bash
# Pre-apply check (tools/preapply.py) for every coded product whose link doesn't apply its code yet (Barry 11-08).
# Soundcore is skipped: its headless storefront has no cart permalink. One test click per product, 45 s apart.
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  out=$(python3.12 tools/preapply.py "$s" 2>&1 | tail -6)
  v=$(echo "$out" | grep -o 'set "cart_variant": [0-9]*' | grep -o '[0-9]*$')
  if [ -n "$v" ]; then echo "PASS $s $v"; else echo "FAIL $s :: $(echo "$out" | tr '\n' ' ' | cut -c1-220)"; fi
  sleep ${GAP:-45}
done
echo "PREAPPLY DONE"
