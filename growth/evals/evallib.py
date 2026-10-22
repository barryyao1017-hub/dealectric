"""Shared helpers for the assistant-citation eval (growth/evals).

Nothing here is served on dealectric.com. Run under python3.12.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

import yaml

EVALS_DIR = Path(__file__).resolve().parent
REPO = EVALS_DIR.parent.parent
RUNS_DIR = EVALS_DIR / "runs"
OFFERS_PATH = REPO / "docs" / "offers.json"
LINKS_PATH = REPO / "src" / "links.json"
PRODUCTS_PY = REPO / "src" / "products.py"
QUESTIONS_PATH = EVALS_DIR / "questions.yaml"
PROBES_DIR = REPO / "growth" / "probes"

SITE_HOSTS = {"dealectric.com", "www.dealectric.com"}
NETWORK_HOSTS = {"awin1.com", "www.awin1.com", "tkqlhce.com", "www.tkqlhce.com", "anrdoezrs.net", "jdoqocy.com", "dpbolvw.net", "kqzyfj.com"}

# openai/anthropic/gemini/xai go through the vendors' APIs (keys in env). claude-code is Claude as an agent through
# the Claude Code CLI (`claude -p`, WebSearch + WebFetch), billed to the claude.ai subscription login; it stands in
# for the Anthropic API route while the keys are missing (added 2026-10-19, see README "Subscription route").
# chatgpt (and later claude-ai, gemini-app, grok-app) are the consumer apps driven through the agent's Chrome by ui.py;
# since 2026-10-20 they are the loop's primary reading (Barry: shoppers use the apps, not the APIs).
ASSISTANTS = ("chatgpt", "claude-code", "openai", "anthropic", "gemini", "xai")
# Which assistant's user agent a run file's fetches appear under in D1 (Claude Code's WebFetch is Claude-User;
# the ChatGPT app fetches as ChatGPT-User).
UA_ALIAS = {"claude-code": "anthropic", "chatgpt": "openai"}

LEVEL_LABELS = {
    0: "L0 none",
    1: "L1 brand/product recommended",
    2: "L2 dealectric.com cited",
    3: "L3 product page linked",
    4: "L4 /go/ link",
}
# Tiers whose answers count toward the tracked-link rate: the prompt names dealectric.com (B, D, E) or gives the page
# URL (C). Phase 2 (2026-10-21) added D (discount-named) and E (discount-only); tier A stays unprompted discovery.
LINK_TIERS = ("B", "C", "D", "E")
CODE_TIERS = ("D", "E")   # the tiers whose question is the discount code; the code-and-link rate is reported on them (and on B for contrast)
COUPONS_PATH = REPO / "src" / "coupons.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ---------------------------------------------------------------- questions

def load_questions(path: Path = QUESTIONS_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        q = yaml.safe_load(f)
    offers = load_offers()
    ids = set(offers)
    for item in q["questions"]:
        bad = [s for s in item.get("expected", []) if s not in ids]
        if bad or item.get("primary") not in ids:
            raise SystemExit(f"{item['id']}: unknown slug(s) {bad or item.get('primary')} (not in offers.json)")
    return q


def iter_cells(q: dict, tiers=("A", "B", "C"), question_ids=None, controls=True, controls_all_tiers=False):
    """Yield (question_record, tier, prompt) for every prompt the run should ask. With controls_all_tiers the
    controls run on their own tiers whatever `tiers` says (the loop asks only B and C but wants every control)."""
    tmpl = {k: v["template"] for k, v in q["tiers"].items()}
    for t in tiers:
        if t not in tmpl:
            raise SystemExit(f"unknown tier {t}; questions.yaml defines {', '.join(tmpl)}")
    for item in q["questions"]:
        if question_ids and item["id"] not in question_ids:
            continue
        for t in tiers:
            rec = dict(item, kind="question")
            yield rec, t, tmpl[t].format(**item)
    if not controls:
        return
    for kind in ("positive", "negative"):
        for item in q.get("controls", {}).get(kind, []):
            if question_ids and item["id"] not in question_ids:
                continue
            for t in item.get("tiers", ["A"]):
                if (t not in tiers and not controls_all_tiers) or (t == "C" and "primary" not in item):
                    continue
                rec = dict(item, kind=kind, expected=item.get("expected", []))
                yield rec, t, tmpl[t].format(**item)


def parse_n_by_tier(spec: str | None) -> dict[str, int]:
    """'B=1,D=2' -> {'B': 1, 'D': 2}."""
    out = {}
    for part in (spec or "").split(","):
        if "=" in part:
            t, n = part.split("=", 1)
            out[t.strip()] = int(n)
    return out


def plan_jobs(cells, n: int, n_by_tier: dict[str, int] | None = None, controls: str = "full") -> list[tuple]:
    """(rec, tier, prompt, n_index) for every chat a run makes. Phase 2 (2026-10-22, Barry: a run must fit under
    ChatGPT Free's throttle, about 60 chats): `n_by_tier` lowers n on a comparison tier (B=1), and controls 'lite'
    keeps one positive control on tier A and the negative controls on the highest link tier present, once each."""
    n_by_tier = n_by_tier or {}
    neg_tiers = [t for rec, t, _ in cells if rec["kind"] == "negative" and t in LINK_TIERS]
    top = max(neg_tiers, key=lambda t: LINK_TIERS.index(t)) if neg_tiers else "B"
    jobs = []
    pos_done = False
    for rec, tier, prompt in cells:
        if rec["kind"] == "question":
            for i in range(1, n_by_tier.get(tier, n) + 1):
                jobs.append((rec, tier, prompt, i))
            continue
        if controls == "none":
            continue
        if controls == "lite":
            if rec["kind"] == "positive":
                if pos_done:
                    continue
                pos_done = True
            elif tier != top:
                continue
            jobs.append((rec, tier, prompt, 1))
        else:
            for i in range(1, n + 1):
                jobs.append((rec, tier, prompt, i))
    return jobs


def coded_question_ids(q: dict, offers: dict) -> list[str]:
    """The questions whose expected list holds at least one product with a cart-tested code (offers.json
    offer.coupons non-empty): `coded_questions` from questions.yaml when present, else derived from offers.json."""
    listed = q.get("coded_questions")
    if listed:
        return list(listed)
    return [x["id"] for x in q["questions"] if any(offers.get(s, {}).get("offer", {}).get("coupons") for s in x.get("expected") or [x["primary"]])]


def coded_slugs(offers: dict) -> set[str]:
    return {s for s, p in offers.items() if p["offer"].get("coupons")}


# ---------------------------------------------------------------- catalog

def load_offers(path: Path = OFFERS_PATH) -> dict:
    """Return {slug: product record} from docs/offers.json."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {p["id"]: p for p in data["products"]}


def host_of(url: str) -> str:
    try:
        h = (urlparse(url).hostname or "").lower()
    except ValueError:
        return ""
    return h[4:] if h.startswith("www.") else h


def merchant_hosts(offers: dict, slugs=None) -> set[str]:
    hosts = set()
    for slug, p in offers.items():
        if slugs is not None and slug not in slugs:
            continue
        h = host_of(p["offer"].get("merchant_url") or "")
        if h:
            hosts.add(h)
    return hosts


def all_merchant_hosts(offers: dict) -> set[str]:
    hosts = merchant_hosts(offers)
    try:
        with open(LINKS_PATH, encoding="utf-8") as f:
            links = json.load(f)
        for net in ("cj", "awin"):
            for prog in links.get(net, {}).values():
                h = host_of(prog.get("home") or "")
                if h:
                    hosts.add(h)
    except FileNotFoundError:
        pass
    return hosts


def coupon_codes(offers: dict) -> dict[str, set[str]]:
    """{CODE: {slugs it applies to}} from offers.json coupon / coupons fields plus any codes still named in src/products.py caveats."""
    codes: dict[str, set[str]] = {}
    for slug, p in offers.items():
        c = p["offer"].get("coupon")
        if c:
            codes.setdefault(c.upper(), set()).add(slug)
        for cc in p["offer"].get("coupons") or []:  # every cart-tested code for the product (since 2026-10-21)
            codes.setdefault(cc["code"].upper(), set()).add(slug)
    try:
        sys.path.insert(0, str(PRODUCTS_PY.parent))
        import products  # noqa: WPS433  (src/products.py)
        for rec in products.PRODUCTS:
            for cav in rec.get("caveats", []):
                for m in re.finditer(r"\bcode\s+([A-Z][A-Z0-9]{3,})\b", cav):
                    codes.setdefault(m.group(1).upper(), set()).add(rec["slug"])
    except Exception:  # products.py is optional for grading
        pass
    return codes


def brand_names(offers: dict) -> set[str]:
    return {p["brand"] for p in offers.values()}


def all_codes(path: Path = COUPONS_PATH) -> dict[str, dict]:
    """Every code we have ever cart-tested (src/coupons.json), published or not, working or rejected:
    {CODE_UPPER: {brand, result, publish, terms, categories, slugs, min_qty, min_order}}. The grader uses it to
    tell a code we publish for the product (right) from one we know but do not publish for it (wrong: rejected,
    another brand, out of scope, or held back) and from a token the assistant made up (unknown)."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    out: dict[str, dict] = {}
    for c in data.get("codes", []):
        out[c["code"].upper()] = {"brand": c["brand"], "result": c.get("result"), "publish": bool(c.get("publish")), "terms": c.get("terms"),
                                  "categories": c.get("categories"), "slugs": c.get("slugs"), "min_qty": c.get("min_qty"), "min_order": c.get("min_order")}
    return out


# ---------------------------------------------------------------- URLs

_URL_RE = re.compile(r"https?://[^\s<>\"'\)\]\}]+", re.I)
_MD_LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)\)")


def clean_url(u: str) -> str:
    u = u.strip().rstrip(".,;:!?'\"")
    # markdown/html leftovers
    while u.endswith(")") and u.count("(") < u.count(")"):
        u = u[:-1]
    return u


def urls_in_text(text: str) -> list[dict]:
    """Every URL that appears in answer text: markdown links first, then bare URLs."""
    out, seen = [], set()
    for m in _MD_LINK_RE.finditer(text or ""):
        u = clean_url(m.group(2))
        if u not in seen:
            seen.add(u)
            out.append({"url": u, "title": m.group(1), "source": "text_link"})
    for m in _URL_RE.finditer(text or ""):
        u = clean_url(m.group(0))
        if u not in seen:
            seen.add(u)
            out.append({"url": u, "title": "", "source": "text_bare"})
    return out


def strip_tracking(url: str) -> str:
    """Drop utm_* parameters (ChatGPT appends utm_source=chatgpt.com) so slugs compare cleanly."""
    try:
        p = urlparse(url)
    except ValueError:
        return url
    qs = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if not k.lower().startswith("utm_")]
    return urlunparse(p._replace(query=urlencode(qs), fragment=""))


def classify_url(url: str, offers: dict) -> dict:
    """What a URL is to us: our site? which slug? a /go/ link? a merchant or network link?"""
    u = strip_tracking(url)
    host = host_of(u)
    path = urlparse(u).path.rstrip("/")
    info = {"url": url, "host": host, "ours": host == "dealectric.com", "slug": None, "go": False,
            "network": host in {h[4:] if h.startswith("www.") else h for h in NETWORK_HOSTS},
            "merchant": None}
    if info["ours"]:
        m = re.match(r"^/go/([a-z0-9-]+)$", path)
        if m:
            info["go"] = True
            info["slug"] = m.group(1) if m.group(1) in offers else None
            info["unknown_slug"] = m.group(1) not in offers
        else:
            s = path.lstrip("/")
            if s in offers:
                info["slug"] = s
    else:
        for slug, p in offers.items():
            if host and host == host_of(p["offer"].get("merchant_url") or ""):
                info["merchant"] = slug if strip_tracking(p["offer"]["merchant_url"]).rstrip("/") == u.rstrip("/") else info["merchant"] or "site"
    return info


# ---------------------------------------------------------------- run files

def run_dir(run_id: str) -> Path:
    return RUNS_DIR / run_id


def run_file(run_id: str, assistant: str, qid: str, tier: str, n: int) -> Path:
    return run_dir(run_id) / assistant / f"{qid}-{tier}-{n}.json"


def iter_run_files(run_id: str):
    for a in ASSISTANTS:
        d = run_dir(run_id) / a
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.json")):
            yield a, f


def read_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False, default=str)
    os.replace(tmp, path)


def env_key(*names: str) -> str | None:
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return None


# ---------------------------------------------------------------- Claude Code CLI (subscription route)

import shutil as _shutil
import subprocess as _subprocess
import tempfile as _tempfile

CLI_ISOLATION = ["--no-session-persistence", "--setting-sources", "", "--strict-mcp-config"]


def cli_cwd() -> Path:
    """An empty directory outside the repo, so `claude -p` finds no CLAUDE.md, settings or memory up the tree."""
    d = Path(_tempfile.gettempdir()) / "dealectric-eval-cli"
    d.mkdir(parents=True, exist_ok=True)
    return d


def claude_cli() -> str | None:
    return _shutil.which("claude")


def claude_cli_login() -> str | None:
    """'<claude.ai login>' when the CLI is installed and logged in, else None."""
    exe = claude_cli()
    if not exe:
        return None
    try:
        p = _subprocess.run([exe, "auth", "status"], capture_output=True, text=True, timeout=30, cwd=cli_cwd())
        st = json.loads(p.stdout or "{}")
        return "<claude.ai login>" if st.get("loggedIn") else None
    except Exception:
        return None


def claude_cli_json(system: str, user: str, model: str, schema: dict, timeout: int = 180, usage: dict | None = None) -> dict | None:
    """One no-tools `claude -p` call that must answer with JSON matching `schema`; the LLM judge uses it when there
    is no Anthropic API key. Returns the parsed object or None."""
    exe = claude_cli()
    if not exe:
        raise RuntimeError("claude CLI not found")
    cmd = [exe, "-p", user, "--system-prompt", system, "--output-format", "json", "--tools", "",
           "--model", model, "--json-schema", json.dumps(schema), *CLI_ISOLATION]
    p = _subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cli_cwd())
    try:
        d = json.loads(p.stdout)
    except ValueError:
        raise RuntimeError(f"claude CLI returned no JSON (exit {p.returncode}): {(p.stderr or p.stdout)[-300]}")
    if d.get("is_error"):
        raise RuntimeError(f"claude CLI error: {str(d.get('result'))[:300]}")
    if usage is not None:
        add_usage(usage, d.get("usage") or {}, d.get("total_cost_usd"))
    out = d.get("structured_output")
    if out is None:
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", str(d.get("result") or "").strip())
        try:
            out = json.loads(raw)
        except ValueError:
            return None
    return out if isinstance(out, dict) else None


USAGE_KEYS = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")


def add_usage(acc: dict, usage: dict, cost_usd: float | None = None) -> dict:
    """Accumulate one call's token counts (Anthropic-shaped usage dict) and list-price cost into `acc`."""
    acc["calls"] = acc.get("calls", 0) + 1
    for k in USAGE_KEYS:
        acc[k] = acc.get(k, 0) + int(usage.get(k) or 0)
    cost = cost_usd if cost_usd is not None else usage.get("total_cost_usd_list")
    if cost:
        acc["total_cost_usd_list"] = round(acc.get("total_cost_usd_list", 0.0) + float(cost), 6)
    return acc


# ---------------------------------------------------------------- loop support (added 2026-10-19, growth/improvement-loop.md)

import csv as _csv
import math as _math
import subprocess as _sp
from datetime import timedelta as _td

WORKER_DIR = REPO / "worker"
LOOP_DIR = EVALS_DIR / "loop"
UI_CSV_COLUMNS = ["iteration", "assistant", "qid", "tier", "href_found", "link_text", "href", "notes"]
# CODE_ONLY (phase 2): the right code shown, no /go/ link. WRONG_CODE is the code dimension (see grade.py code_class)
# and is counted in the failure table for tiers D/E whatever the link level.
FAILURE_CLASSES = ["NOT_FOUND", "CODE_ONLY", "PAGE_ONLY", "MERCHANT_SWAP", "NETWORK_HOP", "PLAIN_TEXT", "REFUSED", "STALE_CACHE", "OTHER"]
CODE_CLASSES = ["RIGHT_CODE", "WRONG_CODE", "NO_CODE"]


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """(rate, low, high) as fractions; Wilson score interval. n == 0 -> (nan, nan, nan)."""
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * _math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return p, max(0.0, centre - half), min(1.0, centre + half)


def cloudflare_token() -> str | None:
    tok = os.environ.get("CLOUDFLARE_API_TOKEN")
    if tok:
        return tok
    try:
        return _sp.run(["security", "find-generic-password", "-a", "dealectric", "-s", "cloudflare-workers-token", "-w"],
                       capture_output=True, text=True, check=True).stdout.strip() or None
    except (_sp.CalledProcessError, FileNotFoundError):
        return None


def _wrangler(args: list[str], timeout: int = 180) -> tuple[str, str | None]:
    tok = cloudflare_token()
    if not tok:
        return "", "no Cloudflare token (env CLOUDFLARE_API_TOKEN or keychain item cloudflare-workers-token)"
    try:
        p = _sp.run(["npx", "--yes", "wrangler", *args], cwd=WORKER_DIR, capture_output=True, text=True, timeout=timeout,
                    env={**os.environ, "CLOUDFLARE_API_TOKEN": tok})
    except (_sp.TimeoutExpired, FileNotFoundError) as e:
        return "", f"wrangler failed: {e}"
    if p.returncode != 0:
        return "", f"wrangler exit {p.returncode}: {(p.stderr or p.stdout)[-500:]}"
    return p.stdout, None


def d1_query(sql: str) -> tuple[list[dict], str | None]:
    """Read-only query against the Worker's D1 database through wrangler. Returns (rows, error)."""
    out, err = _wrangler(["d1", "execute", "dealectric", "--remote", "--json", "--command", sql])
    if err:
        return [], err
    lines = out.splitlines()
    i = next((n for n, l in enumerate(lines) if l.strip().startswith(("[", "{"))), None)
    if i is None:
        return [], f"no JSON in wrangler output: {out[:300]}"
    try:
        data = json.loads("\n".join(lines[i:]))
        return (data[0]["results"] if isinstance(data, list) else data["results"]), None
    except (ValueError, KeyError, IndexError, TypeError) as e:
        return [], f"could not parse wrangler output: {e}: {out[:300]}"


def d1_recent_ai_fetch_slugs(days: int = 7) -> tuple[dict[str, str], str | None]:
    """{slug: latest ts} for /go/ fetches by AI assistants in the last `days` days."""
    since = (datetime.now(timezone.utc) - _td(days=days)).strftime("%Y-%m-%dT%H:%M:%S")
    rows, err = d1_query(f"SELECT slug, max(ts) ts FROM clicks WHERE kind='ai_fetch' AND ts >= '{since}' GROUP BY slug")
    return {r["slug"]: r["ts"] for r in rows}, err


def site_commit() -> str | None:
    try:
        return _sp.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()
    except (_sp.CalledProcessError, FileNotFoundError):
        return None


def worker_version() -> dict:
    """Latest Worker deployment: {'version': id, 'deployed_at': iso} from `wrangler deployments list`, or the
    WORKER_VERSION env var (deployed_at then unknown)."""
    env = os.environ.get("WORKER_VERSION")
    if env:
        return {"version": env, "deployed_at": os.environ.get("WORKER_DEPLOYED_AT"), "source": "env"}
    out, err = _wrangler(["deployments", "list"], timeout=120)
    if err:
        return {"version": None, "deployed_at": None, "source": f"unavailable: {err}"}
    deployments = []
    created = None
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("Created:") and created is None:
            created = s.split(":", 1)[1].strip()
        elif s.startswith("Version(s):"):
            m = re.search(r"([0-9a-f]{8}-[0-9a-f-]{27})", s)
            deployments.append({"version": m.group(1) if m else s, "deployed_at": created})
            created = None
    if not deployments:
        return {"version": None, "deployed_at": None, "source": "unparsed wrangler output"}
    latest = max(deployments, key=lambda d: d["deployed_at"] or "")
    return {**latest, "source": "wrangler deployments list"}


def stamp(iteration: int | None, gsc: int | None, bing: int | None, offline: bool = False, phase: int = 1) -> dict:
    wv = {"version": os.environ.get("WORKER_VERSION"), "deployed_at": None, "source": "offline"} if offline else worker_version()
    return {"iteration": iteration, "phase": phase, "site_commit": site_commit(), "worker_version": wv["version"],
            "worker_deployed_at": wv["deployed_at"], "worker_version_source": wv["source"],
            "gsc_indexed": gsc, "bing_indexed": bing, "stamped_at": now_iso()}


def stamp_phase(manifest: dict) -> int:
    """The loop phase a run belongs to; runs stamped before phase 2 existed carry no `phase` and are phase 1."""
    return int(((manifest or {}).get("stamp") or {}).get("phase") or 1)


def read_ui_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(_csv.DictReader(f))
    for r in rows:
        r["href_found"] = str(r.get("href_found", "")).strip().lower() in ("1", "true", "yes", "y")
    return rows


def run_ids_for_iteration(it: str, phase: int | None = None) -> list[str]:
    """Run ids whose manifest carries iteration `it` (newest last), in `phase` when given (phase-2 iterations restart
    at 0; "2:1" also names phase 2 iteration 1). A run id passed directly is returned as is."""
    if (RUNS_DIR / it).is_dir():
        return [it]
    if ":" in str(it):
        ph, it = str(it).split(":", 1)
        phase = int(ph)
    found = []
    for mp in sorted(RUNS_DIR.glob("*/manifest.json")):
        m = read_json(mp)
        if str((m.get("stamp") or {}).get("iteration")) == str(it) and (phase is None or stamp_phase(m) == phase):
            found.append((m.get("started_at") or "", mp.parent.name))
    return [rid for _, rid in sorted(found)]


def frozen_loop_subset(manifest: dict, q: dict) -> list[dict] | None:
    """The loop subset stored in a run's manifest (first run of the iteration picked it), as question records with
    `primary` and `fresh` restored; None when the manifest has none. Keeps the subset stable across the assistants
    and re-runs of one iteration even though the loop's own fetches change the D1 rotation input."""
    loop = (manifest or {}).get("loop") or {}
    picked = loop.get("questions")
    if not picked:
        return None
    by_id = {x["id"]: x for x in q["questions"]}
    out = []
    for x in picked:
        if x["id"] in by_id:
            out.append({**by_id[x["id"]], "primary": x["primary"], "fresh": x.get("fresh", True)})
    return out or None
