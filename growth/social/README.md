# Official accounts: kit and pre-launch checklist (DLC-185, DLC-186)

Barry, 2026-11-06: "create official accounts for dealectric." Claude can't create accounts, so Barry signs up
(DLC-185). This is everything else. Videos for the channel: `growth/video/` (DLC-187).

## Handles (checked 2026-11-06, logged out)

| Platform | Handle | Status |
|---|---|---|
| YouTube | **@dealectricdeals** | `@Dealectric` is taken (an unrelated channel, joined 2010, 28.6k views). Free: @dealectricdeals, @dealectric_com, @dealectricHQ, @getdealectric |
| X | @dealectric | x.com/dealectric returns 404, so it looks free |
| Pinterest | dealectric | Can't check logged out; try it at sign-up |

Skipped: TikTok and Instagram (links in posts can't be clicked; little AI-citation value). Reddit: an official
Dealectric account since 2026-11-06 (Barry reversed the earlier skip); rules in growth/outreach/reddit-brand-account.md.

## Profile text

**Name** on every platform: Dealectric

**YouTube channel description**
> Dealectric compares portable power stations, solar generator kits and chargers on the numbers that decide them:
> battery, inverter, solar input, and what they actually run. Specs come from each maker's official US store. At
> dealectric.com, prices are re-checked and discount codes are tested in each brand's cart every day. Narration is an
> AI voice; the data and slides are ours. Dealectric earns a commission when you buy through its links, at no cost to you.

**Channel links** (Customization → Basic info → Links):
`https://dealectric.com/?utm_source=youtube&utm_campaign=channel` (title: dealectric.com)

**X bio** (145 characters)
> Power stations, solar kits and chargers compared on the numbers. Discount codes tested daily in each brand's cart.
> We earn a commission on links.

X website: `https://dealectric.com/?utm_source=x`

**Pinterest about**: same as the YouTube description, first two sentences. Website: `https://dealectric.com/?utm_source=pinterest`
(claim the domain in Pinterest; it gives a meta tag or a DNS TXT record, and Claude can add the TXT through Cloudflare).

**Images** (`python3.12 growth/social/brand_assets.py`): `assets/avatar.png` (800×800), `assets/youtube-banner.png`
(2560×1440, text inside the safe area), `assets/x-header.png` (1500×500).

Every outbound link carries `utm_source=<platform>`, so the Worker logs the landing (D1 `landings`) and any `/go/`
click (D1 `clicks.utm_source`) with no Worker change.

## Before the first upload (from the 2026-11-06 terms check)

Barry's (account settings):
1. **YouTube: turn on advanced features** (phone or ID verification). Without it, long-form description links are not
   clickable and Shorts can't have a Related Video link ([YouTube Help](https://support.google.com/youtube/answer/14075157)).
2. **CJ: add the channel as a Social promotional property.** CJ's API has a social property type; account info must list
   the sites in use. Ask Claude afterwards to check whether ALLPOWERS links need that property's ID.
3. **Awin: add the channel as a promotional space**, and tell BLUETTI's program manager. Awin's Code of Conduct says
   activity outside registered spaces must be disclosed "to the advertiser".
4. **Amazon Associates: add the channel URL in Associates Central** ("You must identify your Site(s)"). Amazon links in
   descriptions go straight to amazon.com with the tag, never through `/go/`: a redirect disqualifies the purchase. No
   Amazon prices in videos.
5. Read the ALLPOWERS (CJ) and BLUETTI (Awin) program terms in the dashboards for any social or video limits. Neither
   publishes one; ALLPOWERS bars "unauthorized coupons", and our codes are network-issued.

Already built into every video (`growth/video/render.py`):
- Spoken and on-screen commission disclosure in the first scene, and a commission line above the description links.
  The FTC says the disclosure belongs "in the video and not just in the description".
- No AI "altered or synthetic" label: YouTube requires it for realistic depictions of people, places or events. Our
  reading is that an AI narrator over our own charts is not one; the description still says the voice is AI.
- Each video stands on its own: tables, worked numbers, caveats. That's because YouTube's spam policy bars content
  "created solely to drive users off of YouTube" and AI used "to churn out high volumes of similar content".

Sources: [FTC influencer guide](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers),
[Amazon Associates policies](https://affiliate-program.amazon.com/help/operating/policies),
[Awin promotional spaces](https://success.awin.com/articles/en_US/Knowledge/How-do-I-add-or-edit-my-promotional-sites),
[YouTube altered content](https://support.google.com/youtube/answer/14328491),
[YouTube spam policy](https://support.google.com/youtube/answer/2801973),
[Shorts links](https://support.google.com/youtube/answer/13748639).
