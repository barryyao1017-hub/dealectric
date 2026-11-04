# Promote, tier 3: instruction set for the 2026-11-03 comparison pages (seven pages, step 7b)

Source: the seven research files in this folder (`outreach-vatrer-golf-cart.md`, `outreach-fopo-s788.md`, `outreach-blink-outdoor-4-solar.md`, `outreach-dxp2800-immich-docker.md`, `outreach-dxp480t-all-nvme.md`, `outreach-usb-switch.md`, `outreach-fridge-power-station.md`). Same rules as `growth/focus/fastloop-runs/rv-2kwh/promote-tier3-instructions.md` ("Rules for whoever runs this"): agent's Chrome on 9222 only, never the final click, never create an account (not through agent-vault `register` either), never type credentials, paste exactly, re-read the thread's last posts first, one screenshot per filled form, footprint logging. Nothing in this document has been posted; Barry reviews each task and clicks Submit himself.

## Header

- **21 tasks** across 7 pages: 15 live threads (tier A or B, demand 2–3) in section A, 6 evergreen or correction items (at most two per page) in section B. Section A is ordered by demand, then freshness; section B by demand, then freshness.
- **Accounts.** agent-vault holds logins for diysolarforum.com, forestriverforums.com, irv2.com, macrumors.com, tacomaworld.com and google.com only. 4 tasks use a vault login (MacRumors: T4, T19, T20; diysolarforum: T2). 1 task needs no account (T16, a blog comment form). **16 tasks need an account Barry has to create first**, on 7 venues: Level1Techs (T1, T5, T8, T11, T13, T15), Cartaholics (T3, T7), Slickdeals (T6, T10), Home Assistant community (T9), Amazon's Blink forum (T12, T14), Quora (T17, T18), Best Buy (T21). Claude never creates accounts; the executing subagent opens the sign-up page and leaves it.
- **Venues whose rules put the link at risk** (every text still ends with the page URL and the disclosure, per Barry's 11-01 rule; the task flags the risk and Barry decides):
  - diysolarforum.com: Code of Conduct, "Affiliate links, self-promotion, spam etc, will result in a permanent ban" (T2).
  - Slickdeals: forum rule 1 "Spam, self promotion and referral links are not allowed"; Acceptable Use Policy §10 (no promoting your own business or referral links), §6, §11 (T6, T10).
  - Home Assistant community: ToS §2 bans "unwanted commercial content designed to drive traffic to third party sites" (T9).
  - Amazon's Blink forum: guidelines bar promotional posts and external commercial links; staff-moderated (T12, T14).
  - Best Buy Q&A: promotional content and external links barred; answers with URLs are typically removed (T21).
  - MacRumors: a new account's self-link is treated as advertising; established members may link their own site when it answers a specific question (T4, T19, T20).
  - Level1Techs: FAQ "Don't post spam"; ToS §2 on commercial content; the forum's owner sells KVMs, so T11 may read as competitive. No affiliate rule found.
  - Cartaholics: no written affiliate rule, terms ban "spam or spam-like" content; Eco Battery sponsors the forum; new-member link limits unknown (T3, T7).
  - Quora: direct or cloaked affiliate URLs are treated as spam; a relevant link to your own site with the affiliation disclosed in the body is tolerated; mostly-promotional answers get collapsed (T17, T18).
  - AVForums rule 8 (anyone affiliated with a commercial enterprise must not reference it) is why the one AVForums item is not in this set.
- **Blink pages:** the Blink Outdoor 4 page was corrected today (commit 4dbceda) to list Blink Solaris as the official clip-on option, so the precondition the Blink research set ("fix the page first, then post") is met for T12, T14, T16 and T21.
- **Side finding (not a task):** FOPO's S788 store page was edited on 11-03 and a fetch summary read "Sold out" with the prices inverted; the product JSON said in stock at $499.99. Worth a glance at the next daily sweep.

### Reddit manual-check list (blocked for every tool; Barry checks by hand)

Run each on reddit.com (or old.reddit.com), **sort New, past month**; direct form `https://www.reddit.com/r/<sub>/search/?q=<query>&sort=new&t=month&restrict_sr=1`. Read each subreddit's self-promotion rule first: r/UgreenNASync and r/DataHoarder remove undisclosed affiliate links, r/photography bans self-promotion outside its weekly threads (rules unverified today).

| Subreddit | Exact searches | Page |
|---|---|---|
| r/golfcarts (and r/ClubCar if it exists) | `Club Car lithium` · `48V lithium kit charger` · `Vatrer` · `LiTime golf cart` · `OBC bypass lithium` · `Precedent lithium conversion` | golf-cart kit |
| r/macbookpro | `screen extender` · `triple monitor` | FOPO S788 |
| r/mac | `laptop screen extender displaylink` · `KVM` · `USB switch` | FOPO S788; USB switch |
| r/digitalnomad | `screen extender` · `portable triple monitor` | FOPO S788 |
| r/remotework, r/WorkFromHome | `screen extender` · `KVM work laptop` (WorkFromHome) | FOPO S788; USB switch |
| r/ultrawidemasterrace | `laptop extender` | FOPO S788 |
| r/Monitors, r/buildapcmonitors | `laptop screen extender 1200p` · `16:10 portable` · `built-in KVM mac` (Monitors) · `KVM 4K 144hz mac` (Monitors) | FOPO S788; USB switch |
| r/Daytrading | `laptop screen extender` | FOPO S788 |
| r/thinkpad, r/Dell, r/GamingLaptops | `screen extender 16 inch` · `18 inch` | FOPO S788 |
| r/blinkcameras | `Solaris` · `Outdoor 4 solar` | Blink |
| r/homesecurity, r/smarthome | `Blink Outdoor 4 solar` | Blink |
| r/immich | `NAS` · `which NAS` · `UGREEN` | DXP2800 |
| r/selfhosted | `NAS Immich under 500` · `replace Google Photos NAS` · `DXP2800` | DXP2800 |
| r/homelab | `first NAS Immich` · `N100 NAS Immich` · `flashstor OR "F8 SSD" OR DXP480T` · open https://www.reddit.com/comments/1tciqfi (Nov 2025 "no KVM required" post; HawkingRadiator512's USB-C + USB-A host question) | DXP2800; DXP480T; USB switch |
| r/synology | `Immich DS225+` · `DS223j Immich` | DXP2800 |
| r/UgreenNASync | `Immich` · `Home Assistant VM` · `DH4300 Docker` · `DXP480T` · `thunderbolt mac` | DXP2800; DXP480T |
| r/DataHoarder | `NAS under 500 Docker` · `"all flash" NAS` · `NVMe NAS 10GbE` | DXP2800; DXP480T |
| r/homeassistant | `NAS Home Assistant OS VM UGREEN` · `Immich NAS` | DXP2800 |
| r/HomeServer, r/HomeNAS | `Immich NAS budget` (HomeServer) · `flashstor OR "F8 SSD" OR DXP480T` (HomeNAS) | DXP2800; DXP480T |
| r/editors | `NAS thunderbolt` · `shared storage mac` | DXP480T |
| r/videography | `NAS SSD` · `thunderbolt NAS` | DXP480T |
| r/photography | `NAS silent` OR `SSD NAS` | DXP480T |
| r/macmini, r/MacStudio | `NAS thunderbolt` · `KVM` (macmini) · `USB switch` (macmini) | DXP480T; USB switch |
| r/battlestations | `USB switch` · `KVM mac pc` | USB switch |
| r/macsetups | `KVM` · `USB switch` · `windows pc same monitor` | USB switch |
| r/sysadmin | `USB switch work laptop personal` · `KVM home office` | USB switch |
| r/buildapc | `share keyboard mouse laptop desktop` · `USB switch 10Gbps` | USB switch |
| r/homeoffice | `KVM work laptop` | USB switch |
| r/preppers | `power station fridge` · `battery backup refrigerator` | fridge |
| r/HomeImprovement | `power station refrigerator outage` | fridge |
| r/solar | `power station fridge` (the Dec 2025 "$600 battery station" thread will show; look for newer) | fridge |
| r/Bluetti | `fridge` · `Elite 200 V2 refrigerator` | fridge |
| r/Jackery, r/Ecoflow | `fridge outage` | fridge |
| r/SolarDIY, r/homeowners | `power station outage fridge` | fridge |

Google fallbacks when Reddit's search is poor (Tools → Past month): `site:reddit.com "triple screen laptop extender" 16 inch 2026` · `site:reddit.com "screen extender" "M3" three displays` · `site:reddit.com "1920x1200" "laptop extender"` · `site:reddit.com "power station" fridge outage`.

Other venues the tools could not read, if Barry has time (in the Pane): buggiesgonewild.com threads t=189616 and t=188462 plus its Electric Club Car subforum; golfcartsforum.com › Club Car Electric; ask.nascompares.com threads tid 11836, 12015, 12611, 12757 and "Latest threads"; a signed-in MacRumors search for "extender" sorted by date; Amazon's Blink forum sorted by latest (`Outdoor 4 solar`, `Solaris`); BLUETTI's community thread 39174 (Elite 100 V2 fridge surge).

## Not in this set

- **AVForums DXP480T Plus review discussion (draft 2 in the DXP480T file):** 9 months stale and rule 8 bars any reference to our site; the research recommends skip.
- **Quora "What size portable power station do I need to run a refrigerator…" (fridge draft 2d):** left out only by the two-evergreen-items-per-page cap (the two Quora questions with demand 3 are in). It is the freshest of the three (an answer 28 days ago) and the closest match to the target query; if Barry would rather swap it for T17 or T18, the text is in `outreach-fridge-power-station.md` §2.2d.
- **Amazon forum "Blink Outdoor 4 camera question" (Blink row 3):** the research gave no draft, only "adapt draft B's first paragraph"; nothing exact to paste.
- **DisplayNinja built-in-KVM article (USB switch row 10):** optional suggestion comment, no draft.
- **PowerOutage.us fridge article (fridge row 6):** errors found, but no comment section, no author contact, and not verified on page 1.
- Everything the research itself marked skip, stale or already answered (Cartaholics rows 3–4, the DH4300 buyer thread for the all-NVMe page, the MacRumors newbie NAS thread, Slickdeals rows 4–9, the Studio Display and M6 mini threads, the Firewood Hoarders and r/solar threads, and the rest of each file's "checked and rejected" table).

---

# Section A. Live threads (tier A or B), by demand then freshness

## Execution state (2026-11-03, 18:10 PT)

- **Filled, not posted (13 tasks):** MacRumors T4, T19, T20; diysolarforum T2; Home Assistant community T9; Level1Techs T1, T5, T8, T11, T13, T15; Amazon's Blink forum T12, T14 (signed in through Amazon with Barry's consent, display name barrryyao, guidelines agreed on Barry's yes; the editor is a Lightning rich-text box in a closed shadow root, filled by a real mouse click plus typed input; the Answer/Post button is untouched). Each sits in its reply editor in the Agent Chrome (localhost:9222) with the Post/Reply button untouched; Level1Techs' composer was switched from rich text to markdown so the `**` markup posts as bold. Screenshots in `screenshots/` (`<task>-<venue>.png`). Barry reads each, edits, and clicks Post himself. T2's link risks a diysolarforum ban; T19/T20 only if on page 1; T11 may read as competitive on Level1Techs (the forum sells KVMs).
- **Cartaholics T3, T7: blocked.** The new barrryyao account is "awaiting approval by an administrator", so the forum shows no reply editor. Once approved, run `paste.py` on the two threads (XenForo).
- **Still no account:** Slickdeals (T6, T10), Quora (T17, T18), Best Buy (T21). T16 is a blog comment form (no account; not filled, since the form posts on submit and Barry wanted to review first).
- The vault's approval dialog had to be fixed first (Tk drew no window on macOS; native dialog now, agent-vault commit 7d0ce02). On the corporate network the vault's `bw` cannot reach Bitwarden without the proxy.

## T1. Reply on Level1Techs, "Homelab and/or NAS entry point advice request" (demand 3, posts 11-02 to 11-03)

- **Where:** https://forum.level1techs.com/t/homelab-and-or-nas-entry-point-advice-request/259960 (11 posts at research time; reply after the last)
- **Account:** none in the vault; Barry creates one at https://forum.level1techs.com/signup (Claude never creates accounts). A new Discourse account is limited to about two links per post (not verified for this site); the text has one.
- **Steps:** Open the thread, read every post after #11 (the thread moved the same day). If someone has already said the DH4300/DH4800 are ARM or priced a sub-$500 x86 box, report instead of pasting. Otherwise click Reply at the bottom, paste the text (Discourse renders the Markdown bold), do not click 'Reply'.
- **Rules:** Level1Techs FAQ "Don't post spam"; ToS §2 on commercial content. No affiliate rule found.
- **Notes for Barry (from the research):** verified today: DH4300 Plus CPU/RAM and $399.99, DXP2800 $389.99 (UGREEN US store), ODM RAM table (docs.opendronemap.org). Not on our page: that the DH4300 Plus lacks Docker or VMs (UGREEN's page is silent), so the text argues only from ARM, which holds regardless. "DXP4800 Plus ... over $500" rests on Slickdeals listings ($534 Mar 2026, $559.99), not UGREEN's store today.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Two things nobody's said yet, because they decide between the two paths you're weighing.

**1. The DH4300 Plus and DH4800 are ARM boxes (8-core A76+A55, 8 GB LPDDR4X).** That's fine for "a Google Drive replacement for the family" over SMB and a Tailscale VPN. It bites on your other two goals: Docker on ARM runs only arm64 images, so a chunk of the self-hosted catalogue (and anything you'd want to try "to learn") either has no image or runs under emulation, and there are no x86 VMs for a Linux sandbox. aar.l1t's "amd64 over arm64" point is this, concretely. UGREEN's Intel line gives you both: the 2-bay DXP2800 is an N100 with 8 GB DDR5 (one SO-DIMM slot, 16 GB max), two M.2 slots, 2.5GbE, Docker with Compose projects plus a VM app in UGOS, about 5 W idle, two-year warranty, $389.99 diskless on UGREEN's US store today. The DH4300 Plus is $399.99 on the same store today, so right now the ARM box costs *more* than the x86 one. The 4-bay DXP4800 Plus Agent9 runs is the same idea with two more bays and 10GbE; it's over $500.

**2. OpenDroneMap does not belong on any NAS you'd buy at this price.** ODM's own docs: 4 GB RAM minimum for ~40 images, 16 GB recommended, 64 GB at 1,500 images, 256 GB at 5,000. Run it on your desktop (or a used OptiPlex as jdrch says), keep the datasets on the NAS over 2.5GbE. That also answers "prebuilt vs custom": the NAS only has to be a reliable disk box with Docker; the heavy compute goes elsewhere.

For your dad's photos, the thing you'll end up running is Immich (self-hosted Google Photos: phone backup, face search). It wants 6 GB RAM minimum, 8 GB recommended, and an x86-64 CPU for its machine-learning container (you can turn ML off or run it on another machine). On the DXP2800 put the Docker pool on an M.2 SSD so Immich's database and thumbnails aren't on spinning disks; if you also want Home Assistant OS as a VM later, it takes 2 GB more, so plan the 16 GB SO-DIMM. 2 bays vs 4: two 8–12 TB drives in a mirror hold a lot of RAW; the 4-bay only matters if drone mapping datasets grow past that. Drives will cost as much as the box in 2026, as Glitch001 said; xyz's Duplicacy-to-B2 advice is the other half of the setup.

Caveat on UGREEN generally: UGOS is a locked-down Debian (no apt), and the brand's stance on third-party OSes (people run TrueNAS or Unraid on DXP units, see the Unraid forum plugins) isn't official. If you want to learn Linux properly, an N100 mini PC with Proxmox teaches more for less, but you have data to protect, so I'd take the appliance for the family's copy and learn on the OptiPlex.

I wrote up the under-$500 comparison (DXP2800 vs Synology DS225+, TerraMaster F2-425 Plus, Asustor, QNAP, the ARM DH2300 and the Beelink ME mini) here: https://dealectric.com/best-nas-under-500-for-docker-immich-home-assistant
I run dealectric.com, which earns a commission on some links.
```

## T2. Reply on diysolarforum, "Advice please for a small power cut setup." (demand 3, Spain, opened and last post 11-03)

- **Where:** https://diysolarforum.com/threads/advice-please-for-a-small-power-cut-setup.132150/
- **Account:** diysolarforum.com login in agent-vault (`list_accounts`, then `login`).
- **Steps:** Open the thread, read every post after Hedges' (4 replies at research time; the thread is hours old and moving). If someone has put a kWh figure on the fridge or hours on the 1,024 Wh pack, report instead of pasting. Otherwise paste into the reply editor (XenForo converts the ** marks to bold), do not click 'Post reply'.
- **Rules:** **Permanent-ban risk.** diysolarforum Code of Conduct: "Advertising is not allowed. Affiliate links, self-promotion, spam etc, will result in a permanent ban"; "It is ok to post basic links to products you like, but if we find that you are a shill, you will be banned." The last paragraph (link + disclosure) is what the rule aims at; the arithmetic above it stands on its own. Barry decides whether the link stays.
- **Notes for Barry:** the asker is in southern Spain on 230 V; our US store links do not serve him, which the text says. OUKITEL P1000PLUS figures (1,800 W, 1,024 Wh) are the OP's quoted listing, not checked against OUKITEL. Not repeated: ghostwriter66's MPPT/PWM and series-voltage points, Hedges' compressor-start, icemaker/defroster and idle-draw points.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Since nobody has put numbers on the fridge yet, here is the arithmetic for your plan, which I think works as long as you treat it as a daytime-fridge plan and not a 24-hour one.

**What the fridge takes.** A side-by-side American-style fridge-freezer is the hungriest household type: ENERGY STAR's certified-model medians run about 1.6–1.8 kWh a day for a 26 cu ft side-by-side (1.0–1.4 for top- and bottom-freezer types), measured at about 21 °C with the door mostly shut. That is an average of 65–75 W around the clock, with the compressor pulling 100–250 W while it runs, about 30–50 % of the time in a cool room and 80–90 % in a hot one. A fridge over ten years old can use twice the median. Your yellow EU energy label gives the kWh/year for your exact model; divide by 365.

**What 1,024 Wh buys.** Reckon about 85 % of the rated capacity reaches the plug through the inverter, so about 870 Wh, minus the inverter's own idle draw while it waits for the compressor (typically 10–15 W on units this size, so 120–180 Wh over 12 hours). On a 1.7 kWh/day fridge that is about 10 hours of fridge with nothing else plugged in. That is why a 1 kWh unit is an overnight-or-daytime device for a big fridge, and a full day without sun needs the 2 kWh class.

**What 300 W of panel returns.** A folding or rigid panel delivers roughly 60–75 % of its rating in good sun. With your 6 hours of winter sun that is about 1.1–1.3 kWh on a clear day, under 0.3 kWh on a fully overcast one. The fridge over a 12-hour day costs about 0.85 kWh plus about 0.15 kWh of inverter idle, so on a clear day the panel carries the fridge and leaves the battery close to full for the evening (TV, laptop, tablets and lights are about 0.3–0.5 kWh for a few hours). Two hours of fridge at night is about 0.15 kWh. A cloudy day is where the Honda earns its place: an hour of generator into the station's 1,200 W charger puts back more than the panel does all day.

**Two checks before the first outage.** Put a plug-in energy meter on the fridge for 24 hours now, so you have your number rather than the median. And run the whole setup once for a few hours including a compressor restart; a 1,800 W inverter starts any household compressor, but you want to see it do it.

For comparison, the sizing table and the 2 kWh options are in the piece I wrote for the US market (US store prices, so only the arithmetic carries over to Spain): https://dealectric.com/power-station-to-run-a-refrigerator-for-24-hours. I run dealectric.com, which earns a commission on some links.
```

## T3. Reply on Cartaholics, "Which 48v lithium actually fit?" (demand 3, opened 11-02, last post 11-03)

- **Where:** https://cartaholics.com/threads/which-48v-lithium-actually-fit.27920/
- **Account:** none in the vault; Barry creates one at https://cartaholics.com/register/ (Claude never creates accounts). XenForo may hold a new member's links for moderation.
- **Steps:** Open the thread, read every post after GolfCartTinkerer's dimension table (4 replies at research time). If someone has already raised the OBC bypass or priced kit-vs-bare, report instead of pasting. Otherwise paste into the reply editor, do not click 'Post reply'.
- **Rules:** Cartaholics terms ban "spam or spam-like" content; no written affiliate or link rule was found (checked /help/terms, /help, the posting-guidelines thread). Eco Battery sponsors the forum and the forum's own lithium guide recommends Eco first; expect readers to weigh brand against that.
- **Notes for Barry:** the asker's budget (under $1,000) is below anything we sell; the text says so plainly, so the value here is the OBC warning and the kit-vs-bare math, not a sale. The Vatrer mini's USD price could not be read today (US page 404, collection page rate-limited; CAD page shows $2,121), so the text prices only the narrow pack ($1,579.99 verified) and sizes the mini. The page's OBC year range was reconciled today (commit 4dbceda); the text avoids a year range anyway.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
GolfCartTinkerer's dimension table is the answer to the fit question: every full-size 48V 100Ah box (DC House, LiTime, Redodo) is 20.3–20.5 in long, so none of them goes across the A-frame. The packs that do are the short "mini"/"narrow" builds, and that is where the money goes: Vatrer's 48V 105Ah mini is 13.19 × 12.2 × 10.04 in and ships with a 58.4 V charger and LCD, and their narrow (9.76 in wide) 48V 105Ah is $1,579.99 with the same charger today. Both are about $600 over your ceiling, so the real choice is (a) stay under $1,000 with a long box and move or remount the Alltrax, or (b) spend ~$1,580 for a pack that fits across. Mock it up in cardboard first, as Tinkerer said.

Two things nobody has mentioned yet:

1. If your '96 is a 48V PowerDrive cart it has the Lester on-board computer (the 1996 DS thread here shows OBC 27155-01 v5.1, the version with no blue/white wires). A lithium charger plugs straight to the pack, so the OBC has to be bypassed or the cart won't run: on that version it is the yellow wire from the OBC to controller B−. If the cart is still 36V (Tinkerer's point about the solenoid coil), there is no OBC and you skip this.
2. "Under $1,000" buys a bare battery or a budget bundle; check whether the DC House listing you are looking at includes the 58.4 V lithium charger, because your old PowerDrive charger cannot be used after the bypass. If you decide the extra $300–600 for a complete kit is worth it, the cheapest complete one I priced on 11-03 was LiTime's 48V 100Ah kit at $1,281.66 on sale (charger, 500 A shunt monitor, hold-down bracket; 20.47 × 10.59 × 8.66 in, so longways only; 5-year warranty, no UL 2271 listed), and the cheapest UL 2271 kit was Vatrer's 48V 105Ah Club Car kit at $1,579.99 (also 19.69 in long; 10-year warranty, but only if you register it before the first charge, otherwise it drops to the standard term). The dealer kits (Allied, Epoch, Eco, Dakota, RoyPow) all start past $2,000.

I put the kit prices, dimensions, warranty fine print and the OBC note side by side here: https://dealectric.com/best-48v-lithium-golf-cart-battery-kit-with-charger-club-car . I run dealectric.com, which earns a commission on some links.
```

## T4. Reply on MacRumors, "KVM for 4k monitor" (demand 3, opened 10-28, last post 10-29)

- **Where:** https://forums.macrumors.com/threads/kvm-for-4k-monitor.2493115/
- **Account:** macrumors.com login in agent-vault (`list_accounts`, then `login`).
- **Steps:** Open the thread, check for posts after maflynn's (10-29). If someone has already said "switch the monitor's input and use a USB switch", report instead of pasting. Otherwise paste into the reply editor (XenForo; the "- " bullets stay as typed), do not click 'Post reply'.
- **Rules:** MacRumors: self-promotional links belong in signature/profile; established members may link their own site when it answers a specific question; a new account's self-link is treated as advertising (the forum itself rewrites Amazon links to its own affiliate tag). The research expects the link to be removed if our account counts as new; the text stands without it.
- **Notes for Barry:** one sentence is general knowledge, not from our page ("a KVM rated for 1080p60 or 4K30 will negotiate a lower mode and the monitor scales it up"); the research says cut it if unwanted. The PA279CV USB-C-upstream point could not be verified for that monitor, which is why the text says "check the manual".
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
The blur is the KVM, not the monitor: your old UGREEN box was fine at 1080p because that is what it was built to pass, and a 4K signal squeezed through it comes out resampled; a KVM rated for 1080p60 or 4K30 will negotiate a lower mode and the monitor scales it up. The cheap fix is to stop routing video through a switch at all. The PA279CV has more than one input, so plug the Mac mini into one (HDMI or USB-C) and the PC into the other (DisplayPort or HDMI), and let the monitor's input button do the "V" part; direct cable, nothing to degrade.

For the K and M, a USB switch (no video) moves the keyboard, mouse, webcam, or an external drive between the two computers with one button. Two kinds worth looking at:
- If you only need keyboard and mouse, a USB 2.0 switch is enough: UGREEN's 2-in-4-out USB 2.0 switch is $23.99 on UGREEN's US store ($16.99 at Adorama), 2 USB-A uplinks, one button. USB 2.0 is also the safer class for a Logitech or other 2.4 GHz receiver; UGREEN itself warns against putting receivers on USB 3 switches because of interference.
- If you also want to move a fast SSD or a USB-C device, UGREEN's USB-C switch (CM691) is $40.99: two USB-C uplinks with 0.8 m cables and a wired remote in the box, four 10Gbps USB 3.2 Gen 2 ports (3× A, 1× C), bus-powered, two-year warranty. If your PC only has USB-A, you need a USB-A-to-C data cable (not included) and UGREEN says to keep it under 0.8 m. Cable Matters' 201160 is the other 10Gbps option ($51–66 at resellers); the ATEN US3324, IOGEAR GUS432, Sabrent USB-SW30 and Plugable USB3-SWITCH2 are 5Gbps.

Two habits with any USB switch: eject a drive before you press the button (switching is electrically the same as pulling the plug; Plugable's and ATEN's own support pages say so), and expect each computer to re-enumerate the devices on each switch, which takes a second or two.

Also check the PA279CV's manual for a USB-C upstream: if the monitor's USB hub follows the active input, the monitor is the KVM and you may not need a separate switch for the keyboard and mouse.

I compared the USB switches here, with the cables-in-box, power and speed for each:
https://dealectric.com/best-usb-switch-two-computers-keyboard-mouse-ssd
I run dealectric.com, which earns a commission on some links.
```

## T5. Short reply on Level1Techs, "Need a >=3-way KM switch" (demand 3, opened 10-25, last post 10-29; solution accepted)

- **Where:** https://forum.level1techs.com/t/need-a-3-way-km-switch/259458
- **Account:** none in the vault; Barry creates one at https://forum.level1techs.com/signup (Claude never creates accounts). Same account as T1.
- **Steps:** Open the thread; the asker accepted Agent9's cascade idea on 10-29 but nobody named a model. If a model has been named since, report instead of pasting. Otherwise paste the text in Reply, do not click 'Reply'.
- **Rules:** as T1. The asker is outside the US; the text says the prices are a reference only.
- **Notes for Barry:** the research leaves it to Barry whether a thread that is solved in principle is worth a post.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
For the cascade switch Agent9 suggested: keyboard and mouse only need USB 2.0, and USB 2.0 is the better class if the mouse is wireless (UGREEN warns against 2.4 GHz receivers on USB 3 switches because of interference). Cheap 2-host options I have prices for, US store prices so only a reference for you: UGREEN's 2-in-4-out USB 2.0 switch, $23.99 on UGREEN's US store / $16.99 at Adorama, 2 USB-A uplinks, one button; Sabrent USB-SW30, $14.99, two USB-B uplinks and a single USB-A device port (one port is all the cascade needs); Plugable USB3-SWITCH2, $19.95, same shape at 5Gbps. The UGREEN 10Gbps USB-C switch you already have is the one in the same family that matters if a drive ever rides along.
Comparison with the cables-in-box and power for each: https://dealectric.com/best-usb-switch-two-computers-keyboard-mouse-ssd
I run dealectric.com, which earns a commission on some links.
```

## T6. Reply on Slickdeals, "Amazon UK BONITOYS 15.6-inch Quad Laptop Screen Extender $227.99 w/ code" (demand 3, posted 10-20, last comment 10-26)

- **Where:** https://slickdeals.net/f/20184846
- **Account:** none in the vault; Barry creates one at https://slickdeals.net/register/ (the Sign Up button on any Slickdeals page; Claude never creates accounts).
- **Steps:** Open the thread, read comments after OrangeKestrel6960's (10-26). If BoyangS's Mac-display-limit claim has since been corrected, report instead of pasting. Otherwise paste into the comment box, do not click 'Post'.
- **Rules:** **Removal risk.** Slickdeals forum rule 1: "Spam, self promotion and referral links are not allowed"; rule 12: refrain from linking competitive sites. Acceptable Use Policy §10: no using an account "to promote their own business or services or distribute referral links"; §6 no commercial use; §11 no links to competitive or prohibited sites; moderators decide case by case (§13). The research wrote the body to stand without the last paragraph; Barry decides whether it stays.
- **Notes for Barry:** the BONITOYS code expired 10-31 but the thread was not marked expired on 11-03; a reply still reaches the three undecided posters by notification. The panel bit depth OrangeKestrel6960 asked for is unknown for BONITOYS and not on our page either; the text says so.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
BoyangS, the M1-drives-one / M3-drives-two limit is real for native displays, but it isn't what decides this one. The listing says "one-time driver install", which means the extra screens run as USB display devices (DisplayLink or the maker's own driver), and macOS does not count those against the chip's native limit. That is the whole reason these clip-on triples exist for base M1/M2/M3 Macs: a base-chip MacBook Air that natively allows one external display drives all three panels through the driver. The trade-offs are the driver itself (on a Mac you install it by hand and grant Screen Recording permission; a company-managed laptop may block the install outright, which is the single most common "didn't work" story on these), some pointer latency, and no HDR or protected-video playback on those screens. Fine for text, spreadsheets, Slack and trading screens; not for video editing or games.

OrangeKestrel6960, I couldn't find the bit depth for this BONITOYS anywhere, and the listing doesn't say; the makers in this category rarely publish it (FOPO, the one brand I did check, lists 100% sRGB and no bit depth). Two spec points that do matter and are on the listing: the panels are 1080p 16:9, and 15.6-inch. Next to a 16-inch 16:10 laptop (2560 × 1600 or 1920 × 1200) they sit visibly shorter and you get less vertical room per document. If your laptop is 16:9 that doesn't matter and $228 for three 1080p panels is the cheapest multi-screen price I have seen this autumn (QQH's 12–16-inch triple has been $182–250 on here all summer).

If you do want panels that match a 16-inch 16:10 laptop, the only triple I found at that spec is FOPO's S788: three 16-inch 1920 × 1200 IPS at 100% sRGB, fits 12–18.5-inch laptops, driver-based like this one, PD supply in the box, $499.99 with a 10% code on FOPO's own site ($450). Twice the money, 2.64 kg on the lid, and you only want it if the 16:10 match matters to you. The 2K options (UPERFECT's 16-inch 2560 × 1600 triple) start around $640.

I keep the comparison (specs, drivers, Mac notes, prices as of Nov 3) at https://dealectric.com/best-triple-screen-laptop-extender-16-inch-1920x1200. Disclosure: I run dealectric.com, which earns a commission on some links there (the FOPO row); the others are plain comparisons.
```

## T7. Reply on Cartaholics, "2022 Villager LSV Lithium Conversion" (demand 3, opened 10-15, last post 10-19)

- **Where:** https://cartaholics.com/threads/2022-villager-lsv-lithium-conversion.27883/
- **Account:** none in the vault; Barry creates one at https://cartaholics.com/register/ (Claude never creates accounts). Same account as T3.
- **Steps:** Open the thread (4 replies at research time) and confirm the asker's wording about buying "a lithium package" for a trip "next month" (the research paraphrased it from a fetched page). If a brand has since been chosen or kit prices posted, report instead of pasting. Otherwise paste into the reply editor, do not click 'Post reply'.
- **Rules:** as T3 (no written link rule; "no spam"; Eco Battery sponsors the forum and rjs_boy already recommended Eco; the text does not argue against that).
- **Notes for Barry:** 15 days quiet, but the asker said he installs at the property in November, so a post now still lands before the purchase. Whether the Vatrer kit fits the Villager 2+2 tray is unverified on both sides; the text says so.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Since you are buying the package before the trip, here is what the complete kits (battery + lithium charger + gauge + hold-down) cost on 11-03, so you can weigh rjs_boy's Bolt/Eco advice against price:

- Dealer-channel kits: Allied 48V 105Ah set $2,045–2,395, Epoch 48V 105Ah $2,299, Dakota Lithium 48V 96Ah about $2,699, RoyPow 48V 105Ah $2,999.99 (sold out). Eco's current 48V price I could not confirm.
- Direct-to-consumer: Vatrer 48V 105Ah Club Car kit $1,579.99 (UL 2271, 200 A BMS, 58.4 V 18 A charger, LCD, bracket; 10-year warranty, but only if you register and activate it before the first charge, and returns are 7 days). LiTime 48V 100Ah kit $1,281.66 on sale against $1,649.99 list (58.4 V 18 A charger, 500 A shunt monitor, bracket; 5-year warranty; no UL 2271 shown).

Two caveats specific to your cart. The Vatrer kit is 19.69 × 12.52 × 9.6 in and Vatrer lists it for the DS, Precedent, Tempo and Onward, not the Villager 2+2, so measure the tray before ordering; the LiTime box is 20.47 × 10.59 × 8.66 in. And both have 200 A BMSs: that clears the 175 A continuous a stock cart needs per the forum's "How to choose a Lithium Battery" guide, but it is under the 250 A headroom rjs_boy suggested, so if you plan a bigger controller or a lot of lighting, stay with the Bolt/Eco class he named. Whatever you buy, the lithium charger's aux output for the on-charge interlock (rjs_boy's point) is worth asking the seller about before you are on site with no return window.

Prices, specs and the warranty fine print side by side: https://dealectric.com/best-48v-lithium-golf-cart-battery-kit-with-charger-club-car . I run dealectric.com, which earns a commission on some links.
```

## T8. Reply on Level1Techs, "Extreme Noob: Ugreen NAS Setup" (demand 3, opened 10-10, 0 replies)

- **Where:** https://forum.level1techs.com/t/extreme-noob-ugreen-nas-setup/258288
- **Account:** none in the vault; Barry creates one at https://forum.level1techs.com/signup (Claude never creates accounts). Same account as T1.
- **Steps:** Open the thread; if it is still unanswered, paste the text in Reply (Discourse renders the Markdown), do not click 'Reply'. If someone has answered since, report.
- **Rules:** as T1.
- **Notes for Barry:** the honest answer favours the box he already picked (he wants ARM and distrusts Intel), so the research expects low conversion and leaves it to Barry whether it is worth posting; it is the only page that compares UGREEN's two lines, and the thread is open. Not on our page (general knowledge, be comfortable with them before posting): UGOS per-folder read-only permissions, Tailscale's free tier and invites for relatives, the StarCraft/Battle.net statements. DH4300 Plus specs and $399.99 verified today.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Short version: for what you've described, the DH4300 Plus is a fine choice and you don't need to second-guess it. Point by point:

- **Tailscale is safe** and is exactly the tool for "admin access to my drives from anywhere". It makes a private network between your devices with no port opened on your router, works behind carrier NAT, and the free tier covers a family. Immich's own remote-access guide lists it as one of the three sane routes (the other two: a WireGuard VPN with a forwarded port, or a domain with HTTPS through a reverse proxy) and warns never to expose a service's port bare to the internet. Install the Tailscale client on the NAS and on your phone/laptop; relatives in other states get a Tailscale invite, or a plain share link from UGOS if you'd rather not put them on your tailnet.
- **Read-only folders for relatives:** per-user, per-shared-folder read/write or read-only permissions are a standard NAS feature and UGOS has them; make one user per relative, grant read-only on the folders you choose. Keep admin for yourself only.
- **Is UGOS good?** It's a locked-down Debian (no apt, GUI-first), which for a self-described beginner is the right trade. Two years' warranty. The brand's stance on third-party OSes is unofficial.
- **"Better options?"** The one real fork is ARM vs x86. The DH4300 Plus (8-core A76+A55, 8 GB) is $399.99 on UGREEN's US store today; its Intel sibling the 2-bay DXP2800 (N100, 8 GB to 16 GB, two M.2 slots) is $389.99. x86 matters only if you later want Docker containers that only ship amd64 images, virtual machines, or a self-hosted photo app with face search (Immich wants an x86-64 CPU for its machine-learning container). For file shares plus Tailscale, ARM is enough and runs cooler. You've said you want ARM; nothing in your list argues against it.
- **StarCraft 1 hosting:** a NAS won't host Brood War games. StarCraft: Remastered matchmakes through Battle.net; a LAN game needs one of the players' PCs to host. Nothing to buy for that.

If you ever add phone photo backup to the list, this is the write-up of what Immich needs on the box and on the iPhone: https://dealectric.com/best-nas-for-immich-iphone-photo-backup
I run dealectric.com, which earns a commission on some links.
```

## T9. Reply on the Home Assistant community, "Home server: mini PC, 3 NVMe SSDs, 2.5 GbE, Zigbee, Matter/Thread" (demand 3, opened 09-30, 0 replies)

- **Where:** https://community.home-assistant.io/t/home-server-mini-pc-3-nvme-ssds-2-5-gbe-zigbee-matter-thread/1026929
- **Account:** none in the vault; Barry creates one at https://community.home-assistant.io/signup (Claude never creates accounts).
- **Steps:** Open the thread; if it is still unanswered (0 replies after five weeks at research time), paste the text in Reply (Discourse renders the Markdown), do not click 'Reply'. If someone has answered since, report.
- **Rules:** **ToS risk.** Home Assistant community guidelines have no link rule, but the ToS §2 bans "unwanted commercial content designed to drive traffic to third party sites". The research's defence is a full answer plus the disclosure; Barry decides.
- **Notes for Barry:** not on our page: the USB-extension tip for Zigbee radios (general practice); "Zigbee2MQTT" and "the Matter server as separate containers" are the research's inference from the page's "Container install has no add-ons". Home Guard (his ad blocker) is not addressed; it is one more container on either box.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Nobody answered, so here's the shape of the decision. Your list is really two machines' worth of jobs (Home Assistant + Zigbee/Thread radios, and Immich/Jellyfin + several days of camera footage), and the box depends on whether you insist on NVMe-only.

**If you want exactly "3 NVMe + 2.5GbE" and nothing spinning:** the Beelink ME mini is the obvious fit: Intel N150, 12 GB LPDDR5 (soldered, not upgradable), six M.2 slots, no SATA, two 2.5GbE ports, about 8 W idle, $209 barebone at launch. It ships with no NAS software, so it's a Proxmox box: Home Assistant OS in a VM (HAOS wants 2 GB RAM, 2 vCPUs, UEFI, a bridged NIC), Immich and Jellyfin in Docker in an LXC or small VM. The 12 GB ceiling is the catch: Immich wants 8 GB recommended (6 minimum) with its machine-learning container on, HAOS takes 2, and you still want headroom for the camera recorder. It works if you run Immich with ML off or on a schedule.

**If you'd rather have an appliance with drive bays (footage and media on HDDs, apps on SSD):** the UGREEN DXP2800, $389.99 diskless: Intel N100, 8 GB DDR5 in one SO-DIMM slot (16 GB max), two M.2 slots plus two 3.5" bays, 2.5GbE, UGOS with a Docker app (Compose projects) and a VM app; owners run Home Assistant OS as a VM on it, though one DXP2800 owner reported the VM getting no IP address with no clear fix in that thread. About 5 W idle hibernating, 16 W active. With the 16 GB upgrade, Immich (ML on) + HAOS + Jellyfin fit; put the Docker pool on an M.2 so Immich's Postgres and thumbnails never sit on the HDDs (Immich says never on a network share).

Things that are the same on either box:
- **Zigbee / Thread sticks must be passed through by hand** to the VM (or container) on every platform. Plan a USB extension so the radio isn't next to the chassis.
- **Home Assistant Container has no add-ons**, so if you go the container route you run the Matter server, Zigbee2MQTT etc. as separate containers yourself; HAOS in a VM gives you the add-on store.
- **Immich on iPhone** backs up only when iOS lets it (Background App Refresh on, open the app now and then); first upload in the foreground. The first ML pass over a big library on an N100/N150 runs hours to days (one owner: ~300 photos/hour with ML on, ~5,000 with it off), so import first, let faces run after.
- **Remote access:** Tailscale on phone and box (no open port), or a domain + HTTPS reverse proxy; never forward Immich's port 2283 bare.
- **Camera footage** is continuous writes; on the Beelink that's NVMe endurance you're spending, on the DXP2800 it's a cheap HDD. That's the strongest argument for the second box if the cameras matter.

My pick for your list: the DXP2800 with a 16 GB SO-DIMM and your 990 Pro in one M.2 slot for the app pool, footage on an HDD. If you really want all-flash and you're happy in Proxmox, the ME mini and accept the RAM limit. Comparison table with the alternatives (Synology DS225+ at 2 GB, TerraMaster F2-425 Plus, the ARM boxes that can't run x86 containers): https://dealectric.com/best-nas-under-500-for-docker-immich-home-assistant
I run dealectric.com, which earns a commission on some links.
```

## T10. Short reply on Slickdeals, "Prime: 15.6-inch FLYTOCCA FHD IPS Laptop Screen Extender $66" (demand 3, question 09-19 unanswered, last comment 09-24)

- **Where:** https://slickdeals.net/f/20034240
- **Account:** none in the vault; Barry creates one at https://slickdeals.net/register/ (Claude never creates accounts). Same account as T6.
- **Steps:** Open the thread; if DevanteWeary's 18-inch question is still unanswered, paste into the comment box, do not click 'Post'. The deal is expired, so the thread is quiet; a reply still reaches the asker by notification.
- **Rules:** as T6 (**removal risk**: Slickdeals rule 1 and AUP §10). The body stands without the last paragraph; Barry decides.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
DevanteWeary, on the 18-inch question: the only clip-on extender I found that states a fit past 17.3 inches is FOPO's S788, listed for 12–18.5-inch laptops, with the usual caveat that it is the laptop's physical lid dimensions that decide it, not the diagonal. It is a triple (three 16-inch 1920 × 1200 panels), weighs 2.64 kg and comes with its own power supply, so it is sized for heavy machines like an 18-inch gaming laptop, and the balance worry bb6619 raised about a 16-inch doesn't apply the same way to an 18-inch chassis. Driver-based, $499.99 on FOPO's site, 10% code on the page. For single-screen 18-inch options I haven't found one that states the fit; the FLYTOCCA, QQH and KYY units all stop at 17.3.

On the balance argument: the heavier triples put a rear support leg behind the laptop for this reason; the single-screen clip-ons rely on the hinge, which is BurritoSupremo's point.

Specs and the other units I compared: https://dealectric.com/best-triple-screen-laptop-extender-16-inch-1920x1200. Disclosure: I run dealectric.com, which earns a commission on some links there.
```

## T11. Reply on Level1Techs, "Two MacBooks + gaming PC, 2-3 4K144 monitors: can this be done with one KVM?" (demand 3, opened 09-23, unresolved)

- **Where:** https://forum.level1techs.com/t/two-macbooks-gaming-pc-2-3-4k144-monitors-can-this-be-done-with-one-kvm/257041
- **Account:** none in the vault; Barry creates one at https://forum.level1techs.com/signup (Claude never creates accounts). Same account as T1.
- **Steps:** Open the thread (4 posts at research time, two by wendell). If the asker has bought or the thread has closed (Discourse auto-close), report. Otherwise paste the text in Reply, do not click 'Reply'.
- **Rules:** as T1, plus a sensitivity the research flags: Level1Techs is run by a company that sells KVMs, and the linked page rates their unit at 4K120; a disclosed link to it is fair but may read as competitive.
- **Notes for Barry:** Apple's external-display page did not yet cover the M5 Pro the asker mentions; the text says to check it.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Adding to what wendell said about bandwidth, three things that will bite before the KVM does:

1. Apple's own caps. Apple's external-display page lists the M4 and M4 Pro MacBook Pro at one display up to 4K240 or two displays at 4K144 each; three 4K144 panels from one Mac is out on those chips regardless of the switch. (Apple's page does not yet cover the M5 Pro you mention; check it before buying anything.) Thunderbolt 4 carries DisplayPort 1.4, Thunderbolt 5 carries DP 2.1.
2. DSC. 4K144 at 10-bit does not fit DP 1.4 uncompressed (4K120 8-bit does), so the Mac, the KVM and the monitor must all negotiate Display Stream Compression, and macOS does not document DSC. Level1Techs rates its own DP 1.4 KVM at 4K120 for exactly this reason, and a member's LG 27GP950 pair held 4K144 only with the KVM removed. TESmart's DKS403-class units and Cable Matters' DP 1.4 KVM both claim 4K144 with EDID emulation 2.0 / a DSC-capable host; I found no independent test of either with a Mac. HDMI 2.1 carries 4K144 without DSC, but the HDMI 2.1 KVMs pass one HDMI link per M-series Mac.
3. Macs and re-handshakes. A KVM without working monitor emulation makes macOS see a new display on every switch: windows and Spaces shuffle (turn off "automatically rearrange Spaces based on most recent use") and owners of the UGREEN DP KVMs report the Mac not waking until the lid is closed and reopened. No KVM in this class charges the laptop, so the Element 5 docks stay in the chain either way.

The setup that avoids the switch for two of your three machines: monitors with a built-in KVM. Each takes the PC on DisplayPort/HDMI 2.1 and one Mac on USB-C (USB-C-to-DP 1.4 or Thunderbolt cable), its input button swaps machines, and its USB hub follows the input. Gigabyte's M27UP does 4K160 for about $299–329 (USB-C power is only 18 W, keep the Mac charger); BenQ's PD3226G does 4K144 over Thunderbolt 4 at $969–1,136. That covers one Mac + PC per monitor; the second Mac still needs either a KVM or its own input. For the peripherals a plain USB switch with a button (UGREEN's USB-C switch, $40.99, four 10Gbps ports, two USB-C uplinks) is cheaper and simpler than routing USB through the KVM.

What I found on each KVM's 4K144 claim, Apple's limits and the Mac reports is here:
https://dealectric.com/kvm-switch-for-a-mac-and-pc-4k-144hz
I run dealectric.com, which earns a commission on some links.
```

## T12. Reply on Amazon's Blink forum, "Blink camera solar accessories" (demand 3 if the asker is still shopping; date unverified)

- **Where:** https://www.amazonforum.com/s/question/0D5at00000aQczSCAS/blink-camera-solar-accessories
- **Account:** none in the vault; the forum takes an Amazon login (Sign in button on amazonforum.com). Barry signs in or creates the account himself (Claude never creates accounts).
- **Steps:** The forum does not render for our tools (Salesforce shadow DOM); the research saw only search snippets, so **dates, reply counts and existing answers are unverified**. Open the thread and read it in full first. If the last post is within 45 days, proceed; if older, treat it as evergreen and post only if Barry sees it on page 1 for "solar panel for Blink Outdoor 4". If a member has already named a specific USB-C panel with price and the AA-removal step, report instead of pasting. Otherwise paste into the reply box (plain text, no Markdown), do not click 'Post' / 'Answer'. Also read the pinned forum guidelines before posting.
- **Rules:** **Removal risk.** Amazon's forum guidelines bar promotional posts and external commercial links (exact text not readable by our tools); staff moderate.
- **Blink precondition:** met; the page was corrected today (commit 4dbceda) to list Blink Solaris, the Battery Extension Pack's USB caveat and the $19.99 generic panel price.
- **Notes for Barry (research's cut-before-posting note, conditional):** cut the first paragraph's mount facts if Amazon staff already said them (the snippet says they did); keep "and which was only ever sold with a camera in the US" only if no member said it.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
For an Outdoor 4 you have two real options, and neither is the Blink Solar Panel Mount, which Blink's FAQ limits to the Outdoor (3rd Gen) because of its micro-USB connector and which was only ever sold with a camera in the US.

1. Blink Solaris (official, 2026): a solar panel and battery pack that clicks onto an Outdoor 4 or Outdoor 2K+, $39.99 at Best Buy or Amazon, IP65 when attached. It can't be mounted away from the camera, so it only works if the camera itself gets sun. Early reviews are mixed on charging.

2. A third-party USB-C panel with an internal battery, mounted where the sun is. Wasserstein's is $36.99 (2-pack $63.99) with a 13.1 ft cable, 360° mount and the USB-C adapter; generic 4 W panels are $20–30. You remove the two AAs (lithium AAs don't recharge) and take the USB-C port cover off; the panel's plug seals the port, which is the maker's claim, not Blink's, and Blink's own page says the camera isn't weather-resistant with the cover off. Wasserstein gives 30-day returns and a 3-month warranty.

One thing not to combine: Blink's Battery Extension Pack fits the Outdoor 4, but Blink says you can't plug USB power in while it's attached, so it's either the pack or a panel.

Full comparison with the FAQ quotes: https://dealectric.com/solar-panel-for-blink-outdoor-4-without-a-camera-bundle
I run dealectric.com, which earns a commission on some links.
```

## T13. Reply on Level1Techs, "Advice Needed - Aging Hardware" (demand 2–3, opened and last post 10-16)

- **Where:** https://forum.level1techs.com/t/advice-needed-aging-hardware/258714
- **Account:** none in the vault; Barry creates one at https://forum.level1techs.com/signup (Claude never creates accounts). Same account as T1.
- **Steps:** Open the thread (9 posts at research time). If the asker has since chosen a NAS or the thread has closed, report. Otherwise paste the text in Reply, do not click 'Reply'.
- **Rules:** as T1.
- **Notes for Barry:** not on our page (general knowledge): the Q9550's 60–100 W draw and the rsync/SMB migration steps. Quick Sync for Jellyfin transcodes is inferred from the page's note that Immich can use Quick Sync through /dev/dri on the N100, not stated for Jellyfin. The page documents the DXP2800's VM app through owner guides (HAOS), not for general Linux VMs.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
On the "off ramp for the NAS" specifically, since the replies have covered the lab side: your ~7 TB on a Core 2 Quad with a dying boot stick is the one urgent item, and a $400 2-bay box is the cheapest way to make it stop being urgent.

A UGREEN DXP2800 ($389.99 diskless) plus two 10–12 TB drives in a mirror holds the 7 TB with room to grow, idles around 5 W against a Q9550's 60–100 W, and does the two things you listed: Jellyfin or Plex in its Docker app (N100 with Quick Sync for transcodes) and "some virtual machines for learning" in its VM app, with 8 GB DDR5 upgradable to 16 GB. Moving the data: build the new mirror, mount the FreeNAS share from the UGREEN (or rsync from the FreeNAS shell to the new SMB share), verify counts, then retire the old box. purkkaviritys's 8 TB external is the belt-and-braces copy during the move and the backup afterwards. CrashPlan dropping mapped drives stops mattering once the NAS itself runs a backup job to that external or to a cloud bucket.

That leaves the full $600 of your budget for the gaming PC's new board/CPU, which is where purkkaviritys is right that the 64 GB DDR4 and 2080 Ti are the parts worth keeping. If you'd rather turn the 3770K rig into the lab as you said in post 5, the NAS still stands on its own: it's the thing that should be boring and always on, and the lab the thing you break.

The under-$500 comparison (DXP2800 vs Synology DS225+, TerraMaster, Asustor, QNAP) is here: https://dealectric.com/best-nas-under-500-for-docker-immich-home-assistant
I run dealectric.com, which earns a commission on some links.
```

## T14. Reply on Amazon's Blink forum, "New Solaris for Outdoor 4 / 2K Camera" (demand 2–3; Solaris owners weighing a third-party switch; date unverified, after 2026-05-20)

- **Where:** https://amazonforum.my.site.com/s/question/0D5at00000qpb2nCAA/new-solaris-for-outdoor-4-2k-camera
- **Account:** none in the vault; Amazon login as T12. Barry signs in or creates the account himself (Claude never creates accounts).
- **Steps:** As T12: the forum does not render for our tools, so read the full thread first and record the dates (tier A or B to be confirmed). If someone has already given a specific separately-mounted alternative with price, cable length and the AA/port-cover trade-off, report instead of pasting. Otherwise paste (plain text), do not click 'Post' / 'Answer'. Read the pinned guidelines first.
- **Rules:** as T12 (**removal risk**: no promotional posts or external commercial links; staff-moderated).
- **Blink precondition:** met (commit 4dbceda).
- **Notes for Barry (research's cut-before-posting note, conditional):** cut the first paragraph if a staff member already quoted the "Charging" status FAQ (snippets suggest they did); in that case keep only the 2K+-only readout line and the no-separate-mount point.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Two things worth knowing before you give up on solar for the Outdoor 4.

First, Blink's own troubleshooting for Solaris is thin: the FAQ says to put it in direct sun for 45 minutes and check that the app shows "Charging" under the accessory; if it never does, "Blink Solaris is not charging your camera." It also says in-app battery and charging status is only shown for the Outdoor 2K+, so on an Outdoor 4 you may not get a reliable readout even when it works. Solaris clicks onto the camera and cannot be mounted separately, so if the camera sits in shade the panel does too.

Second, the alternative is a USB-C panel with its own battery that you mount where the sun is. Wasserstein's panel for the Outdoor 4/3/XT2/XT is $36.99 on their US store today (list $48.99; 2-pack $63.99), with an internal battery, a 13.1 ft cable, a 360° mount and the USB-C adapter the Outdoor 4 needs. Generic 4 W USB-C panels with a 2000 mAh battery run about $20–30 on Amazon. The trade-offs: you take the two lithium AAs out (they don't recharge; the camera runs off the panel's battery day and night), and the USB-C port cover comes off, so the panel's plug is what seals the port. Blink's support page says the Outdoor 4 is no longer weather-resistant with the cover off, and the seal is the panel maker's claim, not Blink's. Wasserstein gives 30 days to return and a 3-month warranty, so a shaded or stubborn camera is a cheap test.

I put the comparison (Solaris, Wasserstein, generic 4 W, Blink's old mount) with the Blink FAQ quotes here: https://dealectric.com/solar-panel-for-blink-outdoor-4-without-a-camera-bundle
I run dealectric.com, which earns a commission on some links.
```

## T15. Reply on Level1Techs, "Thoughts on Minisforum S5 (5x M.2) NAS, fanless!" (demand 2, opened and last post 10-22)

- **Where:** https://forum.level1techs.com/t/thoughts-on-minisforum-s5-5x-m-2-nas-fanless/259285
- **Account:** none in the vault; Barry creates one at https://forum.level1techs.com/signup (Claude never creates accounts). Same account as T1.
- **Steps:** Open the thread (6 posts at research time, last 10-22; revival is allowed within 6 months). If someone has since posted heat/noise numbers for a fan-cooled all-flash box or an alternative with prices, report. Otherwise paste the text in Reply (Discourse renders the Markdown), do not click 'Reply'.
- **Rules:** as T1. The research adds: a DIY-leaning crowd, so the text leads with the lane/heat point, not the product.
- **Notes for Barry:** facts not from our pages and attributed to the thread: the S5's lane width (Agent9), its EUR 659 price and 15 W fanless spec (OP); we do not list the S5 and its spec sheet was not verified. The Flashstor heat figures are from the first-generation Flashstor review our page cites, not the Gen2.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
The x1 slots are less of a problem than the fanless part, and it helps to separate the two.

**Lanes.** One PCIe 3.0 lane carries about 985 MB/s and a 10GbE link about 1.1 GB/s, so a single x1 slot already fills the network; a Gen4 x1 slot (which is what Agent9 says the S5 gives each drive) has headroom to spare over 10GbE. Extra lanes only pay off for RAID rebuilds, local transcoding, or a direct Thunderbolt/USB4 link to one machine. For a box that serves files over 10GbE, five Gen4 x1 slots are fine.

**Heat.** This is where I would not go fanless with five populated drives. A review of the first-generation Asustor Flashstor (also an N-series, actively cooled) found unheatsinked drives at 75–85 °C and throttling when fully populated. For comparison, the one all-flash box I have numbers for with a fan: the UGREEN DXP480T Plus (Core i5-1235U, four M.2 slots, two of them PCIe 4.0 x4, 10GbE, two Thunderbolt 4 ports) measured 40–42 dBA on a 100 GB copy with the CPU at 69 °C, 71 °C with throttling only under a synthetic stress test, in Default fan mode; it ships thermal pads for the four drives and has Quiet and Full Speed modes. So "quiet" with a fan is reachable; "silent" with no fan and five drives is where ozlay's "some external airflow across the fins" caveat turns into a requirement. If you do buy the S5, drives with heatsinks, or at least the pads, are not optional.

**What the alternatives cost (US store prices, 2026-11-03):** TerraMaster F8 SSD Plus, eight slots at PCIe 3.0 x1 each, i3-N305, 10GbE, $799.99 list; Asustor Flashstor 6 Gen2, six slots, Ryzen V3C14, 10GbE, two USB4 ports, about $799–899; UGREEN DXP480T Plus, $899.99 (on sale from $999.99, no end date). The S5 at EUR 659 undercuts all three, which is a real argument for it if you solve the airflow.

**The part everyone skips:** the drives cost more than the box. Four 2 TB NVMe drives are roughly $1,200–1,600 right now (Crucial P3 Plus about $306–345 each, Lexar NM790 about $379), four 4 TB drives $2,000–3,400. Late-2026 NAND prices move weekly, so check before committing to a slot count you will not fill.

I put the comparison with slots, lanes per slot, LAN, Thunderbolt/USB4 and prices in one table here: https://dealectric.com/best-all-nvme-nas-under-900 — I run dealectric.com, which earns a commission on some links.
```

---

# Section B. Evergreen and correction items (at most two per page; conditions stated)

## T16. Correction comment on conversionofenergy.com, "Best Solar Panel For Blink Outdoor 4" (correction; title claims "Updated: November 2026")

- **Where:** https://conversionofenergy.com/best-solar-panel-for-blink-outdoor-4/ (WordPress comment form at the bottom; no comments shown)
- **Account:** none needed (comment form). Name: Barry. Email: hello@dealectric.com. Website: leave blank.
- **Steps:** Scroll to the comment form, fill name, email and the text, do not click 'Post Comment'.
- **Rules:** moderated WordPress comments; no stated link policy. The text discloses the affiliation.
- **Blink precondition:** met (commit 4dbceda).
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Three corrections for anyone buying from this list. The Outdoor 4's charging port is USB-C, not "USB Type-A male" as the compatibility section says, so a panel has to end in a USB-C plug (Wasserstein ships a converter; the 4 W generics are USB-C natively). "Blink's solar panel" in the Outdoor 4 section isn't a product Blink makes: the Blink Solar Panel Mount fits only the Outdoor (3rd Gen) per Blink's FAQ. The official option for the Outdoor 4 is Blink Solaris (released 2026, $39.99), a panel-plus-battery that clicks onto the camera and can't be mounted separately, which the article doesn't mention. For a panel you can place in the sun, Wasserstein's is $36.99 (13.1 ft cable, internal battery, USB-C adapter) and generics run $20–30; with any of them the AAs come out and the port cover comes off, which Blink says removes the weather resistance until it's back on.
I compared all four with the Blink FAQ quotes at https://dealectric.com/solar-panel-for-blink-outdoor-4-without-a-camera-bundle
I run dealectric.com, which earns a commission on some links.
```

## T17. Answer on Quora, "What is a reliable but affordable power station that can run a refrigerator and microwave during a blackout?" (demand 3; one answer, May 2026)

- **Where:** https://www.quora.com/What-is-a-reliable-but-affordable-power-station-that-can-run-a-refrigerator-and-microwave-during-a-blackout
- **Account:** none in the vault; Barry creates one at https://www.quora.com/ (Continue with Google as barrryyao@gmail.com is the quickest route; Claude never creates accounts, not even through a Google sign-in).
- **Steps:** Open the question, confirm Morgan Chandler's is still the only answer (the "May 24" date is read as 2026 from Quora's display convention, not verified). Click 'Answer', paste the text (Quora does not render Markdown; the research's ** marks have been removed here), do not click 'Post'.
- **Rules:** Quora's own policy text could not be fetched; third-party 2026 write-ups agree that direct or cloaked affiliate URLs are treated as spam, a relevant link to your own site with the affiliation disclosed in the body is tolerated, and mostly-promotional answers get collapsed.
- **Notes for Barry:** Morgan Chandler's "about 2,200 W nominal" figure is kept as the one point of agreement. ALLPOWERS S2000 Pro was sold out on 11-03, which the text says.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Treat the two appliances as two different questions, because they are.

The refrigerator is a capacity question. A full-size fridge uses about 1.0–1.8 kWh a day (ENERGY STAR certified-model medians: about 1.0 for an 18 cu ft top-freezer, 1.4 for a 22 cu ft French door, 1.8 for a 26 cu ft side-by-side with a dispenser). The compressor only runs 30–50 % of the time at room temperature, so "500 W fridge" on the nameplate is not what you pay for all day. Count about 85 % of a station's rated watt-hours as usable, subtract the inverter's idle draw (about 15 W, so 360 Wh a day), and a 1 kWh station gives 11–17 hours of fridge, a 2 kWh station 22–35 hours, a 3 kWh station 33–51. The one measured run I know of: Bob Vila's reviewer ran a full-size fridge on a 2 kWh BLUETTI Elite 200 V2 for over 30 hours.

The microwave is a wattage question. A 1,000–1,200 W microwave draws about 1,500 W from the wall for the few minutes it runs; each 5-minute use costs roughly 100–125 Wh, which is nothing against a 2 kWh battery. What matters is that the inverter carries 1,500 W plus the fridge's compressor if it starts at the same moment, which is why 2,000 W continuous is the floor (the 2,200 W figure above is right in spirit). Every 2 kWh LFP unit on sale today clears it with 2,400–2,600 W; the 1 kWh class (1,500–1,800 W) is marginal with a microwave in the mix.

Affordable and reliable, as of November 2026: the 2 kWh class is $800–1,030 right now. The BLUETTI Elite 200 V2 is $899 (2,073.6 Wh, 2,600 W, LiFePO4 rated 6,000 cycles, 5-year warranty) and has that 30-hour fridge test behind it; the Jackery Explorer 2000 v2 is around $799 on sale (2,042 Wh, 2,200 W); the Anker SOLIX C2000 Gen 2 is $899.99 (2,048 Wh, 2,400 W); the EcoFlow DELTA 2 Max is $1,029 (2,048 Wh, 2,400 W). Cheaper for a day's cover: the ALLPOWERS S2000 Pro at $549 (1,451 Wh NMC, 2,400 W, about 16–19 hours of fridge), though it was sold out when I checked on November 3. Skip the 1 kWh units for this job: they will not carry a full-size fridge through a day.

Two habits double the value of whatever you buy: keep the door shut (an unopened fridge holds safe temperatures about 4 hours, a full freezer about 48, so you can run the station on a schedule rather than continuously), and test it once with a plug-in watt meter including a compressor restart before you need it.

Full table with prices and codes checked daily: https://dealectric.com/power-station-to-run-a-refrigerator-for-24-hours. I run dealectric.com, which earns a commission on some links.
```

## T18. Answer on Quora, "Would a 1000Wh station be enough for fridge + modem during outages?" (demand 3; four answers, June 2026)

- **Where:** https://www.quora.com/Would-a-1000Wh-station-be-enough-for-fridge-modem-during-outages
- **Account:** as T17 (Quora; none in the vault; Barry creates it).
- **Steps:** Open the question; the four answers span 6 to 24 hours and none uses a daily-kWh figure (dates "Jun 10–11" read as 2026, unverified). If a newer answer has done the arithmetic, report. Otherwise click 'Answer', paste the text (** marks removed for Quora), do not click 'Post'.
- **Rules:** as T17.
- **Notes for Barry:** Mats Petersson's range is credited; Charles Edwards' 6-hour figure is corrected (it assumes a 100 % compressor duty cycle).
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Short version: yes for an overnight or a working day, no for a full 24 hours with a full-size fridge. Mats has the range right; here is why the answers above span 6 to 24 hours.

The fridge. Its compressor draws 100–250 W while running but only runs 30–50 % of the time in a room-temperature kitchen, so a full-size fridge uses about 1.0–1.8 kWh a day (ENERGY STAR medians: 1.0 kWh for an 18 cu ft top-freezer, 1.4 for a French door, 1.8 for a side-by-side with dispenser). "150 W for 6 hours" would be true only if it never cycled off.

The modem (and router). 10–20 W, but it never cycles: 240–480 Wh a day. That is a quarter to half of a 1,000 Wh station on its own.

The station. About 85 % of the rated watt-hours reach the outlet, and the inverter idles at roughly 10–15 W while it waits for the compressor, another 240–360 Wh a day. So: 1,000 Wh × 0.85 = 850 Wh; minus 300 Wh of modem and 300 Wh of idle over 24 hours leaves 250 Wh for a fridge that wants 1,000–1,800. Over 12 hours the same sums leave about 550 Wh against a fridge need of 500–900: an overnight is fine for a top-freezer, tight for a side-by-side, and a hot kitchen (duty cycle 80–90 %) breaks it.

What to do with it. Run the fridge on a schedule rather than continuously: an unopened fridge holds safe temperatures for about 4 hours and a full freezer about 48, so 1 hour on, 2 off keeps food safe and stretches 1,000 Wh across a day while the modem stays on. If you want the fridge covered for a day without thinking about it, the 2 kWh class (about $800–900 now, e.g. BLUETTI Elite 200 V2 $899, 2,073.6 Wh, 2,600 W, 30+ hours on a full-size fridge in Bob Vila's test; Jackery Explorer 2000 v2 about $799) is the right size, and a 1 kWh unit is the right size for the modem, phones, lights and a few hours of fridge.

The hours-per-kWh table and current prices: https://dealectric.com/power-station-to-run-a-refrigerator-for-24-hours. I run dealectric.com, which earns a commission on some links.
```

## T19. Reply on MacRumors, "Foldable MacBook Screen Extender Q" (evergreen, demand 3 at the time; March 2026; **only if Barry sees it on page 1** for a target query)

- **Where:** https://forums.macrumors.com/threads/foldable-macbook-screen-extender-q.2479264/
- **Account:** macrumors.com login in agent-vault.
- **Steps:** **Precondition:** Barry checks Google and Bing page 1 for "triple screen laptop extender 16 inch 1920x1200" or "best triple screen laptop extender for a 16-inch laptop" (the research could not read result pages: Bing returned cached content, DuckDuckGo a bot check). If the thread is not on page 1, skip. If it is, open the thread (4 replies, last 2026-03-17), paste into the reply editor, do not click 'Post reply'.
- **Rules:** MacRumors Registration Agreement: no "advertising, or the promotion of a product, service, organization, or website, except where explicitly permitted"; the separate Forum Rules page was not reachable. New-account self-links are treated as advertising (see T4). 7.5 months quiet.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
fishingfromakay, two things decide this before the brand does. First, which MacBook your daughter has: a base-chip Air or 14-inch Pro (M1/M2/M3, not Pro/Max) natively supports one external display, so any two- or three-screen extender for it has to be a driver-based one (DisplayLink or the maker's own USB display driver), installed by hand with Screen Recording permission granted. That works, with some pointer lag on the extra screens and no protected video on them; it is how all the clip-on triples get around the limit. Second, FreakinEurekan's weight point: the 16-inch-class triples are 2.6 kg plus and are built for 15–18-inch lids with a rear support leg; on a 13-inch Air they are the wrong product, and the 14-inch-panel units are the ones to look at.

If it is a 16-inch MacBook Pro, the one I'd pick for the panel match is FOPO's S788, three 16-inch 1920 × 1200 IPS panels (same 16:10 shape as the MacBook's screen), 12–18.5-inch fit, PD supply in the box, $499.99 with a 10% code on FOPO's site. FOPO lists macOS 2019+ including M1/M2/M3. If budget matters more than the 16:10 match, the 14-inch 1080p triples run $140–250.

The comparison with the driver and Mac notes: https://dealectric.com/best-triple-screen-laptop-extender-16-inch-1920x1200. Disclosure: I run dealectric.com, which earns a commission on some links there.
```

## T20. Reply on MacRumors, "4k 144hz KVM switch PC/MAC?" (evergreen, demand 3 at the time; March 2025; **only if Barry sees it on page 1** for a target query)

- **Where:** https://forums.macrumors.com/threads/4k-144hz-kvm-switch-pc-mac.2453262/
- **Account:** macrumors.com login in agent-vault.
- **Steps:** **Precondition:** Barry checks Google and Bing page 1 for "KVM for Mac and PC 4K 144Hz" (rank not verified by the research; the thread surfaced third in the search tool's results and our KVM page already cites it). If not on page 1, skip (19 months old). If it is, open the thread (1 reply, 2025-03-25), paste into the reply editor, do not click 'Post reply'.
- **Rules:** as T4 (MacRumors; new-account self-link treated as advertising).
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Late, but the question keeps coming up. Short version: no KVM I can find is proven at 4K144 with a MacBook Pro. DP 1.4 carries 4K120 at 8-bit uncompressed; 4K144 needs DSC negotiated by the Mac, the switch and the monitor, and macOS does not document DSC. Level1Techs rates its DP 1.4 KVM at 4K120 for that reason; UGREEN's DP 1.4 KVM lists 4K144 but has no Mac test; TESmart and Cable Matters claim 4K144 with EDID emulation, also untested on a Mac. Add the Mac-specific problems (windows and Spaces shuffle on every re-handshake, sleep/wake failures, and no KVM charges the laptop) and the cleaner answer is a 4K144-or-better monitor with a built-in KVM: PC on DisplayPort/HDMI 2.1, Mac on the monitor's USB-C (Apple lists the M4/M4 Pro MacBook Pro at 4K240 on one display), monitor input button to swap, the monitor's USB hub following the input. Gigabyte M27UP (4K160, about $299–329, 18 W USB-C so keep the charger) or BenQ PD3226G (4K144 over Thunderbolt 4, $969–1,136). For a USB mic, drives or a 10Gbps SSD that the hub can't take, a $40.99 UGREEN USB-C switch toggles four 10Gbps ports between the two computers with its own button.
Details and each vendor's exact claim: https://dealectric.com/kvm-switch-for-a-mac-and-pc-4k-144hz
I run dealectric.com, which earns a commission on some links.
```

## T21. Answer on Best Buy Q&A, Wasserstein 3-pack, "Will this work with the new Blink Outdoor 4 cameras?" (evergreen, demand 3 at the time, about 2 years old; low priority)

- **Where:** https://www.bestbuy.com/site/questions/wasserstein-solar-panel-for-blink-outdoor-camera-3-pack-white/6433171 (question by Benjammin; one one-word answer "yes")
- **Account:** none in the vault; Barry creates one at https://www.bestbuy.com/identity/newAccount (the Create Account link on bestbuy.com; Claude never creates accounts).
- **Steps:** Open the question, click 'Answer this question', paste the text (plain text), do not click 'Submit'.
- **Rules:** **Removal expected.** Best Buy Q&A terms bar promotional content and external links; answers with URLs are typically removed. The disclosure line is still required by our rule, so expect removal; posting is Barry's call.
- **Blink precondition:** met (commit 4dbceda).
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Yes, with the USB-C converter Wasserstein now includes (the Outdoor 4 is USB-C; this older 3-pack listing is micro-USB, so check the box or buy the current "Outdoor 4 & 3" version). Setup: take the two AA lithium batteries out (they don't recharge), remove the camera's USB-C port cover, plug the panel in; the panel's internal battery runs the camera at night. Blink says the camera loses its weather resistance with the cover off, so the panel plug is the seal. Blink's own alternative is Solaris ($39.99), which clicks onto the camera instead of mounting separately.
Details and prices: https://dealectric.com/solar-panel-for-blink-outdoor-4-without-a-camera-bundle
I run dealectric.com, which earns a commission on some links.
```
