# How AI systems find web pages, and how Dealectric gets found — research, 2026-10-18

Question: we can publish the best-structured product data on the web and still earn nothing, because no assistant finds us. What, from first principles, decides whether an AI finds and cites a page, and which channels does the community use today? Sources are listed at the end; vendor blogs are marked as such and primary sources were preferred where they exist.

## Summary

1. **An AI does not browse the web; it queries an index and reads text.** Every assistant answer that cites a page goes: question → several rewritten search queries → top results from a search index → fetch the page → read it as plain text (no JavaScript, CSS or images) → cite one or two passages. A page that is not in the index behind the assistant cannot be cited, however good it is.
2. **Dealectric is not in those indexes yet.** Checked today: Google has 3 of our 42 pages (home, privacy, agents). Bing, which ChatGPT and Copilot search, has 0. Brave, which Claude's search uses, has 0. Common Crawl (the base of most training sets) has no capture of the domain. Cloudflare shows the training crawlers (ClaudeBot 100 requests, Amazonbot 50, GPTBot 19) have been, but **the search crawlers that decide citations (OAI-SearchBot, Claude-SearchBot, PerplexityBot) have never visited.** Our 0/40 probe results are explained by this alone.
3. **Once a page is retrieved, four things decide whether it gets cited** (controlled study, 6 models, 252k trials): topical match to the query, a stated price, a recent timestamp, and being first in the retrieved list. Spec tables, evidence-backed claims and depth help next. Layout and formatting barely matter. We already do the specs; we need to make the question, the price and the date the first thing on each page, and keep the date fresh.
4. **The merchant channels are closed to us by design.** ChatGPT product feeds, Perplexity's Merchant Program, Google Merchant Center, Microsoft/Copilot and Amazon's Shop Direct all take feeds from the seller of record. Our brands are already in them through Shopify. Dealectric's only seat at that table is as the *cited source* an assistant reads while deciding, and as the source of *discount codes* an agent applies at checkout.
5. **What the community actually does** splits into plumbing (Bing Webmaster Tools + IndexNow, Search Console, robots.txt allowlists, schema.org), files with weak evidence (llms.txt, agents.json, NLWeb), paid placement (ChatGPT ads, Cloudflare pay-per-crawl), and the thing that correlates most with being cited: third-party mentions on Reddit, YouTube, niche blogs and comparison pages. Roughly three quarters of ChatGPT and Claude citations go to third-party "best X" pages, not brand sites. That is the slot Dealectric is built for.
6. **Order of work:** get indexed (Bing via IndexNow and URL Submission, Google via Search Console, Brave only via inbound links) → rebuild pages around single questions with answer, price and verified date up top → verified discount-code pages → give the dataset away to earn links and mentions → MCP server in the registry → measure weekly. The flywheel you described (get seen → see what agents do → improve) cannot start before step one.

## 1. First principles: how an AI consumes the web differently from a person

There are three distinct ways our page can reach a model, and they have different mechanics, lags and levers.

| Path | How our page gets in | Lag | What we control |
|---|---|---|---|
| **Training data** | Web crawls (Common Crawl, ClaudeBot, GPTBot, Amazonbot) are filtered and baked into the next model | Months to a year; new domains with few inbound links are crawled late or not at all | Allow the crawlers (done). Inbound links. Nothing else. |
| **Retrieval at answer time** | The assistant's search provider's index returns our URL for a rewritten query; the assistant fetches and reads the page | Days to weeks after the index has us; then real time | Being indexed by Bing / Google / Brave; the page's text; freshness; outside links that raise rank |
| **Agent action** | A browser agent (Comet, Claude in Chrome, ChatGPT Agent) or an API checkout (ACP, UCP) acts for the shopper | Real time | Whether the agent is sent to us (by search or by the user naming us); what the page says to do; discount codes |

Everything commercial for us today runs through the second path, so that is what the rest of this document is about. Points that differ from a human visitor:

**It queries, it does not browse.** A person types "best power station for a fridge" and reads three results. ChatGPT, Gemini and Claude rewrite the question into several narrower sub-queries ("query fan-out": Google's own term), run each against an index, and read the top results of each. Each sub-query retrieves its own sources, so a focused page can win one sub-question even when a broad "best power stations" page loses. Consequence: one page per real question beats one long guide.

**It reads the page as text, in one pass, under a token budget.** Fetchers (OpenAI's ChatGPT-User, Anthropic's Claude-User, Jina, Firecrawl) take the HTML, strip scripts, styles and images, convert it to Markdown and hand it to the model. No JavaScript runs. Our BLUETTI AC180 page is 5,548 bytes of HTML and 1,773 characters of text; the Jina conversion shows the price and buy link near the top, the spec table in the middle, and the "for AI assistants" notes near the bottom. That is already lean; the sites that lose here are JS-rendered stores. The one thing that goes wrong for us is order, see section 3.

**It cannot see facts that are only in markup.** The only controlled test found (searchVIU, 2025) put a price in JSON-LD only and no AI system extracted it. Google says structured data helps rank but is not required. So JSON-LD is for Google's rich results and for consistency; every fact must also be in the visible text.

**It weighs sources by a short list of signals, in order.** The best evidence is a 2026 arXiv study ("What Gets Cited", 252,000 trials across Gemini 2.5 Flash, GPT-5 nano/mini/5.2, Claude 3.5 Sonnet, Kimi K2) that put two candidate sources in a model's context and measured which one it cited first:

| Factor | Effect | Reading for us |
|---|---|---|
| On-topic for the query | Gatekeeper (odds ratio 221 to >10,000) | Page title and first lines must match the question as a shopper phrases it |
| Price stated | Gatekeeper (6 to >10,000) | Already present; move it into the first lines |
| Recent timestamp | Gatekeeper (14 to >10,000) | "Verified 2026-10-14" must stay recent and be visible; stale dates lose to pages with none |
| Listed first in retrieval | Gatekeeper (1,800 to >10,000) | Search rank still decides; this is why indexing and links come first |
| Query keywords present | Strong (6 to 40) | Use the shopper's words (fridge, CPAP, carry-on), not only ours (Wh, LFP) |
| Specifications, evidence-backed claims, deep coverage | Strong | Our spec tables and manufacturer-sourced figures are the right material |
| Confident vs hedged language | Strong but model-dependent | State what the data shows; put caveats after |
| Structured layout, headings | No reliable effect | Do not spend time on formatting |

**It does not click and it does not keep cookies.** Fetchers load a URL once. Affiliate tracking that depends on a redirect setting a cookie never fires inside the assistant. And ChatGPT only renders a URL as clickable if the page was actually loaded in the chat or the URL is already known from search; URLs the model writes itself are shown as plain text or cut to the host (our 10/17 probe: the Awin link became bare `awin1.com`). Claude as an agent passed the full link through. The reliable handoff is therefore our own product page, which the assistant did load, with the buy button on it.

**It is a tiny fraction of traffic but a large fraction of crawling.** Cloudflare's crawl-to-refer ratios for mid-2026 are in the hundreds to thousands of pages fetched per human visitor referred (OpenAI ~250:1, Anthropic ~1,900:1 in July 2026, versus Google ~5:1). Industry benchmarks put AI referrals at 0.1 to 2.8% of a site's traffic. The value for us is not the visit, it is the recommendation plus a working link or code.

## 2. The index behind each assistant, and where Dealectric stands today

| Assistant | Retrieval index | Crawler that decides citation eligibility | Our status, 2026-10-18 | 2026-10-28 |
|---|---|---|---|---|
| ChatGPT search / shopping | Bing plus OpenAI's own OAI-SearchBot and unnamed "third-party search providers" | OAI-SearchBot (must be allowed; is) | `site:dealectric.com` on Bing: **0 pages**. OAI-SearchBot: **never visited**. ChatGPT-User: 5 fetches (our own tests). GPTBot (training): 19 requests | Bing: home page only. **OAI-SearchBot: crawling since 10-21**, 182 verified requests over 53 of 75 sitemap URLs and 41 `/go/` links |
| Claude (web search) | Brave Search (Brave is on Anthropic's subprocessor list; 80 to 88% of Claude's cited URLs are in Brave's top 10 per two vendor measurements) | Claude-SearchBot | Brave: **0 pages**. Claude-SearchBot: **never visited**. ClaudeBot (training): 100 requests, our most frequent bot | Brave: **0 pages** (10-27). Claude-SearchBot: **never visited**; all 296 requests with its UA are unverified scanners |
| Gemini / Google AI Mode / AI Overviews | Google's index; Google says no extra requirements beyond being indexed with a snippet | Googlebot | Google: **3 of 42 pages** indexed (home, /privacy, /agents). Googlebot: 25+ requests. Sitemap read 10/14 | Google: **46 pages** indexed (10-27). Googlebot 199 and Google-InspectionTool 177 verified requests since 10-21 |
| Microsoft Copilot | Bing | Bingbot | 7 Bingbot requests; 0 pages indexed | Bing: home page only; 'Discovered but not crawled' elsewhere, 0 backlinks. Verified Bingbot 28 requests 10-20 to 10-28, no product page |
| Perplexity | Own index (plus merchant feeds and Shopify) | PerplexityBot | **Never visited** | PerplexityBot: **never visited**; all 273 requests with its UA are unverified scanners |
| Amazon Alexa for Shopping | Amazon catalog plus Shop Direct merchant feeds; Amazonbot crawls the web | Amazonbot | 50 requests. No path for a non-merchant | Amazonbot 125 verified requests since 10-21 |
| Training sets generally | Common Crawl monthly crawls, filtered | CCBot | **No captures** of dealectric.com in the Aug and Sep 2026 crawls | not re-checked |

The Cloudflare figures are verified-bot requests since 2026-10-10 (2026-10-28 column: since 10-14 or 10-21 as stated; a bot's name in the UA alone is not counted, since scanners borrow it) (`tools/cf.py`, `verifiedBotCategory`). Checks of Bing and Brave used `site:dealectric.com` in the browser; both returned unrelated results or "too few matches", which is what they show for a domain with no indexed pages. The Google check returned exactly three dealectric.com results.

Conclusion: we are invisible by construction, not by quality. Four days after sitemap submission, no assistant's search provider has our product pages. Nothing else in this document matters until that changes.

How each index can be entered:

- **Bing** (ChatGPT, Copilot): Bing Webmaster Tools is already verified. Two levers exist that we have not used: URL Submission (10,000 URLs per day per root domain, submitted from the dashboard) and IndexNow (host a `{key}.txt` at the site root, then POST up to 10,000 URLs per request to `api.indexnow.org/indexnow`; Bing and Yandex share it). Vendor claims of "minutes" are marketing, but it is the only push mechanism Bing offers and it costs nothing. Bing's "AI Performance" report (public preview) will show Copilot and Bing-AI citations and the grounding phrases used, which is the only first-party citation data available to a site owner anywhere.
- **Google** (Gemini, AI Mode): Search Console has the sitemap; 3 pages indexed means Google is crawling slowly, as it does for a new domain. URL Inspection → Request Indexing on the 42 URLs is the manual push. Google's AI features need nothing beyond normal indexing, and Google-Extended controls training, not search.
- **Brave** (Claude): there is no webmaster tool and no submission form. Brave indexes pages that opted-in Brave browser users visit (Web Discovery Project) and pages linked from pages it already has. The only levers are inbound links and Brave users visiting our pages; a community report says having friends browse the site did not work on its own. This makes outside links the Claude lever, period.
- **Perplexity**: no documented submission; PerplexityBot crawls the open web; being in Bing and Google and having links is the route.

## 3. What the difference changes about the site

**A. Build for the sub-query, not the topic.** Each real shopper question (the 30 in `target-questions.md`) wants its own URL whose title is the question in the shopper's words, whose first 300 characters answer it with a number, a price and a verified date, and whose body is the table and the evidence. The guide pages stay as hubs that link to these. This is DLC-24, with the gatekeepers from the study added as the acceptance test.

**B. Price and date in the first lines of every page, visibly.** Our product pages have both, but after the breadcrumb, title and summary. Move "Verified price $499 at BLUETTI, checked 2026-10-14" into the first paragraph, put `dateModified` in the JSON-LD, and make the weekly re-verification (DLC-9) bump the visible date on every page it touches. A page with a stale date loses to a page with no date, so the weekly cadence is a hard requirement, not a nice-to-have.

**C. Be the primary source others quote.** The 10/17 probes show who gets cited for our questions: brand blogs (Anker, BLUETTI, Pecron), small niche sites (Solar Power Auditor, ExploringOffgrid, Tested Watts, GeekBitz, TechWise, powerstations.reviews), and for audio the big labs (RTINGS, SoundGuys). Normalized runtime, recharge and sizing data in a reusable form (CSV on GitHub and Hugging Face, with a citation line) gives those sites a reason to link to us, and inbound links are the only lever that works on all four indexes at once.

**D. Hand the shopper a link that survives.** The product page is the handoff (DLC-10 notes). Offer the discount code as a first-class, visible field, because codes work on every route: in the chat, in a browser agent, and in ACP/UCP checkout where `discounts.codes` is the one field an agent fills that can carry our attribution (DLC-29, DLC-30).

**E. Keep the agent instructions, but do not rely on them.** Claude as an agent read `llms.txt` and the page notes and followed them; ChatGPT ignored them. They cost nothing and help the agents that read them. They do not help discovery.

**F. Things that do not matter for discovery, so skip them:** `llms.txt` as a ranking signal (0.1% of AI bot requests target it; Google says it does not use it; no provider has confirmed reading it in production), facts that live only in JSON-LD, layout polish, Cloudflare "Markdown for Agents" (needs a Pro plan at about $20 to $25 a month and our pages are already small), agents.json / ai.txt / NLWeb (competing drafts with no consumer that matters), and a Wikidata or Wikipedia entry (a new affiliate site will not pass notability).

## 4. The channels the community uses today, rated for Dealectric

| Channel | Who runs it | What it does | Open to us? | Verdict |
|---|---|---|---|---|
| Bing Webmaster Tools + URL Submission + IndexNow | Microsoft | Gets pages into the index ChatGPT and Copilot search | Yes, verified already | **Do now** (DLC-31) |
| Google Search Console, Request Indexing | Google | Google index → Gemini, AI Mode, AI Overviews | Yes, verified already | **Do now** (DLC-13) |
| Brave index | Brave | What Claude's search retrieves | No submission path | Only via links and Brave users (new DLC-36) |
| robots.txt allowlist for AI bots | Site owner | Eligibility for OAI-SearchBot, Claude-SearchBot, PerplexityBot | Done | Keep; verify after any Cloudflare rule change |
| schema.org Product / Offer JSON-LD | Site owner | Google rich results and ranking help; unproven for others | Done | Keep; mirror every fact in visible text |
| llms.txt / llms-full.txt | Convention (Answer.AI) | Site summary for agents that read it | Done | Keep; zero discovery value |
| Merchant product feeds: ChatGPT (ACP, approved partners via chatgpt.com/merchants), Perplexity Merchant Program, Google Merchant Center, Microsoft Merchant Center / Copilot Checkout, Amazon Shop Direct, Shopify Catalog | OpenAI, Perplexity, Google, Microsoft, Amazon, Shopify | Puts a seller's catalog into the assistant's shopping cards and checkout | **No.** All take the seller of record; Google bars affiliate links outright (its affiliate beta closed in 2021). Our brands are already in via Shopify | Not a channel for us; our role is the cited source and the code |
| ChatGPT ads (self-serve Ads Manager, CPC bidding since May 2026) | OpenAI | Sponsored cards under answers for US Free/Go users | Technically yes; reported minimums have ranged from $50k down to "none", conflicting | Not now; revisit when a page converts |
| Third-party mentions: Reddit, YouTube, niche blogs, comparison pages | Communities | Reddit is the most-cited domain on Perplexity (up to ~47% of top citations in one study) and top three on ChatGPT; 75 to 81% of ChatGPT and Claude citations are third-party best-of pages | Yes, slowly | **Main lever** (DLC-26). Barry answers threads where our table is the answer; we publish data others cite. No astroturfing: Reddit and Wikipedia both police it |
| MCP registry (registry.modelcontextprotocol.io) and directories (Glama, Smithery, PulseMCP, mcp.so) | MCP project, independents | Lists tools agent builders can install; official registry is free, no review, and seeds the others | Yes, once we have a server | **Do** (DLC-27); small audience but it is the one channel where an agent calls us directly |
| Agent-readiness files: agents.json, A2A agent card, NLWeb, .well-known/api-catalog | Competing drafts | Describe an endpoint to agents | Yes | Skip until one has a consumer; MCP covers the need |
| Cloudflare AI Crawl Control, Markdown for Agents, Pay Per Crawl, Content Signals | Cloudflare | Monitor bots; serve Markdown (Pro+); charge crawlers; robots.txt policy | Have the first; the rest are either paid or the opposite of our goal | Keep monitoring; leave Content Signals at the default (all yes) |
| GEO monitoring vendors (Profound, Peec, Otterly, SE Ranking) | Vendors | Track citations across assistants | Yes, paid | Not needed; our probe harness (DLC-12, DLC-34) does this |
| Shopping-specific: Perplexity Merchant Program, PayPal / Shopify store sync | Perplexity | Live product data into Perplexity cards | Sellers only | Same as above |

Two facts from the merchant side are worth holding on to. OpenAI's help center says merchants are ranked by "availability, price, quality, and whether they are the maker or primary seller", and that product cards draw on "structured metadata from first-party and third-party providers … and other third-party content". The brand store will always outrank us as a merchant; the "other third-party content" is where a cited buying guide lives. And OpenAI's Shopping Research (the buyer's-guide mode, GPT-5 mini tuned for shopping) "reads trusted sources and cites them" from the open web, which is exactly a retrieval path.

## 5. Recommended order of work

1. **Get into Bing and Google this week** (DLC-31, DLC-13). Add the IndexNow key file to the build, POST all 42 URLs, submit them in Bing URL Submission, request indexing in Search Console for every page, then check `site:dealectric.com` on Bing, Google and Brave weekly and record the counts. Done when the product pages show on Bing and Google.
2. **Rebuild the content around questions and gatekeepers** (DLC-24, DLC-32). One URL per target question; title in the shopper's words; answer, price and verified date in the first lines; spec table; manufacturer evidence links; `dateModified`. Acceptance test: paste the page's text into a model with a competing page and see which it cites.
3. **Codes as a product** (DLC-29, DLC-30). The one earning path that survives every route.
4. **Earn the links that move all four indexes** (DLC-26). Publish the dataset (CSV + README with a citation line) on GitHub and Hugging Face; a Show HN about "a product database built to be read by agents"; Barry answers 3 to 5 Reddit threads a week where a table answers the question, with the link only where it genuinely helps; email the niche blogs the probes show being cited and offer the data.
5. **Ship the MCP server and list it** (DLC-27).
6. **Measure** (DLC-28, DLC-34): index counts per engine, Bing AI Performance citations, GSC impressions, Cloudflare bot requests by user agent (especially the first OAI-SearchBot and Claude-SearchBot hits), `utm_source=chatgpt.com` visits, the weekly probe score.

Expect a slow curve. New domains take weeks to index on Bing and Google; Brave and training data follow links; vendor data says citation share compounds over three to six months. The signal to watch first is not sales, it is the first visit from a search crawler and the first `site:` result on Bing.

## Sources

Primary and official
- OpenAI crawlers: https://developers.openai.com/api/docs/bots ("Sites that are opted out of OAI-SearchBot will not be shown in ChatGPT search answers")
- OpenAI, Shopping with ChatGPT Search: https://help.openai.com/en/articles/11128490 (merchant ranking factors; third-party content; Shopify Catalog; feed application)
- OpenAI commerce docs and product feed spec: https://developers.openai.com/commerce ("available to approved partners")
- Anthropic crawlers (ClaudeBot, Claude-User, Claude-SearchBot): https://support.claude.com/en/articles/8896518
- Google, AI features and your website: https://developers.google.com/search/docs/appearance/ai-features ("There are no additional requirements"; no special files or markup)
- Google Merchant Center onboarding (affiliate links barred): https://support.google.com/merchants/answer/6363310 ; affiliate beta closed 2021: https://support.google.com/merchants/answer/2811972
- Google UCP: https://developers.google.com/merchant/ucp ; Merchant Center UCP hub: https://support.google.com/merchants/answer/16992327
- Perplexity shopping launch and Merchant Program: https://www.perplexity.ai/hub/blog/shop-like-a-pro
- Microsoft agentic commerce / Copilot Checkout: https://about.ads.microsoft.com/en/solutions/technology/agentic-commerce
- IndexNow documentation: https://www.indexnow.org/documentation
- Brave Web Discovery Project: https://support.brave.app/hc/articles/4409406835469 ; community answer on indexing: https://community.brave.com/t/how-can-i-index-my-website-on-brave-search-engine/557611
- Cloudflare Markdown for Agents: https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents ; AI Crawl Control: https://developers.cloudflare.com/ai-crawl-control/ ; pay-per-use press release: https://www.cloudflare.com/press/press-releases/2026/cloudflare-allows-the-agentic-internet-to-flourish-with-a-simple-philosophy-your-content-your-rules/
- MCP Registry: https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/
- Common Crawl index API (no captures for dealectric.com, CC-MAIN-2026-34 and -39): https://index.commoncrawl.org/
- Amazon Alexa for Shopping / Shop Direct: https://www.digitalcommerce360.com/2026/05/13/amazon-launches-ai-agent-alexa-for-shopping/

Research
- Vishwakarma, "What Gets Cited: Competitive GEO in AI Answer Engines" (2026): https://arxiv.org/abs/2605.25517 (18 factors, 6 models, 252k trials)
- GEO survey 2023–2026: https://arxiv.org/pdf/2607.14035
- searchVIU, schema markup test (JSON-LD-only price not extracted): https://www.searchviu.com/en/schema-markup-and-ai-in-2025-what-chatgpt-claude-perplexity-gemini-really-see/
- Semrush, most-cited domains (230k prompts, 13 weeks): https://www.semrush.com/blog/most-cited-domains-ai/
- HUMAN Security, State of Agentic Traffic (monthly): https://www.humansecurity.com/learn/blog/state-of-agentic-traffic-august-2026-agentic-traffic-grows-27-reaches-new-high-as-codex-debuts-strongly/

Vendor and secondary (treat numbers as directional)
- llms.txt evidence: https://www.semrush.com/blog/llms-txt/ ; https://www.1clickreport.com/blog/llms-txt-evidence-2026 ; https://digitortoise.com/llms-txt-explained/
- Claude search on Brave: https://completeseo.com/claude-web-search-runs-on-brave/ ; https://www.tryprofound.com/blog/what-is-claude-web-search-explained
- ChatGPT search pipeline: https://searchengineland.com/chatgpt-citations-change-hidden-search-pipelines-481843 ; https://dejanmarketing.com/?p=23783
- Query fan-out: https://www.rankability.com/blog/query-fan-out/ ; https://blog.google/products-and-platforms/products/search/ai-mode-search/
- Third-party citation share and affiliate sites: https://rexultz.com/blog/ai-overviews-affiliate-sites-2026-data/ ; https://prvnmedia.com/blogs/news/ai-search-affiliate-content-citations-2026 ; https://www.geoptimizer.io/blog/get-cited-by-ai-2026-evidence
- Reddit citation share: https://quickseo.ai/blog/how-reddit-affects-ai-visibility-2026 ; https://www.getpassionfruit.com/blog/reddit-ai-citation-source-chatgpt-perplexity
- Brand mentions vs visibility: https://news.designrush.com/30m-sources-show-reddit-youtube-lead-ai-search-visibility ; https://victorious.com/quarterly-search-report
- Crawl-to-refer ratios: https://ecorpit.com/ai-crawler-crawl-to-referral-ratio-2026-geo-decision/ ; https://ppc.land/crawl-to-referral-ratio/
- AI referral share of traffic: https://seranking.com/blog/ai-traffic-research-study/ ; https://searchsignal.online/research/ai-search-referrals-citations-2026
- ChatGPT product feeds and Instant Checkout pivot: https://www.lengow.com/get-to-know-more/chatgpt-product-feed ; https://stellagent.ai/insights/chatgpt-shopping-feature-deep-dive
- ChatGPT ads: https://openai.com/index/new-ways-to-buy-chatgpt-ads ; https://www.thrad.ai/content/how-to-advertise-on-chatgpt-the-honest-2026-answer
- Bing Webmaster AI Performance report: https://previsible.io/seo-ai-news/bing-ai-performance-report/ ; https://eseospace.com/blog/bing-webmaster-tools-indexnow-ai-search/
- Agent-readiness standards compared: https://ai-agent-discovery.com/en/standards.html ; https://agentswelcome.dev/protocols
- MCP directories: https://linklyhq.com/blog/mcp-server-directories
- Web-to-Markdown fetchers: https://jina.ai/reader/
