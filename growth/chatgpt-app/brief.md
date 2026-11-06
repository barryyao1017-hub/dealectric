# Dealectric ChatGPT app: go/no-go brief (2026-11-06)

**Status 2026-11-06: built (Barry's yes).** The server is `worker/src/mcp.js` at `https://dealectric.com/mcp`, with
three tools: `search_products`, `check_codes` and `price_history`. Its data is `/offers.json` plus the new
`/price-history.json` (48 products, 336 daily readings since 10-21). Calls are logged in D1 `mcp_calls`, and the
privacy page has a new section on them. Worker usage notes: `worker/README.md`.

Changes from the plan below:
- **Amazon records are left out of the app.** Their tagged links and prices follow Amazon's own rules, which name
  approved sites, not apps.
- **The tool is `search_products`,** not `find_products`.
- **Checkout links:** `/go/<slug>?via=app` sends the three checkout-landing BLUETTI records (Elite 200 V2, AC200L, Elite
  30 V2 solar kit) to their product page instead. The AC200L product page rendered no buy button in October (DLC-71),
  so that one may be a dead end inside the app.

Still Barry's:
- OpenAI developer verification.
- The video walkthrough.
- The yes on submitting.
- Before submitting, check each CJ and Awin program's terms for limits on promoting through software or apps.
  `growth/codes/program-terms.md` doesn't mention any, but it wasn't written with apps in mind.

**Recommendation: conditional go.** Build a small MCP server on the existing Worker. It must stand on its own as a
price-and-code checker, not as a link list. Then submit. The rules allow physical-goods commerce and don't mention
affiliate links either way. Two rules could be read against us (below), so treat approval as uncertain. A rejection costs
the build time and nothing else: OpenAI allows an appeal or a corrected resubmission.

## Why

Agents don't create backlinks. An app gets suggested by ChatGPT on what the app's tool descriptions say and on use. It
does not depend on ranking in OpenAI's index. The guidelines say plugins that show "strong real-world utility and high
user satisfaction" may get directory placement or proactive suggestions. The same server can also be offered to Claude
and to MCP registries. I haven't checked their rules.

## What OpenAI's live guidelines say (read 2026-11-06)

Sources: [submission guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines),
[developer guidelines](https://developers.openai.com/apps-sdk/app-developer-guidelines),
[submission flow](https://developers.openai.com/plugins/deploy/submission). Apps are now submitted as "plugins".

| Rule | Effect on us |
|---|---|
| Commerce only for physical goods | Fits: every product we list is physical. |
| Affiliate or referral links | **Not mentioned.** No rule for or against them. |
| "Must not exist primarily as an advertising vehicle"; must deliver standalone functionality | **Main risk.** A tool that only returns buy links could be read as advertising. Mitigation: the tools answer questions with checked data (does this code work today, is this a good price, which model fits), and links are secondary. |
| Name and description: "Do not advertise pricing ... discounts, or promotions" | This applies to the listing text, not to tool results. The description has to say what the app does ("checks whether a brand's discount codes work in its own cart") without pitching savings. Second risk: a reviewer may count describing discount codes at all as advertising them. |
| Plugins may not "link directly to a checkout or other transactional page" | **Conflicts with our pre-applied links**, which open the store's checkout with the code applied (`cart_variant`). In the app, link to product pages only (the `/go/` "store" kind). This removes one of our two selling points inside ChatGPT. |
| No model-readable text that steers the model toward us over other plugins; descriptions must match behaviour | Same as our Claude-line rule (DLC-59). Plain descriptions only. |
| Minimal data, no tracking or profiling, never reconstruct the chat; published privacy policy | Log only tool name, arguments, time and click IDs. `/privacy` exists; add an MCP section. |
| Verified individual or organization; support contact | Barry verifies, as himself or as Agentify LLC. `/contact` exists. |
| Availability can be limited by country (`publication.countries`) | US only, consistent with the US-only rule (DLC-155). |

## What we would build

- **Endpoint:** a remote MCP server at `https://dealectric.com/mcp` on the existing Worker. It needs no sign-in
  (allowed: "none" auth), so reviewers need no demo account. Domain check: serve the token at
  `/.well-known/openai-apps-challenge`.
- **Tools** (read-only, from data we already have):
  1. `check_code(product or brand)`: the codes published for it, the last cart test date and the result (subtotal →
     total).
  2. `price_check(product)`: today's store price, the lowest and highest in the cart-test log, and whether the price
     dropped. Built from `growth/codes/*-checks.jsonl`, which holds 847 checks since 10-21.
  3. `find_products(category, budget, need)`: matching catalog products with key specs, dated price, code status and
     a `/go/` product-page link.
- **Data:** `build.py` writes `offers.json` and a new price-history JSON. The Worker reads them, so the Daily sweep
  keeps the data fresh with no new job.
- **Logging:** one D1 row per tool call. `/go/` links from the app carry an `mcp` tag in the sub-ID, so a sale through
  the app shows up in CJ and Awin.
- **Listing assets:** name "Dealectric", short and long descriptions, square icon, 5 positive and 3 negative test
  prompts, a video walkthrough URL, release notes, and links to website, support, privacy and terms (all exist).

Effort: about one working session for the server and data, plus a session for tests and the submission package. Work
laptop note: the corporate proxy blocks dealectric.com, so live tests of the endpoint run from the old Mac or through
the Agent Chrome.

## What Barry does (about 1 hour)

1. **Yes or no** on building and deploying `/mcp` (public endpoint on dealectric.com).
2. **OpenAI developer verification**, as an individual or for Agentify LLC (his ID, so his step).
3. **Record the video walkthrough** (a few minutes of screen recording in ChatGPT Developer Mode) and upload it where
   reviewers can open it.
4. **Yes or no on submitting**, and on the policy attestations. Both are outward-facing, so consent-by-brief applies.

## How we'd judge it

- **Approval:** approved, or rejected with a reason. A rejection for "advertising vehicle" ends the ChatGPT route;
  the server stays useful for Claude and the MCP registries.
- **Use:** outside tool calls per week in D1, and `/go/` clicks and sales tagged `mcp`. There is no stop date (Barry's
  rule). Read it in the Daily report once live.

## Open questions this brief can't settle

- Whether a reviewer reads "discount codes" in the description as advertising. Only a submission answers that.
- How much traffic early apps get. OpenAI publishes no numbers, and developers on its forum say discovery is opaque.
