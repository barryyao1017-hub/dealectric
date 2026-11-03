# Tier 3 outreach: /best-nas-under-500-for-docker-immich-home-assistant and /best-nas-for-immich-iphone-photo-backup (step 7b, 2026-11-03)

Research only; nothing posted. Pages read from `docs/` (both published 2026-11-03, prices checked 2026-11-03). Search window:
threads with activity since about 2026-09-20. 24 WebSearch calls were allowed; 17 used, plus direct fetches of each forum's own
newest-first search or thread list (Discourse `search.json` for Home Assistant, Level1Techs and TrueNAS; GitHub Discussions
sorted by date; XenForo thread lists for ServeTheHome and SNBForums; Invision search for Unraid).

**Bottom line: one tier A thread with demand 3 (Level1Techs, opened yesterday, still open as of 19:34 UTC today), two tier B
threads with demand 3 and no replies at all (one on the Home Assistant community, one on Level1Techs), and one tier B thread
with demand 2–3 (Level1Techs). Four drafts below.** The purchase-decision traffic this month is on Level1Techs' Hardware Hub
(12 "which NAS / small server should I buy" threads since Oct 4), not on the NAS-specialist forums: SNBForums' NAS Buying Advice
has had no new thread since March 2026 and ServeTheHome's NAS subforum one since Oct 4. Immich's own GitHub Discussions carry
setup questions, not purchase questions (last hardware-choice thread Nov 2025). Nobody in any thread found is asking the exact
target query ("NAS under $500 for Immich/Docker"); the four candidates are people choosing a first NAS or home server whose
stated needs (family photos, Immich, Home Assistant, Docker, VPN, a Linux sandbox) our page answers.

Price note for Barry: UGREEN's US store today shows the DXP2800 at $389.99 ("Regular price $439.99", Halloween Sale banner),
matching the page. A games.gg article (2026-09-29) quoted $346.99 for an Oct 6–9 sale; that sale is over. The DH4300 Plus,
which two of the candidates are leaning toward, is $399.99 on the same store today, so it is now *more* than the DXP2800.

## 1. Candidates

Sorted by demand, then freshness, then venue activity. Dates are UTC.

| # | URL | Venue | Opened / last post | Tier | Demand (quote) | What's missing | Link rules | Action |
|---|---|---|---|---|---|---|---|---|
| 1 | https://forum.level1techs.com/t/homelab-and-or-nas-entry-point-advice-request/259960 | Level1Techs, Hardware Hub; 11 posts, 126 views | 2026-11-02 / 2026-11-03 19:34 | A | **3**. First NAS, undecided: "a NAS for family use to replace Google Drive", father is a photographer, OP does drone photography/mapping, wants a VPN, OpenDroneMap and a Linux sandbox; asks "whether a prebuilt NAS like the UGREEN DH4300 Plus is enough, or whether a custom build is better"; post 8: "leaning more towards a UGreen DH4300 or DH4800". | Nobody has said the DH4300/DH4800 are ARM boxes, or what that costs him (amd64-only Docker images, no x86 VMs for his Linux sandbox); aar.l1t (post 11) said "amd64 over arm64" in general without naming the models. Nobody priced a sub-$500 x86 unit: Agent9's DXP4800 Plus is over budget, the rest is DIY TrueNAS (Glitch001, BoGs), used Dell OptiPlex (xyz, jdrch), QNAP-with-TrueNAS (redocbew). Nobody has told him ODM needs 16 GB+ RAM (64 GB at 1,500 images) and belongs on his desktop, not on any NAS he can afford. xyz's off-site backup advice (Duplicacy + B2) and Agent9's UPS advice are already given: not repeated. | Guidelines: "Don't post spam"; no affiliate or self-promotion rule found. Discourse default link limits for a new account (not verified for this site). | Reply (draft 2a, page: docker/HA) |
| 2 | https://community.home-assistant.io/t/home-server-mini-pc-3-nvme-ssds-2-5-gbe-zigbee-matter-thread/1026929 | Home Assistant Community; 1 post, 0 replies, 89 views | 2026-09-30 / 2026-09-30 | B (34 days, unanswered) | **3**: "What do you recommend I buy to suit this project?" One box for Home Assistant (Zigbee/Tuya + many brands, Matter/Thread later), Immich or Jellyfin for photos and media, ad blocking, several days of camera footage; wants three NVMe SSDs (OS, media/docs, footage), 2.5GbE; already owns a Samsung 990 Pro 1 TB. | Everything: no reply in five weeks. The question is "mini PC", but two of the units on our page are the direct answers (Beelink ME mini for NVMe-only, DXP2800 if he wants drive bays and an appliance OS), plus the RAM arithmetic for Immich + HAOS and the Zigbee/Thread passthrough rule. | Guidelines have no link rule; ToS §2 bans "unwanted commercial content designed to drive traffic to third party sites". Disclosure plus a full answer is the defence; Barry decides. | Reply (draft 2b, page: docker/HA) |
| 3 | https://forum.level1techs.com/t/extreme-noob-ugreen-nas-setup/258288 | Level1Techs, Hardware Hub; 1 post, 0 replies, 74 views | 2026-10-10 / 2026-10-10 | B (24 days, unanswered) | **3**, but with a constraint that works against our pick: considering the "Ugreen DH4300 Plus NAS", asks "whether better NAS options exist", whether Tailscale is safe, whether UGOS is good, how to give relatives read-only access from other states and countries; "I don't trust Intel chips" (wants ARM). | Everything: no reply. Honest answer favours the box he picked for the use he describes; the DXP2800 only matters if he later wants Docker/VMs. Low conversion expected; included because the question is open and ours is the only page that compares the two UGREEN lines. | As #1 | Reply (draft 2c, page: iPhone/Immich for the Tailscale section, or docker/HA) — Barry's call whether it is worth posting |
| 4 | https://forum.level1techs.com/t/advice-needed-aging-hardware/258714 | Level1Techs, Hardware Hub; 9 posts, 164 views | 2026-10-16 / 2026-10-16 | B (18 days, unresolved) | **2–3**: budget "under $1,000"; "I need an off ramp for the NAS" (Core 2 Quad FreeNAS 11.1, six drives, ~7 TB used, failing boot thumb drive); wants Plex or Jellyfin, a NAS, "some virtual machines for learning"; leaning toward turning the old gaming rig into the lab. | purkkaviritys covered "old hardware is too slow, 16 GB minimum, an 8 TB external to hold the data"; Agent9 covered 2.5GbE. Nobody has offered a purpose-built small NAS as the off-ramp (2 bays hold 7 TB in a mirror; VM app for the learning VMs; ~5 W idle vs a Core 2 Quad), nor how to move 7 TB off FreeNAS safely. | As #1 | Reply (draft 2d, page: docker/HA) |

Evergreen (page 1 for a target query): none verified. The WebSearch tool is not Google; its page-1 results for "best NAS under $500
for Docker and Immich" and "NAS for Immich iPhone photo backup" contained no forum thread we can read: two ask.nascompares.com
threads (tid 11836, 12015) sit behind a Cloudflare bot check our tools cannot pass, the rest are Reddit mirrors and affiliate
roundups. Barry can check those two by hand (see §4). Google and Bing ranks were not checked.

Venue activity, counted this run:
- Level1Techs Hardware Hub: `search.json` for "NAS recommend" since Oct 4 returned 25 topics; 12 are someone choosing a NAS or
  small server to buy (259960, 258893, 258714, 258692, 258541, 258466, 258288, 258132, 254435 and three older build threads).
  The most active buying venue found.
- Home Assistant Community: "NAS #hardware" since Oct 4 → 2 topics (1 buying: 1027472, already ordered); "immich" since Sep 20 →
  15 topics, 1 buying (1026929). Huge forum, little NAS-buying traffic.
- ServeTheHome, NAS Systems subforum (id 39, 339 threads): 1 thread started since Oct 4 (ARM SBC, Oct 27). Slow.
- SNBForums, NAS Buying Advice: newest thread Mar 25, 2026; General NAS Discussion: newest Aug 29, 2026. Dormant.
- Immich GitHub Discussions: 25 newest (since Aug 30) are features and setup; "hardware recommend" sort by date: last hardware
  question #23684, Nov 2025. "ugreen": 2 threads since Sep 20, both setup/backup.
- TrueNAS forums: "immich NAS hardware" since Sep 20 → 0 results. Unraid forums: newest 25 posts for "immich nas buy" are
  support and UGREEN plugin threads (DXP units running Unraid; relevant to the open concern, not to a purchase).

## 2. Drafts

Every fact below is from the two built pages unless marked [verified this run] (fetched today) or [not on page]. Barry reviews
and decides.

### 2a. Level1Techs 259960, Dragonmaster150 (page: docker/HA)

> Two things nobody's said yet, because they decide between the two paths you're weighing.
>
> **1. The DH4300 Plus and DH4800 are ARM boxes (8-core A76+A55, 8 GB LPDDR4X).** That's fine for "a Google Drive replacement for the family" over SMB and a Tailscale VPN. It bites on your other two goals: Docker on ARM runs only arm64 images, so a chunk of the self-hosted catalogue (and anything you'd want to try "to learn") either has no image or runs under emulation, and there are no x86 VMs for a Linux sandbox. aar.l1t's "amd64 over arm64" point is this, concretely. UGREEN's Intel line gives you both: the 2-bay DXP2800 is an N100 with 8 GB DDR5 (one SO-DIMM slot, 16 GB max), two M.2 slots, 2.5GbE, Docker with Compose projects plus a VM app in UGOS, about 5 W idle, two-year warranty, $389.99 diskless on UGREEN's US store today. The DH4300 Plus is $399.99 on the same store today, so right now the ARM box costs *more* than the x86 one. The 4-bay DXP4800 Plus Agent9 runs is the same idea with two more bays and 10GbE; it's over $500.
>
> **2. OpenDroneMap does not belong on any NAS you'd buy at this price.** ODM's own docs: 4 GB RAM minimum for ~40 images, 16 GB recommended, 64 GB at 1,500 images, 256 GB at 5,000. Run it on your desktop (or a used OptiPlex as jdrch says), keep the datasets on the NAS over 2.5GbE. That also answers "prebuilt vs custom": the NAS only has to be a reliable disk box with Docker; the heavy compute goes elsewhere.
>
> For your dad's photos, the thing you'll end up running is Immich (self-hosted Google Photos: phone backup, face search). It wants 6 GB RAM minimum, 8 GB recommended, and an x86-64 CPU for its machine-learning container (you can turn ML off or run it on another machine). On the DXP2800 put the Docker pool on an M.2 SSD so Immich's database and thumbnails aren't on spinning disks; if you also want Home Assistant OS as a VM later, it takes 2 GB more, so plan the 16 GB SO-DIMM. 2 bays vs 4: two 8–12 TB drives in a mirror hold a lot of RAW; the 4-bay only matters if drone mapping datasets grow past that. Drives will cost as much as the box in 2026, as Glitch001 said; xyz's Duplicacy-to-B2 advice is the other half of the setup.
>
> Caveat on UGREEN generally: UGOS is a locked-down Debian (no apt), and the brand's stance on third-party OSes (people run TrueNAS or Unraid on DXP units, see the Unraid forum plugins) isn't official. If you want to learn Linux properly, an N100 mini PC with Proxmox teaches more for less, but you have data to protect, so I'd take the appliance for the family's copy and learn on the OptiPlex.
>
> I wrote up the under-$500 comparison (DXP2800 vs Synology DS225+, TerraMaster F2-425 Plus, Asustor, QNAP, the ARM DH2300 and the Beelink ME mini) here: https://dealectric.com/best-nas-under-500-for-docker-immich-home-assistant
> I run dealectric.com, which earns a commission on some links.

Facts marked [verified this run]: DH4300 Plus CPU/RAM/price $399.99 and DXP2800 $389.99 (ai.ugreen.com today); ODM RAM table
(docs.opendronemap.org). [Not on page]: that the DH4300 Plus lacks Docker or VMs: UGREEN's page is silent and I could not verify
it, so the draft argues only from ARM (arm64-only images, no x86 VMs), which is true regardless. DXP4800 Plus price "over $500"
is from Slickdeals listings ($534 Mar 2026, $559.99), not verified on UGREEN's store today.

### 2b. Home Assistant Community 1026929, Dennver (page: docker/HA)

> Nobody answered, so here's the shape of the decision. Your list is really two machines' worth of jobs (Home Assistant + Zigbee/Thread radios, and Immich/Jellyfin + several days of camera footage), and the box depends on whether you insist on NVMe-only.
>
> **If you want exactly "3 NVMe + 2.5GbE" and nothing spinning:** the Beelink ME mini is the obvious fit: Intel N150, 12 GB LPDDR5 (soldered, not upgradable), six M.2 slots, no SATA, two 2.5GbE ports, about 8 W idle, $209 barebone at launch. It ships with no NAS software, so it's a Proxmox box: Home Assistant OS in a VM (HAOS wants 2 GB RAM, 2 vCPUs, UEFI, a bridged NIC), Immich and Jellyfin in Docker in an LXC or small VM. The 12 GB ceiling is the catch: Immich wants 8 GB recommended (6 minimum) with its machine-learning container on, HAOS takes 2, and you still want headroom for the camera recorder. It works if you run Immich with ML off or on a schedule.
>
> **If you'd rather have an appliance with drive bays (footage and media on HDDs, apps on SSD):** the UGREEN DXP2800, $389.99 diskless: Intel N100, 8 GB DDR5 in one SO-DIMM slot (16 GB max), two M.2 slots plus two 3.5" bays, 2.5GbE, UGOS with a Docker app (Compose projects) and a VM app; owners run Home Assistant OS as a VM on it, though one DXP2800 owner reported the VM getting no IP address with no clear fix in that thread. About 5 W idle hibernating, 16 W active. With the 16 GB upgrade, Immich (ML on) + HAOS + Jellyfin fit; put the Docker pool on an M.2 so Immich's Postgres and thumbnails never sit on the HDDs (Immich says never on a network share).
>
> Things that are the same on either box:
> - **Zigbee / Thread sticks must be passed through by hand** to the VM (or container) on every platform. Plan a USB extension so the radio isn't next to the chassis.
> - **Home Assistant Container has no add-ons**, so if you go the container route you run the Matter server, Zigbee2MQTT etc. as separate containers yourself; HAOS in a VM gives you the add-on store.
> - **Immich on iPhone** backs up only when iOS lets it (Background App Refresh on, open the app now and then); first upload in the foreground. The first ML pass over a big library on an N100/N150 runs hours to days (one owner: ~300 photos/hour with ML on, ~5,000 with it off), so import first, let faces run after.
> - **Remote access:** Tailscale on phone and box (no open port), or a domain + HTTPS reverse proxy; never forward Immich's port 2283 bare.
> - **Camera footage** is continuous writes; on the Beelink that's NVMe endurance you're spending, on the DXP2800 it's a cheap HDD. That's the strongest argument for the second box if the cameras matter.
>
> My pick for your list: the DXP2800 with a 16 GB SO-DIMM and your 990 Pro in one M.2 slot for the app pool, footage on an HDD. If you really want all-flash and you're happy in Proxmox, the ME mini and accept the RAM limit. Comparison table with the alternatives (Synology DS225+ at 2 GB, TerraMaster F2-425 Plus, the ARM boxes that can't run x86 containers): https://dealectric.com/best-nas-under-500-for-docker-immich-home-assistant
> I run dealectric.com, which earns a commission on some links.

[Not on page]: the USB-extension tip for Zigbee radios is general practice, not a page fact; "Zigbee2MQTT" and "Matter server as
separate containers" are my inference from the page's "Container install has no add-ons". Home Guard (his ad blocker) is not
addressed; it is one more container on either box.

### 2c. Level1Techs 258288, oilbloodmoney (page: iPhone/Immich; honest answer favours his pick)

> Short version: for what you've described, the DH4300 Plus is a fine choice and you don't need to second-guess it. Point by point:
>
> - **Tailscale is safe** and is exactly the tool for "admin access to my drives from anywhere". It makes a private network between your devices with no port opened on your router, works behind carrier NAT, and the free tier covers a family. Immich's own remote-access guide lists it as one of the three sane routes (the other two: a WireGuard VPN with a forwarded port, or a domain with HTTPS through a reverse proxy) and warns never to expose a service's port bare to the internet. Install the Tailscale client on the NAS and on your phone/laptop; relatives in other states get a Tailscale invite, or a plain share link from UGOS if you'd rather not put them on your tailnet.
> - **Read-only folders for relatives:** per-user, per-shared-folder read/write or read-only permissions are a standard NAS feature and UGOS has them; make one user per relative, grant read-only on the folders you choose. Keep admin for yourself only.
> - **Is UGOS good?** It's a locked-down Debian (no apt, GUI-first), which for a self-described beginner is the right trade. Two years' warranty. The brand's stance on third-party OSes is unofficial.
> - **"Better options?"** The one real fork is ARM vs x86. The DH4300 Plus (8-core A76+A55, 8 GB) is $399.99 on UGREEN's US store today; its Intel sibling the 2-bay DXP2800 (N100, 8 GB to 16 GB, two M.2 slots) is $389.99. x86 matters only if you later want Docker containers that only ship amd64 images, virtual machines, or a self-hosted photo app with face search (Immich wants an x86-64 CPU for its machine-learning container). For file shares plus Tailscale, ARM is enough and runs cooler. You've said you want ARM; nothing in your list argues against it.
> - **StarCraft 1 hosting:** a NAS won't host Brood War games. StarCraft: Remastered matchmakes through Battle.net; a LAN game needs one of the players' PCs to host. Nothing to buy for that.
>
> If you ever add phone photo backup to the list, this is the write-up of what Immich needs on the box and on the iPhone: https://dealectric.com/best-nas-for-immich-iphone-photo-backup
> I run dealectric.com, which earns a commission on some links.

[Not on page]: UGOS per-folder permissions, Tailscale free tier/relative invites, StarCraft/Battle.net statements are general
knowledge, not page facts; Barry should be comfortable with them before posting. DH4300 Plus specs/price [verified this run].

### 2d. Level1Techs 258714, Tarkaelos (page: docker/HA)

> On the "off ramp for the NAS" specifically, since the replies have covered the lab side: your ~7 TB on a Core 2 Quad with a dying boot stick is the one urgent item, and a $400 2-bay box is the cheapest way to make it stop being urgent.
>
> A UGREEN DXP2800 ($389.99 diskless) plus two 10–12 TB drives in a mirror holds the 7 TB with room to grow, idles around 5 W against a Q9550's 60–100 W, and does the two things you listed: Jellyfin or Plex in its Docker app (N100 with Quick Sync for transcodes) and "some virtual machines for learning" in its VM app, with 8 GB DDR5 upgradable to 16 GB. Moving the data: build the new mirror, mount the FreeNAS share from the UGREEN (or rsync from the FreeNAS shell to the new SMB share), verify counts, then retire the old box. purkkaviritys's 8 TB external is the belt-and-braces copy during the move and the backup afterwards. CrashPlan dropping mapped drives stops mattering once the NAS itself runs a backup job to that external or to a cloud bucket.
>
> That leaves the full $600 of your budget for the gaming PC's new board/CPU, which is where purkkaviritys is right that the 64 GB DDR4 and 2080 Ti are the parts worth keeping. If you'd rather turn the 3770K rig into the lab as you said in post 5, the NAS still stands on its own: it's the thing that should be boring and always on, and the lab the thing you break.
>
> The under-$500 comparison (DXP2800 vs Synology DS225+, TerraMaster, Asustor, QNAP) is here: https://dealectric.com/best-nas-under-500-for-docker-immich-home-assistant
> I run dealectric.com, which earns a commission on some links.

[Not on page]: Q9550 power draw (60–100 W) and the rsync/SMB migration steps are general knowledge; Quick Sync for Jellyfin
transcodes is inferred from the page's note that Immich can use Quick Sync through /dev/dri on the N100, not stated for
Jellyfin. The page says the DXP2800's VM app is documented via owner guides (HAOS), not for general Linux VMs.

## 3. Checked and rejected

| URL | Why |
|---|---|
| https://community.home-assistant.io/t/1027472 (Which base system to use for HA, RAID, nginx…) | Oct 5–8, 12 posts. Hardware already ordered (AOOSTAR WTR PRO); the question is Proxmox vs TrueNAS; Immich only a passing "i hear that immich is very good ?". Demand 1 for us. |
| https://community.home-assistant.io/t/1030854 (400 Bad Request behind Cloudflare Tunnel… Host: NAS (Ugreen)) | Oct 29, 5 posts. Troubleshooting HA in Docker on a UGREEN already owned. Demand 1. |
| https://community.home-assistant.io/t/1029260 (Mini-PC: HA dedicated or via Proxmox?) | Oct 17–19, 46 posts. Owns the mini PC; setup question. |
| https://forum.level1techs.com/t/259616 (Why does NAS photo management still feel so DIY?) | Oct 27–28, 14 posts, 325 views. Discussion, everyone already owns their setup; the OP (AmirNur) is promoting FygoOS across L1T and STH. Demand 1. |
| https://forum.level1techs.com/t/258466 (Einy Tiny Miney Moe… bang for budget NAS host box) | Oct 12, 3 posts, unresolved, demand 3, but the path is a Lenovo M920q + SAS card + 8-bay enclosure under $400 for the computers; nothing we list fits an 8-bay DIY plan. |
| https://forum.level1techs.com/t/258893 (All-In-One Homelab Server) | Oct 18–Nov 1, 23 posts. Core Ultra 270K, RTX 3060, workstation board, 12+ bays; RAM already bought. Not a sub-$500 question. |
| https://forum.level1techs.com/t/258692 (Home storrage server) | Oct 15–21. EU, old rack servers; OP moved to adding drives to an existing 7950X box. |
| https://forum.level1techs.com/t/258132 (My Homelab: Too Many Parts) | Oct 8–11. Three servers owned, Immich already running; asks about clustering/GUI tools. |
| https://forum.level1techs.com/t/254435 (Need Advice on my NAS) | Aug 26–Oct 30. OP's last post Aug 27; Oct 30 post is a bystander's. |
| https://forum.level1techs.com/t/258541 (Buying used workstation… R9700) | GPU host question. |
| https://forums.servethehome.com/index.php?threads/using-an-arm-sbc-as-a-lightweight-home-nas.56634/ | Oct 27–30, 8 posts. ARM SBC + FygoOS discussion (same AmirNur); nobody buying. Demand 1. STH NAS subforum page 1 otherwise has no 2026-Q4 buying thread; "Choosing a NAS for home photo and video storage" (54697) is Jan–Feb 2026, not page-1 ranked. |
| https://github.com/immich-app/immich/discussions/32923 (immich backup from ugreen nas to pcloud) | Nov 3, 1 reply (maintainer). Backup-tool question from an owner; demand 1. Also #32804 (update question), #24990 (Jan 2026 show-and-tell: Immich on a DXP4800 with hardware ML; useful as a source, not a venue). |
| https://forums.overclockers.co.uk/threads/ugreen-nasync-series-owners-thread.19003680/ | Last post Sep 14, 2026 (page 5). Dormant; the only open question (DXP4800 Pro OS-on-SSD) is not ours. |
| https://slickdeals.net/f/19366932 (DXP4800 Plus $534 / DXP2800 $315, B&H) | Mar 31, 2026, expired, 2 comments, no Immich/HA question. No 2026 Slickdeals DXP2800 thread found with open questions. Slickdeals bans self-referral/affiliate links (rule not re-read this run). |
| https://yomotherboard.com/question/what-should-i-learn-before-setting-up-docker-and-immich-on-a-nas/ | Aug 3–5, 2026 (92 days). Answered four times; owner of a UGREEN already. |
| https://forum.heimnetz.de/threads/…home-assistant….6477/ | German-language forum; US-store page does not fit. Not read. |
| Quora: "How can I back my iPhone data (photo/video) to a NAS drive", "Is Synology NAS better than iCloud" and 8 similar | Old, generic, none mention Immich; dates not shown in results. Not evergreen-verified. |
| SNBForums NAS Buying Advice (27) and General NAS Discussion (10) | Newest threads Mar 25 and Aug 29, 2026. Dormant venue; "which NAS for home and docker support?" is from 2024. |
| TrueNAS forums | `search.json` "immich NAS hardware" since Sep 20: 0 results. DIY audience anyway. |
| Unraid forums | Newest 25 "immich nas buy" posts: support threads and the UGREEN NAS Control / LED plugins (DXP480T Plus, DXP8800 Plus owners running Unraid). Evidence for the "third-party OS" open concern, no purchase thread. |

## 4. Could not verify / blocked (manual checks for Barry)

- **ask.nascompares.com** (the only forum the target queries surfaced on the search tool's page 1): Cloudflare bot check blocks
  WebFetch and r.jina.ai. Threads to open by hand: tid 11836 and 12015 (surfaced for "best NAS under $500 for Docker and Immich"),
  12611 and 12757 (surfaced for 2-bay Docker/HA). Record dates and whether anyone has answered with a sub-$500 x86 pick.
- **Synology Community** (community.synology.com): search is JavaScript-only; could not read. Manual: search "Immich" and
  "DS225+ RAM" sorted by newest.
- **Stack Exchange** (superuser, unix.SE, serverfault): blocked for our search crawler. Manual: `site:superuser.com immich NAS`.
- **DH4300 Plus Docker/VM support**: UGREEN's product page is silent; our page documents only the DH2300 ("Docker removed from
  its App Center (reviews); no VMs"). Drafts 2a and 2c therefore argue from ARM, not from "no Docker". Verify before posting if
  Barry wants a stronger line.
- **OpenDroneMap on arm64**: neither the ODM docs nor the README state the architecture; the draft says only "run it on the desktop".
- **Level1Techs link limits for a new account**: Discourse defaults (2 links per post at trust level 0) assumed, not checked.
- **DXP4800 Plus current price**: not fetched; "over $500" rests on Slickdeals' $534 (Mar 2026) and $559.99 listings.

Reddit and Facebook are blocked for our tools; subreddits worth a manual check, with the search to run (sort by New, past month):
- r/immich — `NAS` ; `which NAS` ; `UGREEN`
- r/selfhosted — `NAS Immich under 500` ; `replace Google Photos NAS` ; `DXP2800`
- r/homelab — `first NAS Immich` ; `N100 NAS Immich`
- r/synology — `Immich DS225+` ; `DS223j Immich` (2 GB ARM units; our page says they are below Immich's 6 GB minimum)
- r/UgreenNASync — `Immich` ; `Home Assistant VM` ; `DH4300 Docker` (also settles the DH4300 Plus Docker question)
- r/DataHoarder — `NAS under 500 Docker`
- r/homeassistant — `NAS Home Assistant OS VM UGREEN` ; `Immich NAS`
- r/HomeServer — `Immich NAS budget`
Direct URL form: `https://www.reddit.com/r/<sub>/search/?q=<query>&sort=new&t=month&restrict_sr=1`.
