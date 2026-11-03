# Tier 3 outreach research: /best-usb-switch-two-computers-keyboard-mouse-ssd (promote-2026-11-03, step 7b)

Researched 2026-11-03 by a Fable 5.1 subagent (web search, 20 calls, all used; the fetcher). Drafts only: nothing posted,
no account created, no login used. Brief: `growth/focus/fastloop-briefs/outreach-brief.md`. Page facts read from the
built pages `docs/best-usb-switch-two-computers-keyboard-mouse-ssd.html` and `docs/kvm-switch-for-a-mac-and-pc-4k-144hz.html`;
dealectric.com itself was not fetched (no footprint line to add). Second page used where the asker's question is the
Mac+PC monitor one: https://dealectric.com/kvm-switch-for-a-mac-and-pc-4k-144hz.

**Headline.** The live demand is on Level1Techs (the only forum our tools can search newest-first; 9 KVM/USB-switch
threads opened in the last 30 days) and in MacRumors' Mac Accessories subforum (3 switching threads with posts in the last
30 days). One Tier A thread fits the page exactly: a MacRumors poster (Oct 28) whose UGREEN KVM blurs his new 4K ProArt
and who is about to buy "a KVM that handles 4K", where nobody has said "skip the video KVM, switch the monitor's input
and put the peripherals on a USB switch" (draft 2a). One Tier B thread fits the KVM page: Level1Techs, two MacBooks + a
gaming PC on 4K144 monitors, planning a TESmart DKS403-M24 (draft 2b). One Tier A thread is solved in principle but
asks for a cheap 2-port USB sharing switch to cascade (draft 2c, short). The evergreen MacRumors "4k 144hz KVM switch
PC/MAC?" thread is the KVM page's own subject; its Google/Bing rank is unverified (draft 2d, conditional).

Stack Exchange (Super User, Ask Different), Quora, Spiceworks, Lemmy and Reddit could not be read at all this run
(section 4); Reddit is a manual check (section 5). No fresh thread anywhere asks the SSD-sharing question in the page's
title; the fresh questions are keyboard/mouse/webcam + monitor-input ones, which the page also answers.

Counts: Tier A 2 drafted (demand 3, 3), Tier B 1 drafted (demand 3), evergreen 1 drafted conditionally, correction notes 0
(no checkable error found in the two fresh articles), suggestion comments 1 optional (no draft).

## 1. Ranked candidates

Demand: 3 = about to buy / undecided; 2 = owns one, open question, others shopping; 1 = technical only. Tier: A = post in
the last 14 days; B = 15–45 days, unresolved; E = evergreen (older; rank given as seen). Dates read on 2026-11-03;
MacRumors shows weekdays for the last 7 days ("Wednesday" = Oct 28, "Thursday" = Oct 29).

| # | URL | Venue, dates, size | Tier | Demand (quote) | What is missing | Link rules | Action |
|---|---|---|---|---|---|---|---|
| 1 | https://forums.macrumors.com/threads/kvm-for-4k-monitor.2493115/ | MacRumors, Mac Accessories; opened Oct 28, 2026 (av8raaron, newbie), 1 reply (maflynn, Oct 29); views not shown | A | **3**: Mac mini + Windows PC, new ASUS ProArt PA279CV 4K replacing a 1080p Samsung; "the video through the KVM leads to a very blurry image", direct looks "great"; wants a KVM that handles 4K "without distortion/degradation"; old UGREEN KVM "ran fine" at 1080p | maflynn only names another UGREEN 4-port KVM (works on his BenQ EX321UX; Amazon link). Nobody says: the monitor already has two inputs, so run both computers straight in and switch the input; put keyboard/mouse (and anything else) on a USB switch, which carries no video and cannot blur anything; which switch (CM691 $40.99, 10Gbps; or the $23.99 USB 2.0 one for KM only); the USB-A host cable; wireless-receiver caveat. | MacRumors (rules thread 1672419, read via search summary in the esr-25w run; /help/rules/ is 404 for us): self-promotional links belong in signature/profile; established members may link their own site when it answers a specific question; a new account's self-link is treated as advertising. Note the forum itself rewrites Amazon links to its own affiliate tag (maflynn's reply carries one). Expect the link to be removed from a new account; the draft stands without it. | Reply (draft 2a) |
| 2 | https://forum.level1techs.com/t/two-macbooks-gaming-pc-2-3-4k144-monitors-can-this-be-done-with-one-kvm/257041 | Level1Techs, KVM Helpdesk; opened 2026-09-23 (lukka), 4 posts (2 by wendell, same day), 123 views; still open | B (41 days, unresolved: wendell said "no", asker still wants fewer cables) | **3**: planning a TESmart DKS403-M24 KVM + two CalDigit Element 5 hubs for two MacBooks + a 4070 SUPER PC on 2–3 4K144 monitors, wants HDR/VRR/10-bit/4:4:4 and one Thunderbolt cable per Mac; "is there an all-in-one KVM-and-dock?" | wendell covered bandwidth (DisplayLink fakes 144; each Mac needs 2–3 cables; TB "trash" for switching; realistic 4K120 + 4K60 with DSC through a DP KVM). Missing: Apple's own per-chip display caps (M4 Pro: two displays at 4K144 each, so three 4K144 panels from one Mac is out whatever the switch), the DSC/EDID reason 4K144 fails at a KVM with Macs, that TESmart's "EDID emulation 2.0 / 4K144" claim has no independent Mac test, the Mac re-handshake/window-shuffle and no-wake reports, and the alternative that sidesteps the switch for two of the three machines: monitors with built-in KVM (PC on DP/HDMI 2.1, Mac on USB-C) + a USB switch for the peripherals. | Level1Techs FAQ: no spam, no cross-posting; ToS §2 bans "unwanted commercial content designed to drive traffic to third party sites". No affiliate-link rule in the FAQ. Sensitivity: the forum is run by a company that sells KVMs; a disclosed link to a comparison that rates their unit 4K120 is fair but may read as competitive. New accounts are rate-limited (Discourse trust level 0: few links per post). | Reply (draft 2b) |
| 3 | https://forum.level1techs.com/t/need-a-3-way-km-switch/259458 | Level1Techs; opened 2026-10-25 (darkmann), 9 posts, last 2026-10-29, 109 views; solution accepted | A (5 days) but solved in principle | **3**: already runs a UGREEN USB switch for two PCs, adding a mini-PC head-end; L1T store too expensive and "shipping from the US is a hassle"; accepted Agent9's idea of a cheap 2-port USB-A sharing switch (~$30) cascaded into the existing switch: "I think that will be what I use." | Nobody named a model for the cascade switch, nor said USB 2.0 is the right class for keyboard/mouse (and the safer class for a 2.4 GHz receiver: UGREEN itself warns against receivers on USB 3 switches). Our page's cheap rows: UGREEN USB 2.0 2-in-4-out $23.99 (US store) / $16.99 Adorama, Sabrent USB-SW30 $14.99, Plugable USB3-SWITCH2 $19.95. Asker is outside the US, so US prices are a reference only. | Same as #2 | Short reply (draft 2c); Barry decides whether a solved thread is worth it |
| 4 | https://forums.macrumors.com/threads/4k-144hz-kvm-switch-pc-mac.2453262/ | MacRumors, Mac Accessories; opened 2025-03-16 (hchaugen), 1 reply (timmah339, 2025-03-25: Sabrent TB4 KVM, "only charges the active device"); views not shown | E (candidate): surfaced 3rd in the search tool's result set for "KVM Mac and PC 4K 144Hz monitor built-in KVM"; **Google/Bing page-1 rank not verified** (search budget exhausted); our KVM page already cites it as a source | **3** at the time: 4090 PC gaming at 4K/144 + MacBook Pro for office work on one monitor, "I understand it's not possible to connect Mac with USB-C to charge it, so will be HDMI I guess?" | The only reply is a TB4 KVM at 4K120. Missing: why 4K144 breaks at a KVM (DSC/EDID), that no KVM is proven at 4K144 with a Mac, Apple's per-chip caps, and the monitor-with-KVM + USB-switch setup. | Same as #1 | Reply (draft 2d) **only if Barry sees the thread on page 1** for a target query; otherwise skip (19 months old) |
| 5 | https://forums.macrumors.com/threads/best-way-to-share-setup-between-a-mac-mini-and-macbook-pro.2490683/ | MacRumors, Mac Accessories; opened 2026-09-28 (AppleFan), 6 replies, last 2026-10-04; asker never came back | B (30 days) | **2**: Mac mini M4 + MacBook Pro M5 sharing two Studio Displays (Thunderbolt-only, single-host), keyboard, mouse receiver and backup drive hang off the displays; "are docks or KVM switches worth considering?" | Replies: a dock (Ben J.), extension cables (FreakinEurekan, DavidPS: a TB KVM for two 5K displays "isn't worth the money"), Screen Sharing (xraydoc). Our USB switch cannot move his peripherals because they ride the displays' Thunderbolt link, and the displays have no second input. Nothing on our page fixes his case. | Same as #1 | Skip (documented) |
| 6 | https://forums.macrumors.com/threads/m6-mac-mini-and-kvm-switch.2490222/ | MacRumors, Mac mini; opened 2026-09-22 (UnluckyXIII), 9 replies, all Sep 22 | B by date, but settled | **2**: powered UGREEN USB-A KVM + USB-A-to-C data cable ignored on the M6 mini's rear Thunderbolt ports, works on the front USB-C ports; "why do the rear ports reject the KVM?" Time89 suggested a RayCue SmartDock + Teetek HDMI KVM (~$30). Asker kept the KVM on a front port with a ribbon cable. | Nobody explained the rear-port behaviour and neither can our page (open concern: USB-A vs USB-C host cables; this is the mirror case, a USB-A switch into a Thunderbolt port). Useful evidence for the page's open concern, not a reply target. | Same as #1 | Skip; note for the page's open concern |
| 7 | https://forum.level1techs.com/t/usb-3-1-gen-2-10-gbps-cables-a-to-c-or-c-to-c-3m-long-or-longer/258694 | Level1Techs; opened 2026-10-15 (ICPete), 4 posts (3 his), 78 views | B (19 days) | **1–2**: KVM arriving, computers 6 ft away, wants 10 ft+ 10Gbps A-to-C cables (Club3D C-to-C 16 ft $54, OkyLink active 15 ft $38, passive 10 ft $16); solved his own problem by keeping the KVM near the PCs and running a USB keypad to the desk. | Our page's only cable fact is UGREEN's "keep the uplink within 0.8 m or speed drops", which supports "passive 10Gbps beyond ~1 m is a gamble, buy the active one", but he no longer needs it. | Same as #2 | Skip |
| 8 | https://forum.level1techs.com/t/dell-monitor-goes-black-after-switching-hdmi-2-1-kvm-inputs/258869 | Level1Techs; opened 2026-10-17 (Austin_Oliver, MacBook Pro M5 + MCT T6 dock + L1 HDMI 2.1 KVM, Dell U2718Q), staff reply Oct 18 (pmset sleep settings) | B | **1**: owner troubleshooting; no purchase | Our KVM page records the Mac no-wake/re-handshake pattern but has no fix beyond "turn off automatically rearrange Spaces"; Level1_Amber already gave the sleep workaround. | Same as #2 | Skip |
| 9 | https://forum.level1techs.com/t/flickering-with-hdmi-2-1-edid-kvm-how-to-stop-it/257187 | Level1Techs; opened 2026-09-27 (beowulf), 6 posts, last 2026-10-05 (MSwanson: one PC + two Mac Studios, daily blackouts), 167 views | B | **1** | Cable/interference advice from wendell; nothing our page adds. | Same as #2 | Skip |
| 10 | https://www.displayninja.com/best-monitors-with-built-in-kvm-switch/ | DisplayNinja article "Best Monitors With Built-in KVM Switch [2026 Guide]", published/updated 2026-10-31; 5 comments (not readable: loaded by script) | fresh article (<60 days) | n/a (readers choosing a KVM monitor; PD3226G listed as the 4K 144Hz pick at $900) | Says nothing about Macs or about 4K144 through a KVM, so no error to correct. A suggestion comment ("for a Mac + PC at 4K144 the monitor's KVM plus a USB switch is the setup that works, here is why") fits the brief's comment-section venue. | About page: site uses referral links itself; no comment or link policy stated; comments appear moderated. | Optional suggestion comment (no draft; Barry can lift the first paragraph of 2d) |
| 11 | https://windowsforum.com/news/mouse-without-borders-vs-usb-keyboard-mouse-switches-best-options-for-multi-pc-control.449850/ | WindowsForum "news" roundup of a TechRadar column, 2026-10-24; 0 replies, 295 views; structured data labels it "trainedAlgorithmicMedia" (AI-generated); replies need login | fresh article | n/a | Names j5create Wormhole cables ($14.99–79.99), Asuizo Crossys, LoopMotion; no speeds, no 10Gbps or external-drive claims, so nothing checkable to correct. | Forum account needed to reply; no link policy read | Skip |

Venue activity (how counted, 2026-11-03):
- **Level1Techs**: Discourse search `usb switch order:latest` and `mac kvm order:latest` (`/search.json`). KVM- or USB-switch
  topics created Oct 4–Nov 3: 260031, 259726, 259458, 259135, 259006, 258999, 258869, 258813, 258694 = **9 in 30 days**,
  plus the KVM FAQ megathread (post Oct 30). Most are Level1 KVM owner support; two (259458, 258694) are generic.
- **MacRumors Mac Accessories** (pages 1–2 of 902, newest last post first): switching threads with a post in the last 30
  days: "KVM for 4k monitor" (Oct 28–29), "Two computers and one Studio Display?" (post #575, Oct 26: macOS 27.2 breaks
  a Cable Matters 20Gbps switch on an M4 Pro mini, no Windows PC, troubleshooting only), "Best way to share setup…" (Oct 4)
  = **3**. **Mac mini subforum**: "M6 Mac Mini and KVM Switch" (Sep 22) is the only one on page 1 (back to Sep 9) = 0 in 30 days.
  MacBook Pro subforum page 1 (Oct 18–Nov 3): none.
- **Mac Power Users Talk** (`/search.json?q=kvm order:latest`): 0 new KVM topics in 30 days; built-in KVM mentioned in
  "What are people using as Mac monitors in 2026?" (Sep 19–Oct 28, 37 posts; asker bought a Studio Display Oct 1, nobody
  undecided). Rules: "nor should you use affiliate links to Amazon, etc. when sharing products"; sharing your own work OK
  "just be mindful not to overdo it".
- **Hacker News** (Algolia `search_by_date`, "usb switch" keyboard mouse): 3 comments in 2026 (Sep 13 in the JetKVM Mini
  thread, May 18, Apr 18), no story; dtech asked there whether "good non-IP KVMs still exist" (USB-C + 2 HDMI/DP). HN
  threads are dead after 2 days; skip.
- **Linus Tech Tips forum** (site search, newest): no USB-switch topic since "KVM (no video required) Switch for 8 TVs"
  (Jul 27, year not shown; 8 Tizen TVs, not our case). Dormant on this topic.
- **Tom's Hardware forums**: search page needs a form submission; the web search surfaced only 2014 and 2022 threads;
  the 2022 one (3784451) returned HTTP 429. Not countable this run.

## 2. Drafts

Each ends with the page link and the disclosure, per the brief. Facts are from the two built pages; the one sentence
that is not (marked) is general and Barry can cut it. Prices are "on 2026-11-03".

### 2a. MacRumors "KVM for 4k monitor" (Tier A, demand 3) — USB switch page

> The blur is the KVM, not the monitor: your old UGREEN box was fine at 1080p because that is what it was built to pass, and
> a 4K signal squeezed through it comes out resampled. [general, not from the page: a KVM rated for 1080p60 or 4K30 will
> negotiate a lower mode and the monitor scales it up.] The cheap fix is to stop routing video through a switch at all. The
> PA279CV has more than one input, so plug the Mac mini into one (HDMI or USB-C) and the PC into the other (DisplayPort or
> HDMI), and let the monitor's input button do the "V" part; direct cable, nothing to degrade.
>
> For the K and M, a USB switch (no video) moves the keyboard, mouse, webcam, or an external drive between the two
> computers with one button. Two kinds worth looking at:
> - If you only need keyboard and mouse, a USB 2.0 switch is enough: UGREEN's 2-in-4-out USB 2.0 switch is $23.99 on
>   UGREEN's US store ($16.99 at Adorama), 2 USB-A uplinks, one button. USB 2.0 is also the safer class for a Logitech or
>   other 2.4 GHz receiver; UGREEN itself warns against putting receivers on USB 3 switches because of interference.
> - If you also want to move a fast SSD or a USB-C device, UGREEN's USB-C switch (CM691) is $40.99: two USB-C uplinks
>   with 0.8 m cables and a wired remote in the box, four 10Gbps USB 3.2 Gen 2 ports (3× A, 1× C), bus-powered, two-year
>   warranty. If your PC only has USB-A, you need a USB-A-to-C data cable (not included) and UGREEN says to keep it under
>   0.8 m. Cable Matters' 201160 is the other 10Gbps option ($51–66 at resellers); the ATEN US3324, IOGEAR GUS432, Sabrent
>   USB-SW30 and Plugable USB3-SWITCH2 are 5Gbps.
>
> Two habits with any USB switch: eject a drive before you press the button (switching is electrically the same as pulling
> the plug; Plugable's and ATEN's own support pages say so), and expect each computer to re-enumerate the devices on each
> switch, which takes a second or two.
>
> Also check the PA279CV's manual for a USB-C upstream: if the monitor's USB hub follows the active input, the monitor is
> the KVM and you may not need a separate switch for the keyboard and mouse. [I could not verify this for the PA279CV.]
>
> I compared the USB switches here, with the cables-in-box, power and speed for each:
> https://dealectric.com/best-usb-switch-two-computers-keyboard-mouse-ssd
> I run dealectric.com, which earns a commission on some links.

### 2b. Level1Techs "Two MacBooks + gaming PC, 2-3 4K144 monitors" (Tier B, demand 3) — KVM page

> Adding to what wendell said about bandwidth, three things that will bite before the KVM does:
>
> 1. Apple's own caps. Apple's external-display page lists the M4 and M4 Pro MacBook Pro at one display up to 4K240 or two
>    displays at 4K144 each; three 4K144 panels from one Mac is out on those chips regardless of the switch. (Apple's page
>    does not yet cover the M5 Pro you mention; check it before buying anything.) Thunderbolt 4 carries DisplayPort 1.4,
>    Thunderbolt 5 carries DP 2.1.
> 2. DSC. 4K144 at 10-bit does not fit DP 1.4 uncompressed (4K120 8-bit does), so the Mac, the KVM and the monitor must
>    all negotiate Display Stream Compression, and macOS does not document DSC. Level1Techs rates its own DP 1.4 KVM at
>    4K120 for exactly this reason, and a member's LG 27GP950 pair held 4K144 only with the KVM removed. TESmart's
>    DKS403-class units and Cable Matters' DP 1.4 KVM both claim 4K144 with EDID emulation 2.0 / a DSC-capable host; I found
>    no independent test of either with a Mac. HDMI 2.1 carries 4K144 without DSC, but the HDMI 2.1 KVMs pass one HDMI link
>    per M-series Mac.
> 3. Macs and re-handshakes. A KVM without working monitor emulation makes macOS see a new display on every switch:
>    windows and Spaces shuffle (turn off "automatically rearrange Spaces based on most recent use") and owners of the UGREEN
>    DP KVMs report the Mac not waking until the lid is closed and reopened. No KVM in this class charges the laptop, so
>    the Element 5 docks stay in the chain either way.
>
> The setup that avoids the switch for two of your three machines: monitors with a built-in KVM. Each takes the PC on
> DisplayPort/HDMI 2.1 and one Mac on USB-C (USB-C-to-DP 1.4 or Thunderbolt cable), its input button swaps machines, and
> its USB hub follows the input. Gigabyte's M27UP does 4K160 for about $299–329 (USB-C power is only 18 W, keep the Mac
> charger); BenQ's PD3226G does 4K144 over Thunderbolt 4 at $969–1,136. That covers one Mac + PC per monitor; the second
> Mac still needs either a KVM or its own input. For the peripherals a plain USB switch with a button (UGREEN's USB-C
> switch, $40.99, four 10Gbps ports, two USB-C uplinks) is cheaper and simpler than routing USB through the KVM.
>
> What I found on each KVM's 4K144 claim, Apple's limits and the Mac reports is here:
> https://dealectric.com/kvm-switch-for-a-mac-and-pc-4k-144hz
> I run dealectric.com, which earns a commission on some links.

### 2c. Level1Techs "Need a >=3-way KM switch" (Tier A, demand 3, solved in principle) — USB switch page, short

> For the cascade switch Agent9 suggested: keyboard and mouse only need USB 2.0, and USB 2.0 is the better class if the
> mouse is wireless (UGREEN warns against 2.4 GHz receivers on USB 3 switches because of interference). Cheap 2-host
> options I have prices for, US store prices so only a reference for you: UGREEN's 2-in-4-out USB 2.0 switch, $23.99 on
> UGREEN's US store / $16.99 at Adorama, 2 USB-A uplinks, one button; Sabrent USB-SW30, $14.99, two USB-B uplinks and a
> single USB-A device port (one port is all the cascade needs); Plugable USB3-SWITCH2, $19.95, same shape at 5Gbps. The
> UGREEN 10Gbps USB-C switch you already have is the one in the same family that matters if a drive ever rides along.
> Comparison with the cables-in-box and power for each: https://dealectric.com/best-usb-switch-two-computers-keyboard-mouse-ssd
> I run dealectric.com, which earns a commission on some links.

### 2d. MacRumors "4k 144hz KVM switch PC/MAC?" (evergreen, conditional on page-1 rank) — KVM page

> Late, but the question keeps coming up. Short version: no KVM I can find is proven at 4K144 with a MacBook Pro. DP 1.4
> carries 4K120 at 8-bit uncompressed; 4K144 needs DSC negotiated by the Mac, the switch and the monitor, and macOS does
> not document DSC. Level1Techs rates its DP 1.4 KVM at 4K120 for that reason; UGREEN's DP 1.4 KVM lists 4K144 but has no
> Mac test; TESmart and Cable Matters claim 4K144 with EDID emulation, also untested on a Mac. Add the Mac-specific
> problems (windows and Spaces shuffle on every re-handshake, sleep/wake failures, and no KVM charges the laptop) and the
> cleaner answer is a 4K144-or-better monitor with a built-in KVM: PC on DisplayPort/HDMI 2.1, Mac on the monitor's USB-C
> (Apple lists the M4/M4 Pro MacBook Pro at 4K240 on one display), monitor input button to swap, the monitor's USB hub
> following the input. Gigabyte M27UP (4K160, about $299–329, 18 W USB-C so keep the charger) or BenQ PD3226G (4K144 over
> Thunderbolt 4, $969–1,136). For a USB mic, drives or a 10Gbps SSD that the hub can't take, a $40.99 UGREEN USB-C switch
> toggles four 10Gbps ports between the two computers with its own button.
> Details and each vendor's exact claim: https://dealectric.com/kvm-switch-for-a-mac-and-pc-4k-144hz
> I run dealectric.com, which earns a commission on some links.

## 3. Checked and rejected (so the next run skips them)

Stale (last post > 45 days, not seen on page 1 for a target query):
- https://forums.macrumors.com/threads/seeking-advice-dual-monitor-setup-for-mac-mini-m4-dell-laptop-need-split-screen-dual-mode-flexibility.2474701/ — Dec 14–23, 2025; demand 3 at the time (Mac mini M4 + Dell Latitude, move mouse, keyboard, external drive, Focusrite 2i2; wants split-screen mode). zarmanto already said don't switch a drive mid-transfer and use the monitor's input swap. The best-fit old thread for this page; 10 months quiet.
- https://forum.level1techs.com/t/struggling-to-find-a-solution-to-use-my-work-laptop-with-my-own-rigs-peripherals-when-at-home/255192 — Sep 6–12, 2026 (58 days), HP EliteBook + 3090 Ti rig, three monitors; havocx and shapesinaframe already gave "USB switch + monitor input switching", no model named. Exactly target query 2; re-check if it gets a new post.
- https://forum.level1techs.com/t/levelonetechs-k-v-m-something-else-or-just-find-a-quality-u-s-b-switch/255280 — Sep 8–10, 2026; 1440p180 + two 1080p, work laptop without admin; Jeffrey1910 answered; no Mac.
- https://forum.level1techs.com/t/quickly-switching-between-mac-and-linux-on-one-monitor/255866 — Sep 12, 2026; wants instant 4K240 switching, rejected KVMs and USB switches already; mihawk90 explained the handshake. Nothing to add.
- https://forum.level1techs.com/t/m3-ultra-mac-studio-5120x2160-120hz-quad-dp1-4-kvm-compatibility/254031 — Aug 18, 2026, 1 post, unanswered, 77 days.
- https://forum.level1techs.com/t/daisy-chaining-to-a-portable-monitor-vs-a-separate-kvm-switch/253341 (and duplicate 253048) — Jul 2026, 1 post each, "monitor's built-in KVM or a separate switch for dual-monitor dual-PC?", unanswered, 95 days.
- https://forums.macrumors.com/threads/how-do-i-get-my-mac-studio-with-pro-display-and-w11-pc-to-share-screens-and-peripherals.2448630/ — Feb 2025; Studio Display (one input), decided to swap cables.
- https://forums.macrumors.com/threads/what-are-people-using-as-mac-monitors-in-2026/ (talk.macpowerusers.com/t/46982) — Sep 19–Oct 28, 2026; two posts mention built-in KVMs (Asus ProArt 5K, Dell 40" UltraSharp); nobody undecided.
- https://forum.level1techs.com/t/buying-a-4-port-km-switch-setup-for-two-laptops/224239 — Jan–Feb 2025, two MacBook Pros; answered by vagrantin.
- https://www.elevenforum.com/t/sharing-a-mouse-keyboard-with-2-pcs.29158/ — Oct 2024; asker chose a USB switch for a Unifying receiver; thread dead.
- https://www.bleepingcomputer.com/forums/t/757738/shifting-between-work-and-personal-laptop — Sep 2021; UGREEN and Plugable switches already recommended.
- https://www.keebtalk.com/t/anyone-recommend-a-kvm-switch/14273 — May 2021.
- https://forums.tomshardware.com/threads/usb-switch-for-keyboard-and-mouse-on-2-computers.1771702/ — 2014. Level1Techs 198473 (2023, closed), 89349, 105225; AnandTech 2451884, 2583060, 2387887; hardforum — all pre-2025.
- HN: "Show HN: Multi-monitor KVM using just a USB switch" (Feb 2024, 397 points) and the JetKVM Mini thread (~Sep 13, 2026) — read-only history now.
- Reddit snapshot (reddit.sentinel-team.org) r/homelab "Mac + PC sharing one monitor, one K/M — no KVM required", ~Nov 23, 2025: HawkingRadiator512 "couldn't find a USB switch that supports both USB-C and USB-A" hosts — the CM691 (USB-C uplinks, USB-A host via A-to-C cable) is that switch; a year old, listed in section 5 for a manual look.

No purchase in view (demand 1) or settled: table rows 6–9; https://forum.level1techs.com/t/kvm-multiple-power-sources-usb-dc-usb-backfeeding-power/259726 (Oct 28–Nov 2, L1 KVM backfeed, staff handling); https://forum.level1techs.com/t/usb-instability-only-on-linux-zorin-os-18/260031 (Nov 3, L1 KVM + Zorin, Mac mini fine); https://forum.level1techs.com/t/usw-km314-switch-usb-audio-not-starting-properly/259006 (L1 KM switch audio, RMA); https://forum.level1techs.com/t/usb-c-to-displayport/258813 (cable through L1 KVM); Dell community U2722DE (2023, closed) and U2723QE KVM threads; Apple Community 255938539 (Jan–Feb 2025, TESmart firmware fix, closed).

Wrong size or shape: Level1Techs 259458 wants three computers (our switch does two; drafted only for the cascade part); LTT "KVM (no video) for 8 TVs"; MacRumors 2490683 (Studio Displays, no second input).

Articles: windowsforum.com (Oct 24, AI roundup, no checkable error, 0 replies); displayninja.com (Oct 31, no error; optional comment); budgetloadout.com "Best USB Switch in 2026" returned HTTP 429 (not read; the search summary says it warns USB 2.0 ports throttle drives and that devices disconnect during the swap, both consistent with our page); yomotherboard.com Q&A (Aug 17–21, 2026, "share one keyboard and mouse between my PC and work laptop", LG C2 TV; one generic answer; site shows signs of templated content, 78 days old; comments open) — skip unless it ranks.

Search-engine ranks: none verified this run. The search tool's result sets are not Google/Bing SERPs, and the 20-call budget went to venue discovery. For the evergreen rule, Barry (or the next run, in the pane) should check Google and Bing page 1 for "KVM for Mac and PC 4K 144Hz" (is forums.macrumors.com/…2453262 there?) and for "USB switch two computers keyboard mouse SSD".

## 4. Could not verify / blocked

- **Stack Exchange** (superuser.com, apple.stackexchange.com, api.stackexchange.com): "unable to fetch" for all three; the web search returned no SE results for four site-restricted queries. Rule to carry (brief): an answer linking your own site must disclose the affiliation in the answer body. Needs a manual search in the pane: `site:superuser.com "USB switch" keyboard mouse` and `site:apple.stackexchange.com KVM mac windows` sorted newest.
- **Quora**: search page HTTP 403; site-restricted web search returned nothing. Rule from earlier runs: affiliate links banned; a self-promotional link allowed inside a complete answer with the affiliation disclosed; posting needs a login (Google as barrryyao).
- **Spiceworks**: fetch refused. **Lemmy** (lemmy.world, lemm.ee): certificate error / instance gone. **Reddit**: blocked; one 2025 post read via a snapshot mirror.
- **Tom's Hardware** site search needs a form; thread 3784451 HTTP 429. **MacRumors** rules page 404 (rule text reused from the esr-25w run). **DisplayNinja** comments not readable (script-loaded).
- Google/Bing page-1 ranks: not checked (section 3).
- The one general claim in draft 2a (1080p-class KVMs negotiating a lower mode) is not on our page; cut it if unwanted.

## 5. Manual checks (Reddit; blocked for our tools)

Run in the pane or Personal Chrome, newest first, last month: `https://www.reddit.com/r/<sub>/search/?q=<query>&sort=new&restrict_sr=1&t=month`
- r/battlestations: `USB switch`; `KVM mac pc`
- r/macsetups: `KVM`; `USB switch`; `windows pc same monitor`
- r/sysadmin: `USB switch work laptop personal`; `KVM home office`
- r/buildapc: `share keyboard mouse laptop desktop`; `USB switch 10Gbps`
- r/Monitors: `built-in KVM mac`; `KVM 4K 144hz mac`
- r/mac and r/macmini: `KVM`; `USB switch`
- r/homelab: open https://www.reddit.com/comments/1tciqfi (the Nov 2025 "no KVM required" post; HawkingRadiator512's USB-C + USB-A host question may still be unanswered)
- r/WorkFromHome, r/homeoffice: `KVM work laptop`
Check each subreddit's self-promotion rule before posting; most require disclosure and ban affiliate links outright.
