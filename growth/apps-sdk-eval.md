# DLC-145: OpenAI Apps SDK as a channel (memo, read Nov 2026)

**Verdict: wait-for-trigger.** Do not build now. Rules do not clearly forbid us, but reach is tiny and unproven, and the checkout and "not an ad vehicle" rules are a real rejection risk. Revisit if (a) OpenAI documents in-chat app suggestions for shopping queries, or (b) the 10-sales goal stalls with the organic path saturated.

## What the rules say
All from OpenAI's submission guidelines (https://developers.openai.com/apps-sdk/app-submission-guidelines, fetched Nov 2026, no "last updated" date shown; the page now says "plugins" where older docs said "apps").
- Affiliate, referral, commission, sponsored, redirect: none of these words appear. Silent, so no explicit ban and no explicit permission. A third-party guide calls affiliate links permitted if relevant and disclosed; that is interpretation, not policy.
- Advertising: plugins "must not serve advertisements and must not exist primarily as an advertising vehicle." An app whose only job is to push affiliate links risks being read this way. It needs standalone value (search and compare offers).
- Checkout: plugins may not "Link directly to a checkout or other transactional page." External checkout on "your own domain" is the required model. Our `/go/` links go to a merchant's cart, not our domain. Likely a conflict, and the biggest unknown.
- Descriptions may not advertise "pricing, subscriptions, free trials, discounts, or promotions." Listing text can't say "coupon codes"; the codes could appear only in tool output. Likely awkward for a coupon app.
- Commerce is limited to physical goods (ours are). Metadata must not "interfere with fair discovery."
- Instant Checkout is beta/select partners only; the search coverage says OpenAI pulled back in-chat checkout around March 2026 (secondary sources, dates differ). Rankings are described as organic and unsponsored.

## Discovery
- OpenAI docs: discovery via name mention, directory browsing, and model suggestion based on tool metadata and past usage (quoted in a search summary; the user-interaction page 404'd for me, so I did not read it directly).
- Suggestions: OpenAI ran in-chat app suggestions in Dec 2025, users read them as ads, and OpenAI turned them off (TechRadar and others, secondary). I found no confirmation they are back.
- OpenAI forum thread, Apr-May 2026 (https://community.openai.com/t/when-do-our-apps-surface-to-users-clarification-requested/1379612): staff said directory listings are "fairly manual"; developers report ~50 users/day and "effectively nonexistent" discovery; category pages show mostly large brands.
- Implication: reach is users who search the directory or name the app. A coupon site nobody has heard of gets near zero, versus the organic path where ChatGPT already fetches our pages for ordinary shopping queries and returns `/go/` links (the source of our first sale). The card widget would only help the few who connect the app.

## Build cost (estimate, mine)
- MCP server (stable public HTTPS, e.g. a Cloudflare Worker next to `dealectric-edge`) with 1-2 read-only tools over the existing `https://dealectric.com/offers.json`: about 1-2 days.
- Card widget (iframe component; docs say iframes "may require additional review"): 1-2 days.
- Submission package: 5 positive and 3 negative test cases, video walkthrough, release notes, privacy/support contact, test creds (none needed if no sign-in): about 1 day. Review time not documented. Rejection risk from the rules above; each metadata change needs re-review.
- Ongoing: tool changes are rescanned daily; low upkeep. Total roughly 3-5 days of agent work plus Barry's review-submission touches.

## Ownership
Org owner submits, or a member with Apps Management Write. Publishing needs individual or business verification in the OpenAI platform org settings, and misrepresentation can get removal. Use the Agentify LLC once formed (filed 11-01); a personal-name listing would be harder to move later. Needs a verified domain and support contact (barrryyao@gmail.com or a dealectric.com address). Needs a platform org Barry controls; the existing API-key org may not be the right one.

## Could not verify
- Whether affiliate/coupon apps have been approved or rejected (no case found).
- Whether the `/go/` 302 to a merchant cart counts as "linking directly to a checkout page."
- Whether in-chat app suggestions for shopping are live today.
- Review turnaround; the user-interaction doc page; OpenAI's separate usage policies and "apps" terms (not read).
- All build costs are my estimates.
