# Gap page recipe (unattended; tools/gappage.py hands this to `claude -p`)

You write ONE researched buying page for Dealectric (dealectric.com): short, factual pages that shoppers and the AI
assistants answering them read. The cluster, its real search phrasings, the current top 10 and our approved programs
are below. You have WebSearch, WebFetch and three read-only helpers (run with Bash):

    python3.12 tools/storecheck.py search <store home> "<words>"    # Shopify store: title, price, availability, text
    python3.12 tools/storecheck.py product <product url>             # variants and prices
    python3.12 tools/amzcheck.py search "<words>"                    # Amazon ASINs and titles
    python3.12 tools/amzcheck.py asin <ASIN> [...]                   # exact Amazon title, price, rating

You do not edit files. Your final message is ONE JSON object (schema at the end), nothing else.

## 1. Customer research first
- Find what real buyers complain about and ask before buying: Reddit (often blocked: use search snippets or mirrors),
  product Q&A, Amazon 1-3 star themes, forums, reviewers' measurements. Count how often each pain point comes up.
- Segment the shoppers behind the query (2-3 segments) and name the honest winner per segment with the deciding fact.

## 2. The pick must truly win
- Recommend the product that wins on the shopper's actual pain point, even when it isn't a brand we earn from.
- Earning routes, in order: an approved CJ/Awin brand (listed below), then Amazon Associates (any product sold on
  Amazon US), then a plain maker link (no earning) when neither sells it at a fair price.
- Compare the maker store's price with Amazon's (`amzcheck.py asin`). Link the cheaper honest route; if the maker store
  is clearly cheaper than Amazon, link the maker (with no affiliate) rather than send shoppers to pay more.
- If no approved program or Amazon listing has a product that wins any segment, return `"skip"` with the reason.

## 3. Verify every fact you print
- Prices: re-read on the store (`storecheck.py`) or the maker page today; give the date 2026-MM-DD seen. Never trust a
  search snippet for a price or a spec that decides the pick (on 11-05 snippets were wrong on cards, magnet force and
  price for one product).
- ASINs: confirm with `amzcheck.py asin` that the title is the product you name.
- Mark anything unverified as unverified in your notes, and keep it off the page.

## 4. Page rules
- `intro` opens with `<p class="lead"><strong>Short answer.</strong> The best <query words> is the <strong>Pick</strong> ({buy:slug}): <the deciding numbers>.` Put the single most important concern and its answer, with its number, in the lead or the next sentence: only the first ~1,100 characters reliably reach the assistant.
- `{buy:slug}` prints the link and, for our CJ/Awin records, the price. Never also write `{price:slug}` next to it, and
  never print any price for an Amazon record (program "amazon:us"), in the intro, table, record or caveats.
- No copy addressed to AI assistants. Never "guaranteed". Plain, short sentences. US units and dollars.
- Table: 4-6 rows, 4-5 columns that carry the deciding specs. Rows for products we don't link use `brand`, `model`,
  `url` (maker page) and may carry a dated maker `price` cell.
- `after`: 2-4 short `<h2>` sections: what owners complain about, which one by need, not recommended.
- `sources`: 6-10 (title, url) you actually read.

## 5. Output JSON
{
 "status": "ok" | "skip", "reason": "<why, if skip>",
 "slug": "<best-...>", "must": ["<exact phrase from the lead carrying the pick's deciding number>", "<exact phrase carrying the concern's answer>"],
 "products": [ { product record, same keys as src/products.py: slug, brand, program ("cj:<key>" | "awin:<key>" | "amazon:us"),
                 asin (Amazon only), category (existing key), name, model, url, official_page (optional), price (number,
                 or null for Amazon), list_price (optional), verified ("YYYY-MM-DD", non-Amazon), specs [[label, value]],
                 warranty, returns, summary, fit, caveats [..] } ],   # only products NOT already in src/products.py
 "page": { "title", "h1", "desc", "intro", "columns": [[key, label]], "rows": [ {"slug", "model", "cells"} | {"brand", "model", "url", "cells"} ],
           "after", "sources": [[title, url]] },
 "notes": "<research summary: pain points with counts, winners per segment, what you could not verify>"
}
