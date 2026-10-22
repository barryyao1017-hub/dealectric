#!/usr/bin/env python3.12
"""Grade the raw run files of one run deterministically, then add the LLM-judged rank, the failure class with the
assistant's own explanation, the D1 fetch join, and the browser spot-check (UI) merge.

    python3.12 growth/evals/grade.py                     # today's run
    python3.12 growth/evals/grade.py --run-id 2026-10-19 --no-d1 --no-judge
    python3.12 growth/evals/grade.py --run-id 2026-10-20 --ui-csv growth/evals/loop/ui/iter-01.csv
    python3.12 growth/evals/grade.py --regrade           # ignore cached grades

Writes growth/evals/runs/<run-id>/grades.jsonl (one row per run file), grades-ui.jsonl (one row per UI CSV line,
when a CSV is found) and d1-ai-fetch.json.

Ladder (on the URLs the shopper sees: inline citations plus links in the answer text):
  L0 none
  L1 one of our brands or an expected product is named
  L2 dealectric.com cited or linked
  L3 the Dealectric product page of an expected slug linked
  L4 https://dealectric.com/go/<expected slug> linked   (= L4-api; L4-ui comes from the UI CSV)
Flags: bypass (merchant-site or awin1/tkqlhce link instead of /go/, tiers B and C), coupon surfaced
(codes from offers.json / src/products.py), our_rank (LLM judge, tiers A and B only, only when a brand or product
is named), consulted_ours (assistant fetched or searched our site but did not show it), d1_fetched_slugs.

Failure classes for every non-L4 answer (growth/improvement-loop.md §3), checked in this order:
  NOT_FOUND      nothing of ours shown, consulted or fetched (tier B; tier C answers that show no sign of reading
                 the page get it too, with the evidence saying so)
  REFUSED        prose declining to give an affiliate / tracked / redirect link
  STALE_CACHE    a linked awin1/tkqlhce URL carries a click id whose D1 row predates the last Worker deploy
  NETWORK_HOP    a raw awin1.com / tkqlhce.com URL linked
  MERCHANT_SWAP  the merchant's site linked instead of /go/
  CODE_ONLY      (phase 2) a code we publish for the product shown, no /go/ link
  PAGE_ONLY      our product page linked, no /go/ anywhere
  OTHER          none of the above (PLAIN_TEXT exists for UI rows only)
Phase 2 code dimension, on every row: code_class RIGHT_CODE (a code we publish for the linked or expected product),
WRONG_CODE (a code we know but do not publish for it, or a token the answer presents as a code that we never had),
NO_CODE; code_and_link = L4 and RIGHT_CODE in the same answer.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

JUDGE_MODEL_DEFAULT = "claude-sonnet-5-5"

# Distinctive names per slug, matched case-insensitively with flexible spacing/hyphens. Regex allowed.
KEYWORDS = {
    "baseus-blade-hd-100w-20000mah": ["Blade HD"],  # retired 2026-10-21; kept so older runs re-grade the same
    "baseus-blade-h1-100w-20000mah": ["Blade H1"],
    "baseus-gan5-pro-65w-2c-u": ["GaN5 Pro", "GaN 5 Pro"],
    "baseus-nomos-5-in-1-140w-qi2": ["Nomos"],
    "baseus-picogo-am52-qi2-2-10000mah-45w": ["PicoGo"],
    "baseus-usb-c-cable-100w": ["Baseus 100W", "Baseus USB-C to USB-C", "CAWJ020001"],
    "esr-cryoboost-3-in-1-qi2-2-25w-stand": ["CryoBoost 3-in-1", "ESR 3-in-1", "ESR 25W 3-in-1"],
    "esr-halolock-magslim-qi2-power-bank-10000mah": ["MagSlim"],
    "esr-100w-6-in-1-magsafe-cryoboost-station": ["ESR 6-in-1", "ESR 100W", "6-in-1 CryoBoost"],
    "esr-halolock-15w-wireless-car-charger-cryoboost": ["HaloLock car", "ESR car charger", "ESR HaloLock CryoBoost car"],
    "esr-qi2-mini-wireless-charger-15w": ["Qi2 Mini", "ESR mini wireless", "ESR Magnetic Charging Pad"],
    "tenergy-tn480u-8-bay-nimh-charger": ["TN480"],
    "tenergy-premium-pro-aa-2800mah-20-pack": ["Premium Pro"],
    "tenergy-tn270-li-ion-18650-charger": ["TN270"],
    "tenergy-t320-300wh-power-station": ["T320"],
    "bluetti-elite-200-v2": ["Elite 200"],
    "bluetti-ac200l": ["AC200L"],
    "bluetti-elite-30-v2": ["Elite 30(?!0)"],
    "bluetti-elite-300": ["Elite 300"],
    "bluetti-ac180": ["AC180"],
    "allpowers-p1800-1024wh": ["P1800"],
    "allpowers-r600-299wh": ["R600"],
    "allpowers-s2000-pro-1451wh": ["S2000"],
    "allpowers-r4000-3456wh": ["R4000"],
    "allpowers-sp037-400w-solar-panel": ["SP037"],
    "soundcore-liberty-4-pro": ["Liberty 4 Pro"],
    "soundcore-space-one-pro": ["Space One Pro"],
    "soundcore-space-one": [r"Space One(?![\s-]?Pro)"],
    "soundcore-aerofit-2": ["AeroFit 2"],
    "soundcore-boom-2-plus": ["Boom 2 Plus"],
    "soundcore-motion-x600": ["X600"],
    "soundcore-boom-3i": ["Boom 3i"],
}


def _kw_re(kw: str) -> re.Pattern:
    pat = re.sub(r"\s+", r"[\\s-]*", kw)
    return re.compile(r"(?<![A-Za-z0-9])" + pat + r"(?![A-Za-z0-9])", re.I)


KW_RES = {slug: [_kw_re(k) for k in kws] for slug, kws in KEYWORDS.items()}
UA_MAP = [
    ("openai", ("chatgpt-user", "oai-searchbot", "gptbot", "openai")),
    ("anthropic", ("claude-user", "claudebot", "anthropic")),
    ("gemini", ("google", "gemini")),
    ("xai", ("grok", "xai", "x.ai")),
]
REFUSAL_RE = re.compile(
    r"(?:can(?:no|')t|cannot|won'?t|will not|unable to|not able to|don'?t|do not|shouldn'?t|not going to|refus\w*|declin\w*)"
    r"[^.\n]{0,80}?(?:affiliate|tracked|tracking|redirect|referral)[^.\n]{0,40}?(?:link|url)"
    r"|(?:affiliate|tracked|tracking|redirect|referral) (?:links?|urls?)[^.\n]{0,60}?"
    r"(?:not (?:allowed|permitted|supported|something)|can'?t|cannot|won'?t|against|unable)", re.I)
CLICK_ID_RE = re.compile(r"(?:clickref|sid)=([a-z0-9-]+)\.([0-9a-f]{6,})", re.I)
STALE_COPY_MARKERS = ["specs, price and offer", "October 14, 2026", "2026-10-14", "normalized specs and verified offers",
                      "Structured electronics product data for AI shopping assistants",
                      # the Elite 30 V2's price before the 10/21 price check: only a catalog copy from before 10/21 carries it
                      "$279.99"]
# A negative-control answer that says we do not list the product. Such an answer may still link products we do carry
# as alternatives (iteration 0 did, with /go/ links); that is not an invented listing, so it passes.
NEG_HONEST_RE = re.compile(
    r"dealectric(?:\.com)?[^.\n]{0,60}?(?:doesn'?t|does not|don'?t|do not|didn'?t|did not)[^.\n]{0,20}?(?:sell|carry|list|stock|offer|have|include)"
    r"|(?:not|no)[^.\n]{0,30}?(?:in|on|at) (?:its|their|the|dealectric'?s?) (?:catalog|catalogue|site|listings?|offers)"
    r"|(?:isn'?t|is not|aren'?t|are not)[^.\n]{0,40}?(?:listed|carried|sold|available|stocked)[^.\n]{0,30}?(?:on|at|by) dealectric"
    r"|no (?:dealectric )?(?:listing|product page|buy link)[^.\n]{0,60}?(?:for|of) (?:this|that|the)"
    r"|can'?t (?:give|get|provide|find)[^.\n]{0,40}?dealectric[^.\n]{0,30}?(?:link|code|listing|page)"
    r"|(?:isn'?t|is not|aren'?t|are not|not) (?:one of|among|in) (?:them|its|their|the) ?(?:brands|catalog|listings?)?", re.I)


# Phase 2: a token the answer presents as a code ("code AFSC20", "promo code: `SAVE10`"), to catch codes we never
# published. Uppercase, 4–20 characters, a digit or at least 5 letters; common words after "code" are skipped.
CODE_TOKEN_RE = re.compile(r"(?:\bcode|\bcoupon|\bpromo(?:\s+code)?|\bvoucher)\b\s*(?:is|was|:|：|-|–|—)?\s*[\"'“‘`*_]*([A-Z][A-Z0-9]{3,19})(?![a-z])")
CODE_STOP = {"NONE", "THIS", "THAT", "YOUR", "WITH", "FROM", "ONLY", "ENTER", "APPLY", "CHECKOUT", "DEALECTRIC", "HERE", "BELOW", "ABOVE",
             "WHICH", "THERE", "WHEN", "LISTED", "AVAILABLE", "NEEDED", "REQUIRED", "VALID", "WORKS", "FOUND", "SHOWN", "GIVEN"}


def codes_in_text(text: str, known: dict[str, set[str]], universe: dict[str, dict]) -> dict:
    """Which codes the answer shows: `known` ({CODE: slugs it applies to} from offers.json), `universe` (every code
    in src/coupons.json), plus uppercase tokens the prose presents as a code. Returns the three disjoint lists."""
    found_known = sorted({c for c in known if re.search(r"(?<![A-Z0-9])" + re.escape(c) + r"(?![A-Z0-9])", text, re.I)})
    found_universe = sorted({c for c in universe if c not in known and re.search(r"(?<![A-Z0-9])" + re.escape(c) + r"(?![A-Z0-9])", text, re.I)})
    tokens = set()
    for m in CODE_TOKEN_RE.finditer(text or ""):
        t = m.group(1)
        if t in CODE_STOP or t.upper() in known or t.upper() in universe:
            continue
        if not (re.search(r"\d", t) or len(t) >= 5):
            continue
        tokens.add(t)
    return {"known": found_known, "other_known": found_universe, "unknown": sorted(tokens)}


def ua_assistant(ua: str) -> str:
    u = (ua or "").lower()
    for name, needles in UA_MAP:
        if any(n in u for n in needles):
            return name
    return "other"


def parse_ts(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


# ---------------------------------------------------------------- deterministic part

def grade_record(rec: dict, offers: dict, coupons: dict, brands: set[str], universe: dict | None = None) -> dict:
    # Curly apostrophes (ChatGPT and Claude both write "doesn’t") would slip past the ASCII-quoted regexes.
    text = (rec.get("text") or "").replace("\u2019", "'").replace("\u2018", "'")
    universe = universe if universe is not None else E.all_codes()
    expected = set(rec.get("expected") or [])
    shown_src = [(u, E.classify_url(u["url"], offers)) for u in (rec.get("citations") or []) + (rec.get("text_urls") or []) if u.get("url")]
    shown = [c for _, c in shown_src]
    consulted = [E.classify_url(u["url"], offers) for u in (rec.get("consulted") or []) if u.get("url")]

    go_slugs = sorted({c["slug"] for c in shown if c["go"] and c["slug"]})
    go_unknown = sorted({E.strip_tracking(c["url"]) for c in shown if c["go"] and c.get("unknown_slug")})
    page_slugs = sorted({c["slug"] for c in shown if c["ours"] and not c["go"] and c["slug"]})
    ours_shown = [E.strip_tracking(c["url"]) for c in shown if c["ours"]]
    network_links = sorted({c["url"] for c in shown if c["network"]})
    exp_merchants = E.merchant_hosts(offers, expected) if expected else E.all_merchant_hosts(offers)
    merchant_links = sorted({c["url"] for c in shown if c["host"] in exp_merchants})
    l4_evidence = sorted({u["source"] for u, c in shown_src if c["go"] and c["slug"] in expected})

    brand_hits = sorted({b for b in brands if re.search(r"(?<![A-Za-z])" + re.escape(b) + r"(?![A-Za-z])", text, re.I)})
    product_hits = sorted({s for s, pats in KW_RES.items() if any(p.search(text) for p in pats)})
    expected_hits = sorted(set(product_hits) & expected)

    if expected and set(go_slugs) & expected:
        level = 4
    elif expected and set(page_slugs) & expected:
        level = 3
    elif ours_shown:
        level = 2
    elif expected_hits or brand_hits:
        level = 1
    else:
        level = 0

    cf = codes_in_text(text, coupons, universe)
    codes_found = cf["known"]
    coupon_applicable = sorted({c for c in codes_found if coupons[c] & expected}) if expected else []
    # Phase 2 code dimension. The target is the product the answer linked (go slug in expected) when there is one,
    # else any expected product. Right = a code we publish for the target; wrong = a code we know but do not publish
    # for it (rejected, another brand, out of scope, held back) or a token the answer invented; none = no code shown.
    target = (set(go_slugs) & expected) or expected
    codes_right = sorted({c for c in codes_found if coupons[c] & target}) if target else []
    codes_wrong = sorted(set(codes_found) - set(codes_right)) + cf["other_known"] + cf["unknown"]
    code_class = "RIGHT_CODE" if codes_right else ("WRONG_CODE" if codes_wrong else "NO_CODE")

    tier = rec["tier"]
    bypass = bool(tier in E.LINK_TIERS and (merchant_links or network_links) and level < 4)
    domains_shown = sorted({c["host"] for c in shown if c["host"]})
    expect_domains = rec.get("expect_domains") or []
    control_pass = None
    if rec.get("kind") == "positive":
        control_pass = any(any(h == d or h.endswith("." + d) for h in domains_shown) for d in expect_domains)
    elif rec.get("kind") == "negative":
        # Pass = no invented /go/ slug, and either nothing of ours presented as the product (L<3) or the answer says
        # outright that we do not list it (alternatives from our catalog may then carry product-page or /go/ links).
        # On tier D (phase 2) a code we never had, presented without saying we do not list the product, also fails
        # (an honest answer may still pass on coupon-site codes it found elsewhere, as claude-code did for Anker).
        honest = bool(NEG_HONEST_RE.search(text))
        control_pass = not go_unknown and ((level < 3 and not go_slugs) or honest) and not (tier == "D" and cf["unknown"] and not honest)

    click_ids = sorted({m.group(2) for u in network_links + merchant_links for m in [CLICK_ID_RE.search(u)] if m})
    refusal = REFUSAL_RE.search(text)
    # Phase 2 stale-copy marker (2026-10-22): ChatGPT answers from its search-index copy of a page even after fetching
    # the live one. Pre-rebrand titles ("specs, price and offer", the product page's old <title>) and the pre-10/21
    # verification date in the answer or in the citation titles mean the cell read old copy.
    cite_titles = " ".join(str(c.get("title") or "") for c in (rec.get("citations") or []))
    stale_copy = sorted({m for m in STALE_COPY_MARKERS if m.lower() in (text + " " + cite_titles).lower()})
    # "content": a pre-deploy date or wording in the answer itself; "title": only the old page title, which ChatGPT shows
    # as the citation chip label from its search index even when the fetched content was fresh.
    stale_strength = ("content" if any(m.lower() in text.lower() for m in STALE_COPY_MARKERS if "October 14" in m or "2026-10-14" in m or m == "$279.99")
                      else "title" if stale_copy else None)
    # App records (ui.py) score hyperlinks only; a /go/ URL that is in the visible text but not an <a href> is PLAIN_TEXT.
    go_in_text = sorted(s for s in expected if re.search(r"dealectric\.com/go/" + re.escape(s) + r"(?![a-z0-9-])", text))
    st = rec.get("stamp") or {}
    return {
        "iteration": st.get("iteration"), "stamp_phase": st.get("phase"), "site_commit": st.get("site_commit"), "worker_version": st.get("worker_version"),
        "worker_deployed_at": st.get("worker_deployed_at"), "gsc_indexed": st.get("gsc_indexed"), "bing_indexed": st.get("bing_indexed"),
        "level": level, "level_label": E.LEVEL_LABELS[level], "l4_api": level == 4, "l4_evidence": l4_evidence,
        "brand_hits": brand_hits, "product_hits": product_hits, "expected_hits": expected_hits,
        "dealectric_urls_shown": sorted(set(ours_shown)), "page_slugs": page_slugs, "go_slugs": go_slugs,
        "go_unknown_slugs": go_unknown, "other_our_slugs": sorted((set(page_slugs) | set(go_slugs)) - expected),
        "merchant_links": merchant_links, "network_links": network_links, "bypass": bypass,
        "coupon_codes_found": codes_found, "coupon_surfaced": bool(coupon_applicable), "coupon_applicable": coupon_applicable,
        "codes_right": codes_right, "codes_wrong": codes_wrong, "codes_unknown": cf["unknown"], "code_class": code_class,
        "code_and_link": bool(level == 4 and codes_right),
        "consulted_ours": sorted({E.strip_tracking(c["url"]) for c in consulted if c["ours"]}),
        "domains_shown": domains_shown, "n_shown_urls": len(shown), "n_consulted_urls": len(consulted),
        "n_raw_citations": len(rec.get("raw_citations") or []),
        "control_pass": control_pass, "refusal_match": refusal.group(0) if refusal else None, "click_ids": click_ids,
        "ui": bool(rec.get("ui")), "go_in_text": go_in_text, "stale_copy": stale_copy, "stale_strength": stale_strength,
    }


def classify_failure(row: dict, stale_ids: set[str]) -> tuple[str | None, str]:
    """(class, evidence) for a graded API row; (None, '') when the answer is L4."""
    if row["level"] == 4:
        return None, ""
    if row.get("ui") and row.get("go_in_text"):
        return "PLAIN_TEXT", "/go/ URL in the answer text but not a hyperlink: " + ", ".join(row["go_in_text"])
    reached = row["level"] >= 2 or row["consulted_ours"] or row.get("d1_fetched_slugs")
    if not reached:
        why = "no dealectric.com URL shown or consulted, no ai_fetch row"
        return "NOT_FOUND", why + ("" if row["tier"] == "B" else f" (tier {row['tier']}: page apparently not read)")
    ours = [E.strip_tracking(u).rstrip("/") for u in row["dealectric_urls_shown"]]
    if row["level"] == 2 and ours and all(u in ("https://dealectric.com", "https://www.dealectric.com") for u in ours) \
            and not row["consulted_ours"] and not row.get("d1_fetched_slugs"):
        # Search returned our home page and nothing deeper: the product was not found (the app's tier-B signature).
        return "NOT_FOUND", "only the home page linked (search returned no product page)"
    if row.get("refusal_match"):
        return "REFUSED", f"prose: \"{row['refusal_match'][:120]}\""
    if row["click_ids"] and set(row["click_ids"]) & stale_ids:
        return "STALE_CACHE", f"click id(s) {sorted(set(row['click_ids']) & stale_ids)} predate the last Worker deploy"
    if row.get("stale_copy") and (row.get("stamp_phase") or 0) >= 2 and (row.get("iteration") or 0) >= 1:
        return "STALE_CACHE", "answer built from a pre-rebrand copy of the page: " + ", ".join(row["stale_copy"])
    if row["network_links"]:
        return "NETWORK_HOP", "linked " + "; ".join(row["network_links"][:2])
    if row["merchant_links"]:
        return "MERCHANT_SWAP", "linked " + "; ".join(row["merchant_links"][:2])
    if row.get("codes_right"):
        # Phase 2: the code reached the shopper, the tracked link did not (the page may be linked, named in evidence).
        return "CODE_ONLY", "code " + ", ".join(row["codes_right"]) + " shown, no /go/ link" + \
            (f"; product page linked: {', '.join(row['page_slugs'])}" if row["level"] == 3 else "")
    if row["level"] == 3:
        return "PAGE_ONLY", "product page linked: " + ", ".join(row["page_slugs"])
    detail = []
    if row["level"] == 2:
        detail.append("dealectric.com cited without a product page: " + ", ".join(row["dealectric_urls_shown"][:2]))
    if row["consulted_ours"] and row["level"] < 2:
        detail.append("our site consulted but not shown")
    if row.get("d1_fetched_slugs") and row["level"] < 2:
        detail.append("/go/ fetched (D1) but nothing of ours shown")
    if row.get("error"):
        detail.append(f"API error: {str(row['error'])[:80]}")
    return "OTHER", "; ".join(detail) or "no link evidence matched"


# ---------------------------------------------------------------- LLM passes (Anthropic API)

JUDGE_SYSTEM = (
    "You grade a shopping assistant's answer for a product catalog owner. You get the catalog (id, brand, name) and "
    "the answer. List the products the answer recommends or presents as picks, in the order the answer presents them "
    "(top pick first). For each, give the catalog id it is (the same product; a different model or variant is not a "
    "match) or null. Products the answer only mentions in passing, as a comparison, or as something to avoid are not "
    "picks. Reply with JSON only: {\"picks\": [{\"name\": str, \"slug\": str|null}]}."
)
EXPLAIN_SYSTEM = (
    "You are given a shopping assistant's answer. The assistant was asked for the buy link that dealectric.com gives "
    "(https://dealectric.com/go/...). Quote, verbatim and complete, the sentence or sentences in which the assistant "
    "explains which link it chose to give the shopper and why, or why it could not give one (for example that a link "
    "redirects to the official product page, that it does not give affiliate or tracking links, that it could not find "
    "the page). Copy the text exactly as written; do not paraphrase or fix typos. If no such explanation exists, "
    "return null. Reply with JSON only: {\"quote\": str|null}."
)


JUDGE_SCHEMA = {"type": "object", "properties": {"picks": {"type": "array", "items": {
    "type": "object", "properties": {"name": {"type": "string"}, "slug": {"type": ["string", "null"]}}, "required": ["name", "slug"]}}},
    "required": ["picks"]}
EXPLAIN_SCHEMA = {"type": "object", "properties": {"quote": {"type": ["string", "null"]}}, "required": ["quote"]}


def _json_reply(resp) -> dict | None:
    raw = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


class ApiJudge:
    """The LLM passes over the Anthropic API (ANTHROPIC_API_KEY or an auth token)."""
    name = "anthropic API"

    def __init__(self, model: str):
        import anthropic
        self.client = anthropic.Anthropic(timeout=120, max_retries=3)
        if not (getattr(self.client, "api_key", None) or getattr(self.client, "auth_token", None)):
            raise RuntimeError("no ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN")
        self.model = model
        self.usage: dict = {}

    def ask(self, system: str, user: str, schema: dict, max_tokens: int) -> dict | None:
        resp = self.client.messages.create(model=self.model, max_tokens=max_tokens, system=system,
                                           messages=[{"role": "user", "content": user}],
                                           extra_body={"output_config": {"effort": "low"}})
        u = getattr(resp, "usage", None)
        E.add_usage(self.usage, {k: getattr(u, k, 0) for k in E.USAGE_KEYS} if u else {})
        return _json_reply(resp)


class CliJudge:
    """The same passes through `claude -p` (no tools, JSON schema), billed to the claude.ai subscription login.
    Used when there is no API key; see README "Subscription route"."""
    name = "claude CLI (subscription)"

    def __init__(self, model: str):
        if not E.claude_cli_login():
            raise RuntimeError("claude CLI not installed or not logged in")
        self.model = model
        self.usage: dict = {}

    def ask(self, system: str, user: str, schema: dict, max_tokens: int) -> dict | None:
        return E.claude_cli_json(system, user, self.model, schema, usage=self.usage)


def make_judge(kind: str, model: str):
    """kind: auto (API if a key exists, else CLI), api, cli. Raises when the chosen backend is unavailable."""
    if kind == "api":
        return ApiJudge(model)
    if kind == "cli":
        return CliJudge(model)
    try:
        return ApiJudge(model)
    except Exception as api_err:
        try:
            return CliJudge(model)
        except Exception as cli_err:
            raise RuntimeError(f"{api_err}; {cli_err}")


def judge_rank(judge, model: str, text: str, offers: dict, expected: set[str]) -> dict:
    catalog = "\n".join(f"- {s}: {p['brand']} {p['name']}" for s, p in offers.items())
    data = judge.ask(JUDGE_SYSTEM, f"CATALOG\n{catalog}\n\nANSWER\n{text[:12000]}", JUDGE_SCHEMA, 2048)
    if not isinstance(data, dict):
        return {"picks": [], "our_rank": None, "catalog_rank": None, "judge_error": "unparseable judge reply"}
    picks = data.get("picks") or []
    return {"picks": picks, "judge_error": None, "judge_model": f"{model} via {judge.name}",
            "our_rank": next((i for i, p in enumerate(picks, 1) if p.get("slug") in expected), None),
            "catalog_rank": next((i for i, p in enumerate(picks, 1) if p.get("slug") in offers), None)}


def explain_link(judge, model: str, text: str) -> dict:
    data = judge.ask(EXPLAIN_SYSTEM, f"ANSWER\n{text[:12000]}", EXPLAIN_SCHEMA, 1024)
    quote = data.get("quote") if isinstance(data, dict) else None
    if not quote:
        return {"explanation": None, "explanation_verbatim": None}
    norm = lambda s: re.sub(r"\s+", " ", s).strip().lower()  # noqa: E731
    return {"explanation": quote, "explanation_verbatim": norm(quote) in norm(text)}


# ---------------------------------------------------------------- D1

def d1_ai_fetch_rows(start: datetime, end: datetime) -> tuple[list[dict], str | None]:
    sql = ("SELECT id, ts, slug, click_id, user_agent, utm_source, query, country, verified_bot FROM clicks "
           f"WHERE kind='ai_fetch' AND ts >= '{start.strftime('%Y-%m-%dT%H:%M:%S')}' "
           f"AND ts <= '{end.strftime('%Y-%m-%dT%H:%M:%S')}.999Z' ORDER BY id")
    rows, err = E.d1_query(sql)
    for r in rows:
        r["assistant"] = ua_assistant(r.get("user_agent", ""))
    return rows, err


def d1_click_id_rows(ids: set[str]) -> tuple[list[dict], str | None]:
    if not ids:
        return [], None
    quoted = ",".join("'" + i.replace("'", "") + "'" for i in sorted(ids))
    return E.d1_query(f"SELECT click_id, ts, kind, slug FROM clicks WHERE click_id IN ({quoted})")


# ---------------------------------------------------------------- UI merge

def grade_ui_row(r: dict, offers: dict, expected: set[str], stale_ids: set[str]) -> dict:
    href = (r.get("href") or "").strip()
    link_text, notes = r.get("link_text") or "", r.get("notes") or ""
    out = {"source": "ui", "iteration": r.get("iteration"), "assistant": r.get("assistant"), "qid": r.get("qid"),
           "tier": r.get("tier"), "href_found": r["href_found"], "link_text": link_text, "href": href, "notes": notes,
           "expected": sorted(expected), "level": 0, "l4_ui": False, "failure_class": None, "failure_evidence": ""}
    if not r["href_found"]:
        if "/go/" in link_text or "/go/" in href or "/go/" in notes:
            out.update(level=2, failure_class="PLAIN_TEXT", failure_evidence=f"/go/ shown as text: {link_text or href}")
        else:
            out.update(failure_class="NOT_FOUND", failure_evidence="no hyperlink in the answer")
        return out
    c = E.classify_url(href, offers)
    m = CLICK_ID_RE.search(href)
    if c["go"] and c["slug"] in expected:
        out.update(level=4, l4_ui=True)
    elif c["go"]:
        out.update(level=2, failure_class="OTHER", failure_evidence=f"/go/ link for another or unknown slug: {href}")
    elif c["ours"] and c["slug"] in expected:
        out.update(level=3, failure_class="PAGE_ONLY", failure_evidence=f"product page linked: {href}")
    elif c["ours"]:
        out.update(level=2, failure_class="OTHER", failure_evidence=f"dealectric.com link, not a product page: {href}")
    elif c["network"]:
        stale = bool(m and m.group(2) in stale_ids)
        out.update(level=0, failure_class="STALE_CACHE" if stale else "NETWORK_HOP", failure_evidence=f"linked {href}")
    elif c["host"] in E.merchant_hosts(offers, expected):
        out.update(level=0, failure_class="MERCHANT_SWAP", failure_evidence=f"linked {href}")
    else:
        out.update(level=0, failure_class="OTHER", failure_evidence=f"linked {href}")
    return out


def find_ui_csv(args, rdir: Path, manifest: dict) -> Path | None:
    if args.ui_csv:
        return Path(args.ui_csv)
    cands = [rdir / "ui.csv"]
    it = (manifest.get("stamp") or {}).get("iteration")
    if (isinstance(it, int) or (isinstance(it, str) and it.isdigit())) and E.stamp_phase(manifest) == 1:
        cands.append(E.LOOP_DIR / "ui" / f"iter-{int(it):02d}.csv")   # phase-1 manual spot-checks only
    return next((c for c in cands if c.exists()), None)


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-id", default=E.today())
    ap.add_argument("--no-judge", action="store_true", help="skip the LLM passes (rank, explanation quotes)")
    ap.add_argument("--no-d1", action="store_true", help="skip the D1 clicks join and stale-cache lookup")
    ap.add_argument("--judge-model", default=os.environ.get("JUDGE_MODEL", JUDGE_MODEL_DEFAULT))
    ap.add_argument("--judge", choices=["auto", "api", "cli"], default="auto",
                    help="LLM-pass backend: Anthropic API, or the claude CLI under the subscription login (auto: API if a key exists, else CLI)")
    ap.add_argument("--ui-csv", default=None, help="browser spot-check CSV (default: <run>/ui.csv or loop/ui/iter-NN.csv)")
    ap.add_argument("--regrade", action="store_true", help="recompute rows already in grades.jsonl (LLM passes re-run too)")
    ap.add_argument("--rescore", action="store_true", help="recompute the deterministic fields and failure class of cached rows; keep their LLM-pass fields")
    args = ap.parse_args()

    rdir = E.run_dir(args.run_id)
    if not rdir.is_dir():
        raise SystemExit(f"no run at {rdir}; run run.py first")
    manifest = E.read_json(rdir / "manifest.json") if (rdir / "manifest.json").exists() else {}
    offers = E.load_offers()
    coupons = E.coupon_codes(offers)
    brands = E.brand_names(offers)
    universe = E.all_codes()

    grades_path = rdir / "grades.jsonl"
    cached: dict[str, dict] = {}
    if grades_path.exists() and not args.regrade:
        with open(grades_path, encoding="utf-8") as f:
            cached = {g["file"]: g for g in (json.loads(l) for l in f if l.strip())}

    judge, judge_note = None, None
    if args.no_judge:
        judge_note = "LLM passes disabled by --no-judge"
    else:
        try:
            judge = make_judge(args.judge, args.judge_model)
            print(f"LLM passes: {args.judge_model} via {judge.name}")
        except Exception as e:
            judge_note = f"LLM passes disabled: {e}"

    # 1. deterministic grades
    rows, starts, ends, fresh = [], [], [], []
    files = list(E.iter_run_files(args.run_id))
    for assistant, f in files:
        key = str(f.relative_to(rdir))
        rec = E.read_json(f)
        s, e_ = parse_ts(rec.get("started_at")), parse_ts(rec.get("finished_at"))
        if s and e_:
            starts.append(s); ends.append(e_)
        if key in cached and args.rescore:
            row = cached[key]
            # the run file may have been re-asked since (rerun_stale.sh): refresh what comes from the record itself
            row.update({"expected": rec.get("expected") or [], "primary": rec.get("primary"), "prompt": rec.get("prompt"),
                        "started_at": rec.get("started_at"), "finished_at": rec.get("finished_at"), "latency_s": rec.get("latency_s"),
                        "error": rec.get("error"), "stop_reason": rec.get("stop_reason"), "queries": rec.get("queries") or []})
            row.update(grade_record(rec, offers, coupons, brands, universe))
            row["_text"] = rec.get("text") or ""
            rows.append(row); continue
        if key in cached:
            rows.append(cached[key]); continue
        g = grade_record(rec, offers, coupons, brands, universe)
        row = {"file": key, "source": "api", "run_id": rec.get("run_id"), "assistant": assistant, "model": rec.get("model"),
               "qid": rec["qid"], "kind": rec.get("kind"), "tier": rec["tier"], "n": rec["n"], "prompt": rec.get("prompt"),
               "expected": rec.get("expected") or [], "primary": rec.get("primary"), "started_at": rec.get("started_at"),
               "finished_at": rec.get("finished_at"), "latency_s": rec.get("latency_s"), "error": rec.get("error"),
               "stop_reason": rec.get("stop_reason"), "queries": rec.get("queries") or [], **g,
               "picks": [], "our_rank": None, "catalog_rank": None, "judge_error": judge_note,
               "explanation": None, "explanation_verbatim": None, "d1_fetched_slugs": [],
               "failure_class": None, "failure_evidence": "", "_text": rec.get("text") or ""}
        rows.append(row); fresh.append(row)

    # 2. D1: fetches in the run window, and the rows behind any click ids seen in linked network URLs
    d1 = {"note": None, "rows": [], "by_assistant": {}, "click_id_rows": [], "stale_click_ids": []}
    deploy_at = parse_ts((manifest.get("stamp") or {}).get("worker_deployed_at"))
    stale_ids: set[str] = set()
    if args.no_d1:
        d1["note"] = "skipped (--no-d1)"
    elif manifest.get("mock"):
        d1["note"] = "mock run; D1 not queried"
    elif not starts:
        d1["note"] = "no run files with timestamps"
    else:
        start, end = min(starts) - timedelta(minutes=2), max(ends) + timedelta(minutes=2)
        d1rows, err = d1_ai_fetch_rows(start, end)
        d1.update(note=err, window=[start.isoformat(), end.isoformat()], rows=d1rows)
        by: dict[str, list] = {}
        for r in d1rows:
            by.setdefault(r["assistant"], []).append(r["slug"])
        d1["by_assistant"] = {a: sorted(set(v)) for a, v in by.items()}
        slack = timedelta(seconds=3)   # app chats run back to back ~20 s apart; a wider slack attributed a neighbour's fetch
        for row in rows:
            s, e_ = parse_ts(row.get("started_at")), parse_ts(row.get("finished_at"))
            ua_name = E.UA_ALIAS.get(row["assistant"], row["assistant"])   # claude-code fetches arrive as Claude-User
            if s and e_:
                row["d1_fetched_slugs"] = sorted({r["slug"] for r in d1rows if r["assistant"] == ua_name
                                                  and (ts := parse_ts(r["ts"])) and s - slack <= ts <= e_ + slack})
        ids = {i for row in rows for i in row.get("click_ids") or []}
        if ids:
            crows, cerr = d1_click_id_rows(ids)
            d1["click_id_rows"] = crows
            cutoff = deploy_at or min(starts)
            d1["stale_cutoff"] = cutoff.isoformat() + ("" if deploy_at else " (run start; Worker deploy time unknown)")
            stale_ids = {r["click_id"] for r in crows if (ts := parse_ts(r["ts"])) and ts < cutoff}
            d1["stale_click_ids"] = sorted(stale_ids)
            if cerr:
                d1["note"] = (d1["note"] or "") + f"; click-id lookup failed: {cerr}"
    E.write_json(rdir / "d1-ai-fetch.json", d1)

    # 3. failure class + LLM passes (fresh rows only; --rescore recomputes the class of cached rows too)
    if args.rescore:
        for row in rows:
            if row not in fresh:
                row["failure_class"], row["failure_evidence"] = classify_failure(row, stale_ids)
                row.pop("_text", None)
    for i, row in enumerate(fresh, 1):
        row["failure_class"], row["failure_evidence"] = classify_failure(row, stale_ids)
        text = row.pop("_text")
        if judge and row["kind"] == "question" and row["tier"] in ("A", "B", "E") and row["level"] >= 1 and text:
            try:
                row.update(judge_rank(judge, args.judge_model, text, offers, set(row["expected"])))
            except Exception as e:
                row["judge_error"] = f"{type(e).__name__}: {e}"
        if judge and row["tier"] in E.LINK_TIERS and row["failure_class"] and row["failure_class"] != "NOT_FOUND" and text:
            try:
                row.update(explain_link(judge, args.judge_model, text))
            except Exception as e:
                row["judge_error"] = f"{type(e).__name__}: {e}"
        print(f"[{i}/{len(fresh)}] {row['file']}: {row['level_label']}"
              + (f" {row['failure_class']}" if row["failure_class"] else "") + (" bypass" if row["bypass"] else "")
              + (f" {row['code_class']}" if row.get("code_class") and row["code_class"] != "NO_CODE" else "")
              + (f" rank={row['our_rank']}" if row["our_rank"] else "") + (f" ERROR {str(row['error'])[:80]}" if row["error"] else ""),
              flush=True)
    for row in rows:
        row.pop("_text", None)
    if judge and judge.usage.get("calls"):
        # Token accounting for the LLM passes, summed over every grade.py run on this run id (the iteration report reads it).
        up = rdir / "judge-usage.json"
        acc = E.read_json(up) if up.exists() else {}
        for k, v in judge.usage.items():
            acc[k] = round(acc.get(k, 0) + v, 6) if isinstance(v, float) else acc.get(k, 0) + v
        acc.update({"model": args.judge_model, "backend": judge.name, "updated_at": E.now_iso()})
        E.write_json(up, acc)
        print(f"LLM passes: {judge.usage['calls']} calls this run; totals in {up.name}")

    with open(grades_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
    print(f"graded {len(rows)} run files ({len(fresh)} new) -> {grades_path}")

    # 4. UI spot-check merge
    ui_csv = find_ui_csv(args, rdir, manifest)
    if ui_csv:
        q = E.load_questions()
        exp_by_q = {x["id"]: set(x.get("expected") or []) for x in q["questions"]}
        for row in rows:  # the run's own expected list wins (slug rotation may have changed the primary)
            if row["kind"] == "question":
                exp_by_q[row["qid"]] = set(row["expected"])
        ui_rows = [grade_ui_row(r, offers, exp_by_q.get(r.get("qid"), set()), stale_ids) for r in E.read_ui_csv(ui_csv)]
        with open(rdir / "grades-ui.jsonl", "w", encoding="utf-8") as f:
            for r in ui_rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"UI spot-check: {len(ui_rows)} rows from {ui_csv} -> grades-ui.jsonl "
              f"(L4-ui {sum(r['l4_ui'] for r in ui_rows)}/{len(ui_rows)})")
    else:
        print("UI spot-check: no CSV found (pass --ui-csv, or put ui.csv in the run folder)")

    if judge_note:
        print(judge_note)
    print(f"D1: {d1['note']}" if d1["note"] else
          f"D1: {len(d1['rows'])} ai_fetch rows in window; by assistant: {d1['by_assistant']}; stale click ids: {d1['stale_click_ids']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
