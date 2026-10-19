# Agent checkout over an API ("route 1") — research, 2026-10-17

How an assistant buys for a shopper without a browser, and where Dealectric could fit. Based on the two open standards: OpenAI + Stripe's **Agentic Commerce Protocol (ACP)** and Google's **Universal Commerce Protocol (UCP)**. Spec details are from the official spec pages; rollout status is from secondary reporting and is less certain.

## The two standards

| | ACP | UCP |
|---|---|---|
| Maintained by | OpenAI and Stripe | Google, with Shopify, Etsy, Wayfair, Target, Walmart, Amazon, Microsoft, Meta, Stripe and others |
| Where shoppers see it | ChatGPT (Instant Checkout) | Google AI Mode and the Gemini app |
| Status (secondary sources, unverified) | Live since Sept 2025; reports say OpenAI scaled back in-chat checkout in March 2026 and shifted to discovery, while the protocol kept evolving (cart, orders, MCP added 2026-04-17) | Checkout rolling out since Feb 2026 in the US, Etsy and Wayfair first; Shopify, Target, Walmart integrating |
| Who sells | The merchant is merchant of record in both; the platform isn't a store |
| Fee | One guide says 4% to OpenAI per order | Not disclosed |

## The journey, step by step

**1. The merchant publishes its catalog to the platform, ahead of time.**
- ACP: a product feed (JSON/CSV, refreshed daily) sent to OpenAI: IDs, prices, stock, shipping, images.
- UCP: the merchant's Google Merchant Center feed, with a `native_commerce` flag so a Buy button can appear. It also publishes a profile at `/.well-known/ucp` listing what it supports (checkout, discounts, payment methods).

**2. The shopper asks, and the assistant picks products.**
Picks come from the platform's catalog (the feeds) and its own ranking. The assistant may also read the web for advice ("which power station for a fridge?"). **This is the only step where web content like ours can still influence the outcome**, and only as background reading.

**3. The shopper says "buy it". The assistant opens a checkout with the merchant.**
A server-to-server call: ACP `POST /checkout_sessions` with `items`, `buyer` (name, email, phone) and `fulfillment_address`. UCP Create Checkout with `line_items`, sending a `UCP-Agent` header that identifies the platform. The merchant replies with the full cart: line items, tax, shipping options, totals.

**4. The cart gets refined.**
The assistant updates the session (shipping choice, quantity, **discount codes**). The status moves through ACP `not_ready_for_payment → ready_for_payment`, or UCP `incomplete → ready_for_complete`. If the merchant needs something the API can't do (age check, account login, review), UCP returns `requires_escalation` with a `continue_url`, and the shopper finishes on the merchant's own website.

**5. Payment, without the assistant seeing the card.**
The shopper confirms in the assistant's UI. ACP: OpenAI gets a one-time Stripe *Shared Payment Token* capped at the order amount. UCP: Google Pay through a "payment handler" (AP2 mandates for fully delegated buying). The assistant calls Complete with the token (ACP `POST /checkout_sessions/{id}/complete` with `payment_data.token`). The merchant charges it through its normal processor.

**6. Order and after-sale.**
The merchant returns an order ID and a link to the order. Shipping updates, returns and support come from the merchant via webhooks (UCP order capability, ACP orders spec).

No web page is loaded, no JavaScript runs and no cookie is set at any step. The merchant's server receives API calls from OpenAI's or Google's servers.

## Where an affiliate could get credit

| Mechanism | ACP | UCP | What it means for us |
|---|---|---|---|
| Affiliate / referrer field | None | `attribution` object: campaign source, medium and name, click IDs (e.g. `gclid`). Filled in **by the platform** and copied onto the order. The spec says it sets no attribution model and "MUST NOT affect the response" | The platform tags its own referral. No slot for a third party like us. |
| **Discount codes** | `discounts.codes` (string array) on create/update; merchant answers with `discounts.applied` or `discounts.rejected` (e.g. `discount_code_expired`) | `discounts.codes` on cart/checkout create/update; applied codes go in `discounts.applied`, rejections in `messages[]` | **The one way in.** Neither spec says where codes come from: the shopper or the agent can supply them. A code tied to our affiliate account, applied by the agent, gets recorded on the order. |
| Hand-off to the merchant's site | — | `continue_url` on escalation | The shopper lands on the merchant's checkout via the platform's link, not ours. No affiliate click. |

## What this means for Dealectric

1. **Links and cookies are worthless here.** The sale happens between platform and merchant servers. Our CJ/Awin links never run.
2. **Codes are the one way in, and agents are built to apply them.** Both specs let the agent submit codes and tell it right away whether each worked. An agent looking for the best price would want a source of *working, checked* codes, which is what DLC-29 and DLC-30 produce. Commission only follows if the code is tied to our publisher account and the merchant's network records code redemptions (CJ and Awin both support coupon-code attribution, but each brand has to set it up). That's the question to put to each brand in DLC-30.
3. **Being the agent's source of codes and data.** An offers API / MCP server (DLC-27) that returns verified codes per merchant is something a shopping agent could call during step 4. Both specs are adding MCP support, so that's the natural interface.
4. **Content still shapes step 2,** but it earns nothing on its own here. Whatever earns has to arrive as a code in step 4.

## Open questions

- Does ChatGPT or Gemini actually let a shopper or agent type in a code during in-chat checkout today, or only apply automatic discounts? The spec allows it; the product may not offer it.
- Are our brands live on either? BLUETTI, Soundcore, Baseus, ESR and ALLPOWERS run Shopify stores; one guide claims Shopify turns UCP on by default for all merchants (unverified).
- Do CJ/Awin credit code-only redemptions for these specific brands, and will the brands issue us an exclusive code?

## Sources
- ACP checkout spec: https://developers.openai.com/commerce/specs/checkout
- ACP key concepts: https://developers.openai.com/commerce/guides/key-concepts
- ACP repo and versions: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol
- ACP discount RFC: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol/blob/main/rfcs/rfc.discount_extension.md
- UCP home: https://ucp.dev
- UCP checkout: https://ucp.dev/latest/specification/shopping/checkout/
- UCP cart: https://ucp.dev/latest/specification/shopping/cart/
- UCP discount extension: https://ucp.dev/latest/specification/shopping/extensions/discount/
- UCP overview (attribution, platform identity): https://ucp.dev/latest/specification/overview/
- Rollout reporting: https://www.thekeyword.co/news/google-rolls-out-ucp-powered-checkout-inside-ai-mode-and-gemini , https://www.emarketer.com/content/google-brings-checkout-ai-mode-races-rivals-agentic-commerce , https://www.hypotenuse.ai/blog/chatgpts-instant-checkout-the-next-phase-of-agentic-commerce , https://blog.lengow.com/chatgpt-wanted-to-become-the-worlds-biggest-shop , https://launchcodex.com/blog/web-digital-infrastructure/universal-commerce-protocol-merchant-guide/
