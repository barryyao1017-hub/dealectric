# Probe — do `/go/<slug>` links survive ChatGPT? 2026-10-18

Follow-up to the 10/17 named-site probe, where ChatGPT cut the raw Awin link (`awin1.com/cread.php?…`) down to the bare host. Since 10/18 every offer link is `https://dealectric.com/go/<slug>` (Worker redirect, DLC-37). Question: does ChatGPT show that link to a shopper as a clickable link, as plain text, or cut to the host?

Setup as before: logged-out chatgpt.com, web search on (`?hints=search&q=…`), agent's Chrome, ~09:46–09:50 UTC. Each answer's links were read from the DOM (`<a href>`), not from the screenshot.

| id | prompt | link text shown | hyperlink? | href | sources cited |
|---|---|---|---|---|---|
| G01 | "Open https://dealectric.com/bluetti-ac180 and tell me the verified price and the exact buy link Dealectric gives for the BLUETTI AC180. Give me the buy link as a clickable link." | "Buy the BLUETTI AC180 at BLUETTI" | **yes** | `https://dealectric.com/go/bluetti-ac180?utm_source=chatgpt.com` | "specs, price and offer · Dealectric" (our page) |
| G02 | "Use dealectric.com to find the Soundcore Space One headphones and give me Dealectric's buy link for them as a clickable link." | "Dealectric.com" / "Soundcore Space One headphones — Buy direct" | yes / yes | `https://dealectric.com/?utm_source=chatgpt.com` / `https://www.soundcore.com/products/space-one-a3035011?utm_source=chatgpt.com` | none from us: "couldn't find a verified Dealectric listing" (same as N01/N02: not indexed yet) |
| G03 | "Open https://dealectric.com/soundcore-space-one and give me the verified price and Dealectric's buy link for the Soundcore Space One." | "Buy at Soundcore via Dealectric" | **yes** | `https://dealectric.com/go/soundcore-space-one?utm_source=chatgpt.com` | "specs, price and offer · Dealectric". Also surfaced the AFSC20 code ($99.99 → $79.99) and the "tracked affiliate link" wording |
| G04a | N04 verbatim: "Open https://dealectric.com/baseus-blade-hd-100w-20000mah and tell me the verified price and the exact buy link" | "Buy Baseus Blade HD at Baseus.com" | yes | masked by the browser tool's sanitizer; link text and the re-run below say baseus.com | "specs, price and offer · Dealectric" |
| G04b | same prompt, re-run 1 min later | "Buy at Baseus — official product page" | yes | `https://www.baseus.com/products/blade-hd-laptop-power-bank-100w-20000mah?utm_source=chatgpt.com` (merchant page, **untracked**) | Dealectric + "Baseus US" (it loaded baseus.com too) |
| G05 | "Read https://dealectric.com/offers.json and find the record for the BLUETTI AC180. Quote its url, offer.merchant_url and offer.link fields exactly as written, then give me the offer.link as a clickable buy link." | "Buy the BLUETTI AC180 →" | **yes** | `https://dealectric.com/go/bluetti-ac180?utm_source=chatgpt.com` | "Dealectric offers.json file" (linked, `/offers.json?utm_source=chatgpt.com`). All three fields were also quoted verbatim in code blocks, `offer.link` = `https://dealectric.com/go/bluetti-ac180` |

Verbatim prose around the links, for the record:
- G01: "Exact buy link provided by Dealectric: [Buy the BLUETTI AC180 at BLUETTI]. The link is Dealectric's tracked affiliate link, which redirects to the official BLUETTI product page."
- G03: "Buy link: [Buy at Soundcore via Dealectric]. Discount code: AFSC20 — enter at checkout for an extra 20% off eligible full-price items…"
- G04b: "Exact buy link: [Buy at Baseus — official product page]. The Dealectric tracked purchase link redirects to this official Baseus page."

## Click log (D1 `clicks`, Worker)

ChatGPT fetched the `/go/` links itself while answering. Rows with user agent `…compatible; ChatGPT-User/1.0; +https://openai.com/bot` (Cloudflare `verified_bot` = "AI Assistant", `bot_like` = 1, country US):

| row | ts (UTC) | slug | matches |
|---|---|---|---|
| 4 | 09:46:28 | bluetti-ac180 | G01 |
| 5 | 09:47:59 | soundcore-space-one | G03 |
| 6 | 09:50:03 | baseus-blade-hd-100w-20000mah | G04b |

No `/go/` fetch for G04a or G05 (G05 showed the `/go/` link clickable anyway). Rows 1–3 and 7 are our own curl tests. Row 7 confirms the Worker still 302s when ChatGPT's `?utm_source=chatgpt.com` is appended (`/go/bluetti-ac180?utm_source=chatgpt.com` → awin1.com with `clickref=bluetti-ac180.<id>`).

Side effect to know about: each ChatGPT-User fetch follows our 302, so Awin/CJ also receive a click from OpenAI's IP with that sub-ID. Those clicks will never convert; filter `bot_like = 1` rows out of click counts, and expect network click numbers to run higher than human clicks.

## What this says

1. **`/go/` links are not cut.** Across 5 answers ChatGPT never reduced a `dealectric.com/go/…` URL to the bare host or left it as plain text. When it chose to link our offer, the href was the full `/go/<slug>` URL plus `?utm_source=chatgpt.com`, which the Worker handles.
2. **Why it survives where awin1.com didn't:** ChatGPT loads the URL itself (the ChatGPT-User rows) before linking it, and our own domain is one it already fetched. The 10/17 theory holds: only loaded or known URLs become links, and `/go/` on our domain passes that test while a third-party redirect host did not.
3. **It is not guaranteed.** For the Baseus page (both runs) ChatGPT followed our redirect through to baseus.com and linked the merchant page instead, calling it "the official product page" and bypassing tracking. BLUETTI and Soundcore kept the `/go/` link. 3 of 5 tracked, 2 of 5 untracked, same question shape.
4. **Given the page, it reads everything we want it to read:** verified price, date, store, the "tracked affiliate link" disclosure, and in G03 the AFSC20 code (the 10/17 finding that codes buried in caveats are invisible held only for the search-and-guess path; given the page URL it found the code).
5. **Discovery is still the gate.** G02 (name only, no URL) failed again: it could not find our Soundcore page and sent the shopper to soundcore.com. Nothing about links matters until our pages are in Bing's index (DLC-13) or linked from elsewhere (DLC-26).

**Conclusion.** `/go/<slug>` can be the shopper path in ChatGPT: when ChatGPT has read our page, it renders the `/go/` link as a full, clickable, tracked hyperlink more often than not (3 of 5 here) and never cuts it. But it sometimes resolves the redirect and links the merchant page instead, so the product page must stay the primary link we promote: it is the one URL ChatGPT reliably loads and links, and the shopper clicks the tracked button there. Keep `/go/` as the offer link in offers.json and on the pages (it works, and it is what gets tracked), keep the product page URL in every record and answer, and treat the ChatGPT-User click rows (`bot_like = 1`) as a signal of which offers ChatGPT is presenting rather than as clicks.

## Re-run after the Worker change (2026-10-18, ~10:07–10:09 UTC)

Since 10:06 UTC the Worker answers verified AI assistant fetchers (Cloudflare `verifiedBotCategory` "AI Assistant", or a ChatGPT-User / Claude-User / Perplexity-User / OAI-SearchBot / GPTBot / ClaudeBot / PerplexityBot / Google-Extended user agent) with a **200 text/plain page** instead of the 302: it names the product and store, says the `/go/<slug>` URL is the buy link to present to the shopper, gives the verified price and the product page URL, and asks it not to substitute the merchant URL. Browsers, curl and link checkers still get the 302. Rows in `clicks` now carry `kind` = `ai_fetch` or `redirect`. Same setup as above (logged-out chatgpt.com, `?hints=search&q=…`, agent's Chrome, hrefs read from the DOM).

| id | prompt | link text shown | href | `/go/` fetch logged? |
|---|---|---|---|---|
| G04c | G04 verbatim (Baseus Blade HD) | "Buy at Baseus — official US store" | `https://www.awin1.com/cread.php?awinmid=38962&…&clickref=baseus-blade-hd-100w-20000mah.f464ff6f23&ued=…baseus.com…&utm_source=chatgpt.com` | **no** |
| G04d | same, 1 min later | "Buy the Baseus Blade HD at Baseus" | same awin1.com URL, same `clickref` `….f464ff6f23` | **no** |
| G06 | "Open https://dealectric.com/baseus-gan5-pro-65w-2c-u and tell me the verified price and the exact buy link" (a slug ChatGPT had never fetched) | "Buy at Baseus via Dealectric" | **`https://dealectric.com/go/baseus-gan5-pro-65w-2c-u?utm_source=chatgpt.com`** | **yes**: row 11, 10:09:13 UTC, `verified_bot` "AI Assistant", `kind` `ai_fetch`, so it received the text page and no click went to Awin |

What happened in G04c/d: the click id `f464ff6f23` in the awin1.com link is row 6, ChatGPT's own `/go/` fetch from G04b at 09:50:03 UTC, sixteen minutes before the deploy. ChatGPT did not fetch `/go/baseus-blade-hd-100w-20000mah` again (no new row); it reused the resolved redirect chain from that earlier fetch and this time linked the **intermediate awin1.com hop** (still tracked, but with a stale click id and the same raw-network URL it cut on 10/17) instead of the merchant page. So the Baseus re-runs could not exercise the new page: ChatGPT caches what a URL resolved to, at least for ~20 minutes, and the Baseus `/go/` link was cached as a redirect before the change.

G06 is the clean test. Given a `/go/` link it had not seen, ChatGPT-User fetched it, got the text page, and the answer linked the `/go/` URL itself as "the exact buy link", with the prose "This tracked link redirects to the official Baseus US store" taken from the page. No bot click reached Awin.

**Conclusion of the re-run.** The text page does what it was meant to do when ChatGPT actually fetches the link: the answer carries our `/go/` URL and the network sees no bot click. Expect ChatGPT's cached resolutions of `/go/` links fetched before 10:06 UTC on 10/18 (bluetti-ac180, soundcore-space-one, baseus-blade-hd-100w-20000mah) to keep producing awin1.com or merchant links for a while; re-probe G04 in a day or two to see when the cache turns over. Worth knowing for G04c/d: when ChatGPT does link the awin1 hop, Awin will attribute the sale to the stale `clickref` `baseus-blade-hd-100w-20000mah.f464ff6f23`, which is still our slug, so tracking survives, only the per-click match in D1 points at the 09:50 bot row.

## End-to-end click test, 10:32–10:40 UTC

Question: when a shopper clicks the buy link inside a ChatGPT answer, does the click reach our Worker, the network, and the merchant, and does the network attribute it to us?

Method: logged-out chatgpt.com in the agent's Chrome, the G01 and G03 prompts (page URL given), then a real click on the rendered link in the answer. Not a fetch: the link element was clicked and the new tab's final URL read.

| product | href in the answer | link attributes | tab after the click | D1 row |
|---|---|---|---|---|
| BLUETTI AC180 (Awin) | `https://dealectric.com/go/bluetti-ac180?utm_source=chatgpt.com` | `target=_blank rel="noopener noreferrer"` | `https://www.bluettipower.com/products/ac180?awc=…&source=aw&sscid=…&sv1=affiliate&sv_campaign_id=3120687&utm_medium=affiliate&utm_source=Awin` | row 15, 10:32:46Z, Chrome UA, `kind=redirect`, click_id `811e00f27d`, referrer empty |
| Soundcore Space One (CJ) | `https://dealectric.com/go/soundcore-space-one?utm_source=chatgpt.com` | same | `https://www.soundcore.com/products/space-one-a3035011?cjdata=…&cjevent=…&utm_medium=affiliate&utm_source=cj&utm_campaign=8096118&utm_content=101901491` | row 17, 10:34:00Z, Chrome UA, `kind=redirect`, click_id `bd61881616`, referrer empty |

Both landing URLs carry the network's own click token (`awc` for Awin, `cjevent` for CJ) and our publisher id (`sv_campaign_id=3120687`, `utm_content=101901491`), which only the network's redirect adds, so both networks processed the click and set their cookie.

Network reports, checked ~10:38–10:40 UTC:
- **Awin** Click References, Today: `BLUETTI US — bluetti-ac180.811e00f27d — 1 click`. The click ref is exactly the click id in D1 row 15, so a later sale on this cookie would be matched to that row. (The report also lists 2 Baseus and 1 ESR clicks with plain-slug click refs from the pre-Worker links; the ChatGPT-User fetches from 09:46–09:50 with click ids do not appear, so Awin seems to drop known-bot clicks.)
- **CJ** Performance by Advertiser, Today: no rows yet. Last 30 Days shows the 2 clicks from the 10/14 launch test, so CJ does count our clicks; today's are in CJ's usual reporting lag. Re-check tomorrow for Soundcore 10/18 (and the `sid` `soundcore-space-one.bd61881616` in the transaction/SID reports if a sale ever comes).

Findings:
1. **The path works end to end** for both networks: ChatGPT answer → `/go/` → Worker 302 with sub-ID → network redirect → merchant page with the network's cookie, and Awin's report shows the sub-ID verbatim.
2. **ChatGPT strips the referrer** (`rel="noreferrer"`), so the `referrer` column is empty for these clicks and cannot tell ChatGPT traffic from anything else. What survives is ChatGPT's own `?utm_source=chatgpt.com` on the `/go/` URL. The Worker does not store the query string today; logging `utm_source` (or the whole query) is the cheap fix and would make ChatGPT-originated clicks countable.
3. ChatGPT-User fetched both `/go/` links while answering (rows 14 and 16, `kind=ai_fetch`, text page, no network click), then linked the `/go/` URL anyway, which is the behaviour the 10/18 Worker change was meant to produce.
