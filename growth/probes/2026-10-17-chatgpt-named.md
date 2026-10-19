# Probe — ChatGPT told to use Dealectric, 2026-10-17

Same setup (logged-out chatgpt.com, web search on). This time the question names dealectric.com, to test the agent path end to end: can it read our data, does it cite us, and does the shopper get a link that earns a commission?

| id | prompt | used our data? | link the shopper gets |
|---|---|---|---|
| N01 | "Use dealectric.com to find me a Soundcore discount code and give me the link to buy." | No: "couldn't verify a Soundcore-specific coupon on dealectric.com". Found AFSC20 via Evreward instead | soundcore.com (untracked) |
| N02 | "What does dealectric.com recommend as a power bank to take on a plane? Give me its buy link." | No: "couldn't find a verifiable recommendation on dealectric.com in the search results" | none |
| N03 | "Read https://dealectric.com/offers.json and recommend a power station that can run a fridge…" | **Yes.** Picked BLUETTI Elite 200 V2, quoted our specs and our `fit` text, cited "Dealectric" | "View Dealectric offer" (our page) and "Official store" (the untracked `merchant_url`) |
| N04 | "Open https://dealectric.com/baseus-blade-hd-100w-20000mah and tell me the verified price and the exact buy link" | **Yes.** $79.99, verified 2026-10-14, cited Dealectric | **Broken:** "Buy at Baseus →" became `https://www.awin1.com?utm_source=chatgpt.com`, which drops the whole tracking path and query |
| N05 | "Check dealectric.com for a verified ALLPOWERS coupon and give me the Dealectric buy link for the R600" | **Yes.** $219, sold out at verification, ALLPOWERS26 credited to Dealectric | `https://dealectric.com/allpowers-r600-299wh?utm_source=chatgpt.com` (our page, works) |

Cloudflare confirms the live fetches: verified `ChatGPT-User/1.0` requested `/offers.json`, `/` and `/baseus-blade-hd-100w-20000mah` at 23:14 UTC.

## What this says

1. **Given a URL, ChatGPT reads our data and trusts it.** It quotes our specs, verification dates and fit notes, and credits Dealectric by name. The data format works.
2. **Given only the name, it can't find us.** N01 and N02 fail because ChatGPT search doesn't have our pages yet (it searches Bing's index). Indexing (DLC-13) and outside links (DLC-26) gate everything else.
3. **Our tracked links don't survive ChatGPT.** It cut the Awin link (`awin1.com/cread.php?awinmid=…&ued=…`) down to the bare host, a dead link that earns nothing. When it does link out, it prefers either our product page (fine: the shopper clicks our button there) or the plain `merchant_url` from offers.json, which bypasses us. See the follow-up below for why: a `/go/<slug>` link probably won't survive either, so the product page is the handoff (DLC-10).
4. **Coupons hidden in caveat text are invisible.** N01: the AFSC20 code is on our Soundcore pages, but only inside a caveat sentence, so ChatGPT didn't find it. Codes need their own field and page (DLC-29).
5. ChatGPT adds `?utm_source=chatgpt.com` to the links it gives out, so ChatGPT referrals to our pages can be counted in Cloudflare Web Analytics.

## Follow-up: why the Awin link was cut (N06)

Prompt: read offers.json and give the record's `url`, `offer.merchant_url` and `offer.link` exactly as written. The model printed all three in full, including the complete `awin1.com/cread.php?…&ued=…` link. So it reads the link correctly. But ChatGPT made none of the three clickable; they stayed plain text.

Taken with N03–N05: the cutting happens in ChatGPT's display layer, not in the model. ChatGPT only shows a URL as a clickable link if it was actually loaded in the chat (our product pages) or is already known from search (baseus.com). Any other URL is shown as plain text or reduced to its host. This matches OpenAI's published safeguard against prompt-injection data leaks through model-written URLs. The Awin redirect is never loaded (opening it would set a tracking cookie), so it gets cut. A `/go/<slug>` link on our own domain would probably be treated the same way. The link that reliably reaches shoppers is our product page.
