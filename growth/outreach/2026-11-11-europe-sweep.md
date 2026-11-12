# Europe network sweep, 2026-11-11 (DLC-155)

Barry 11-11: "Turn on Amazon OneLink for the UK and EU now ... we don't have to fully adopt and productionize these new markets. However, you should expand the network and start with enabling everything for Europe as a starting point."
Scope: same rules as the 11-03 US sweep (brand-owned consumer-electronics device and accessory programs; skipped retailers and marketplaces, software/VPN, kitchen and white goods, apparel, e-bikes/scooters, lead-gen, B2B). Regional variants of one brand were all applied (e.g. JBL in 12 countries). Nothing on the site changes: no EU product records, prices, codes, pages or Worker geo-routing until Barry asks.

## Amazon Associates: OneLink already on
Associates Central → Global earning preferences (`/app/global-earning-preferences`) shows "10 of 10 active": US, Canada, UK, Germany, France, Italy, Spain, Netherlands, Poland, Sweden, all earning on the `dealectric-20` store ID. Nothing to switch. Still Barry's: tax and payment details (the home page shows "The primary account holder needs to finish filling out tax information", DLC-157); each country's earnings accrue to that country's Associates account. Our Amazon links are amazon.com/dp/<ASIN>; OneLink redirects a European visitor to the local store only where the same ASIN exists, and US 120 V power stations mostly don't.

## Awin (same publisher account 3120687)
Directory pulled with region = all 28 European countries, status Not Applied: 1,497 programs in Audio Visual, Computers, Electronic Accessories, Electronic Superstore, Gadgets, PC & Video Games, Photography; 3,261 more in Green, Automotive, Home & Garden, Sports Equipment, White Goods (keyword-screened); plus brand-name searches for ~230 brands.
Message (promotion https://dealectric.com): catalog for shoppers and AI shopping assistants, dated specs/price checks, network- or brand-approved codes tested in the cart, disclosed sponsored links, power stations/solar the largest category, "adding UK and European coverage", no brand-keyword bidding, operated by Agentify LLC. No traffic claims.
Terms: each program's profile text was screened for price-display and coupon/voucher bans (none found), but the downloadable terms PDFs were **not** read. Read them before building any EU page for a brand.

**Approved on the spot (10):** AKKO FR (69050), DATOUBOSS (DE) (127057), METZ (130499), Mibro (131533), Mibro FR (131783), miniminipower DE (57455), Monsgeek EU (113754), Nothingprojector (75408), SIRUI Optical GmbH (DE) (128645), Xiaomi RO (118223).

**Pending (276, incl. BLUETTI UK sent by hand first):** 3DMakerpro (EU); ACER BE; Acer ×13; Acer Gadget Partner-Newease; AKKO ×2; ALLPOWERS ×6; ALLPOWERS PL & UA; AlphaESS Vitapower; Anker ×2; Anker Solix DE; ANTHBOT DE; Anthbot Denmark; AOSU DA; Aqara UK; Arlo Security ×3; beyerdynamic DE; BLUETTI ×5; Cambridge Audio ×2; Creality; Eco-Worthy DE; EcoFlow ×3; Ecoflow NL; Ecovacs ×3; ECTIVE DE; ElectricSun ×2; Endgame Gear ×2; ESR ×2; eSUN official store; Eufy FR; Fanttik (DE); FRITZ! DE; Geekom ×2; GEEKOM ×2; Harman Kardon ×12; HMD ×2; Holdit ×6; Hollyland DE; Honor ×6; Hoymiles Affiliate Program; Hubble Connected; Humax 1; ieGeek ×4; Imou ×3; inateck.de; Indevolt; iRobot IT; Jackery ×2; JAPANNEXT FR; JBL ×12; Kippy srl IT; Klyqa DE; LG ×6; LG Electronics ×2; LG PRM ES; LiTime ×2; Loewe DE; MEDION AT; Medionshop DE; Meross Smarthome; MIFCOM; MiniFinder SE; MSI ×5; Narwal ×4; Navimow ×3; Nebo Tools; Nextbase DE; NIVOCASE; NIVOCASE DE; Nothing Tech ×3; OBSBOT ×2; Oehlbach DE; OLIGHT UK; Olight ×3; Oppo IT; Otterbox ×3; PAJ GPS ×4; PURE Audio UK; Q Acoustics UK; Refoss DE; reolink DE; Road Angel; Samsung ×26; Simplisafe; SolarMars; SONOFF DE; Sony ×12; Sovol EU; Sylvoxtv ×2; Tado ×3; Targus ×4; Tech21 UK; Technaxx; TECKNET DE; TESmart DE; TP Link Store NL; UGREEN ×2; Unistellar ×2; Vasco FR; Vasco Electronics DE; VIVE ×3; Vivo ×2; WiiM Audio DE; Wired2Fire; Wybot EU; Xiaomi ×11; Xplora ×2; XPPen DE; XTRONS; Xtrons DE; Yale Home FR; Yale Store; YaleHome ×2; Zagg ×2; Zens Shop BNL; Zosi ×2.

Full id list: every program in this file's Awin section was sent with the same message; Awin returned "saved: pendingApproval" (or "saved: active") for each, and a re-read of the profiles confirmed the status. AKKO DE answered 'membership already exists' (a duplicate send while the job restarted; it is pending).

## CJ (publisher 8096118)
All 2,824 CJ advertisers pulled (internal search JSON); 1,184 with no relationship bill in EUR/GBP/CZK/PLN/SEK/DKK. Screened to 14 brand programs, 12 applied:
- **Approved on the spot:** XPLORA UK (5175167).
- **Pending:** EcoFlow EU (6123342), Dreame EU (7221208), ASUS ES (5260673), SanDisk EU (7244342, special terms accepted: standard affiliate agreement, no price or coupon ban), Marshall Headphones (4763187, SEK), Withings (4996850), Nuki Home Solutions International (7313136), myFUJIFILM (4945330), Husqvarna EMEA (6307113), STIGA (7470667), Weenect (5831266).
- **Held:** Canon EMEA (6509919) and Canon UK (6509930), same reason Canon US is held (price-display ban, DLC-154).
- Skipped: CZ/SK/HU-only shops, appliance makers (Philips, Kärcher, Tefal, Electrolux), software, retailers.
How to apply on CJ from a script: opening `/member/accounts/publisher/affiliations/joinprograms.do?onJoin=clickSearch&advertiserId=<id>&publisherId=8096118&norefresh=true` submits the application at once (the Apply button opens that page as a popup, which a background tab blocks); programs with special terms show them first with an "Accept and Apply" button.
Profiles updated the same day (Barry: "Yes, update profiles"): see "Network profiles" below.

## Rakuten (site 613226, US network)
The publisher search spans the US, UK (GB), FR and DE networks from the same account. Applied (all "pending", POST `/api/partnerships/<mid>`):
Lautsprecher Teufel Germany (45970), Austria (45971), Belgium (45976), France (45972), Netherlands (45975), Poland (45973), Switzerland (45977), Italy (46426), Spain (46425); Panasonic UK (53579); Technics EU (54282), Technics UK (54278); Roberts Radio (53968).
Blocked ("Currently you do not meet these terms"): Panasonic EU (54215), Mous UK (47971). Samsung UK (53591) shows no Apply button.
Teufel's terms are a downloadable PDF, not read; same rule as Awin before building pages.

## Network profiles (updated 2026-11-11, Barry's OK)
All three now say the audience is mostly US today and UK/European coverage is being added from November 2026; no traffic claims beyond "under 1,000 visits per month"; operated by Agentify LLC.
- **CJ:** Network Profile description rewritten (dropped "Audience: United States (95%+)" and "Operated from Sunnyvale, California"); promotional property 101901491 description rewritten and tags United Kingdom, Europe, solar kits added.
- **Awin:** Promotional regions now US (primary) plus 27 European countries (Russia left out); profile description and promotional-space description rewritten.
- **Rakuten:** channel description rewritten (225-character limit).
- Not changed: the contact/postal addresses on the networks (Awin still shows the Sunnyvale address) and the payee/tax details. Those are Barry's.

## Impact
Not touched (Marketplace still declined; DLC-15/154).

## Next
- Approvals arrive by email; the approval-inbox flow (DLC-14) records them. Add an EU program to `src/links.json` only when a page uses it.
- When Barry wants EU pages: UK first; per brand read the terms PDF, pick 230 V / UK-plug SKUs, prices in GBP incl. VAT, codes tested from a UK cart, then Worker geo-routing of `/go/` by `cf.country`.
