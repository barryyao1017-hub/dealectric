"""Write "cart_variant" on every product that passed tools/preapply.py ('PASS <slug> <variant>' lines in the logs given),
found by parsing src/products.py; inserted right after the record's "slug" value."""
import ast, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
passes = {}
for f in sys.argv[1:]:
    if ":" in f and not f.endswith(".log"):
        s, v = f.split(":"); passes[s] = int(v); continue
    for l in Path(f).read_text().splitlines():
        if l.startswith("PASS "):
            _, s, v = l.split()[:3]; passes[s] = int(v)
pp = ROOT / "src/products.py"
src = pp.read_text()
edits = []
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Dict):
        keys = [k.value if isinstance(k, ast.Constant) else None for k in node.keys]
        if "slug" in keys and "brand" in keys:
            slug = node.values[keys.index("slug")].value
            if slug in passes and "cart_variant" not in keys:
                v = node.values[keys.index("slug")]
                edits.append((v.end_lineno, v.end_col_offset, f', "cart_variant": {passes[slug]}'))
lines = src.splitlines(keepends=True)
for ln, col, text in sorted(edits, reverse=True):
    lines[ln - 1] = lines[ln - 1][:col] + text + lines[ln - 1][col:]
pp.write_text("".join(lines))
print(len(edits), "products set;", len(passes), "passes given")
