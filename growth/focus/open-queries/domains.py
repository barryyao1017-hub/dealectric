"""Source classes for the open-query gate (2026-11-14). A domain is a primary source when the shopper's question has an
owner there: the maker of the product, an official body, or a major reviewer whose verdict ChatGPT repeats. Everything
else is a site of our own kind. Unknown domains fall to "small" and are listed by report.py for review."""
import re

MAKER = r"""ecoflow bluettipower bluetti jackery anker ankersolix goalzero renogy zendure pecron oupes allpowers iallpowers
vtoman growatt sungoldpower sungoldsolar battlebornbatteries dakotalithium victronenergy generac tesla enphase champion
championpowerequipment westinghouse westinghouseoutdoorpower honda powerequipment.honda yamaha duracell duracellpower
geneverse lionenergy naturesgenerator mangopower dji ugreen togopower bougerv rockpals baldr fossibot oukitel dabbsson
yoshinopower ampace 4patriots pointzero titansolar inergy inergytek humless ego egopowerplus dewalt milwaukeetool ryobitools
kohler kohlerpower briggsandstratton cummins apc cyberpower schneider-electric eaton tripplite resmed philips respironics
dometic iceco alpicool whynter starlink weboost harborfreight predatorengines wen wenproducts craftsman greenworks
einstar shining3d revopoint creality qidi3d qidi bambulab prusa3d anycubic elegoo vatrer vatrerpower redodo redodopower
litime ampertime epoch epochbatteries ecoworthy eco-worthy zerobreeze ecoflow anthbot mova mammotion segway navimow
husqvarna worx ecovacs vividstorm elitescreens silverticket alorair aprilaire santa-fe santafe midea frigidaire lg samsung
sunpower solaredge sol-ark eg4 eg4electronics signaturesolar mrcool pioneer senville minisplit clubcar ezgo yamahagolfcar
minnkota garmin lowrance winnebago thorindustries airstream lippert progressive-dynamics wfco xantrex magnum-dimensions
aimscorp gopower go-power zamp zampsolar rich-solar richsolar newpowa hqst bougerv dokio flexsolar topsolar sunjack
biolite nitecore omnicharge shargeek baseus inui mophie belkin soundcore nebula xgimi epson benq hisense formovie awol
optoma viewsonic jmgo dangbei frigidaire ge geappliances whirlpool bosch rheem lennox carrier trane goodman grundfos
zoeller wayne waynepumps liberty libertypumps basementwatchdog pentair franklin-electric gouldspumps
revopoint3d bosaenergy eabattery wiltsonenergy progressivedyn runhoodpower inergytek goalzero powerfilmsolar aliyuncs
matterhackers snapmaker flashforge sovol luba mammotion yarbo sunseeker ecoflow dreame roborock eufy
screeninnovations stewartfilmscreen akia nothingprojector valerion aosom ghostcontrols mightymule liftmaster""".split()
OFFICIAL = r"""energy.gov ready.gov fema.gov cdc.gov epa.gov cpsc.gov nfpa.org redcross.org osha.gov nrel.gov irs.gov
fda.gov nih.gov usda.gov noaa.gov weather.gov faa.gov tsa.gov lung.org heart.org mayoclinic.org clevelandclinic.org
aarp.org ul.com iihs.org nhtsa.gov energystar.gov eia.gov dsireusa.org""".split()
PUBLISHER = r"""nytimes.com wirecutter.com cnet.com pcmag.com techradar.com tomsguide.com theverge.com wired.com
popularmechanics.com popsci.com consumerreports.org outdoorgearlab.com bobvila.com thisoldhouse.com forbes.com cnn.com
rtings.com zdnet.com engadget.com digitaltrends.com usnews.com familyhandyman.com treehugger.com energysage.com
gearjunkie.com outsideonline.com fieldandstream.com outdoorlife.com rvtravel.com rv.com tomshardware.com pcworld.com
macworld.com androidcentral.com businessinsider.com nbcnews.com goodhousekeeping.com thespruce.com hgtv.com
architecturaldigest.com cleantechnica.com electrek.co pv-magazine.com solarreviews.com motortrend.com caranddriver.com
roadandtrack.com thedrive.com autoblog.com howtogeek.com lifewire.com makeuseof.com gizmodo.com arstechnica.com
nymag.com today.com usatoday.com washingtonpost.com theguardian.com bbc.com reviewed.com gearlab.com switchbacktravel.com
cleverhiker.com rei.com/learn mensjournal.com gearpatrol.com 9to5mac.com 9to5toys.com notebookcheck.net
all3dp.com 3dprintingindustry.com tomsguide.com projectorcentral.com soundandvision.com avsforum.com""".split()
RETAILER = r"""amazon.com walmart.com homedepot.com lowes.com bestbuy.com costco.com samsclub.com rei.com bhphotovideo.com
campingworld.com target.com ebay.com newegg.com microcenter.com northerntool.com tractorsupply.com acehardware.com
menards.com wayfair.com batteriesplus.com westmarine.com cabelas.com basspro.com etsy.com temu.com aliexpress.com
shopsolarkits.com signaturesolar.com altestore.com""".split()
COMMUNITY = r"""reddit.com quora.com youtube.com facebook.com diysolarforum.com irv2.com forestriverforums.com
expeditionportal.com stackexchange.com garagejournal.com cpaptalk.com apneaboard.com tiktok.com instagram.com
medium.com pinterest.com escapees.com rvforum.net airforums.com tacomaworld.com ih8mud.com overlandbound.com
backyardchickens.com permies.com homesteadingtoday.com houzz.com doityourself.com diychatroom.com""".split()


MANUALS = "device.report manuals.plus manualowl.com manualslib.com manualzz.com manualsfile.com manua.ls usermanual.wiki fccid.io".split()
EXTRA = {"tech.yahoo.com": "publisher", "yahoo.com": "publisher", "qvc.com": "retailer", "webstaurantstore.com": "retailer",
         "images.thdstatic.com": "retailer", "donrowe.com": "retailer", "publications.gc.ca": "official", "intertek.com": "official",
         "pdf.lowes.com": "retailer", "supplyhouse.com": "retailer", "sumppumpsdirect.com": "retailer", "gatedepot.com": "retailer",
         # reviewed 11-15 from the sources cited in open answers
         "static.globalindustrial.com": "maker", "s1.solacity.com": "maker",      # retailers' hosts for the makers' manuals and spec sheets
         "nfm.com": "retailer", "dynamism.com": "retailer", "batterie24.de": "retailer", "marinea.fi": "retailer",
         "solarkontor.de": "retailer", "ecosolarkits.com": "retailer", "blackboxsupplies.com": "retailer", "rapidscan3d.com": "retailer",
         "phillipsandtemro.com": "maker", "leochlithium.com": "maker", "dajiuenergy.com": "maker", "supercharge.com.au": "maker",
         "web.twindom.com": "maker", "rogerele.com": "maker",
         # reviewed 11-15 from the second chats
         "artec3d.com": "maker", "3d-scantech.com": "maker", "verisurf.com": "maker", "shop.scankraft.com": "maker", "shapify.me": "maker",
         "the-independent.com": "publisher", "dora.state.co.us": "official", "allprogenerators.com": "retailer",
         "golfcartbatterysource.com": "retailer", "f.machineryhost.com": "retailer", "vimeo.com": "community", "cdn.solarpowersupply.eu": "retailer",
         # reviewed 11-15 from the third chats
         "cyberpowersystems.com": "maker", "files.bbystatic.com": "maker",       # Best Buy's host for makers' manuals
         "skylab3d.com": "retailer", "amsindia.co": "retailer", "visionminer.com": "retailer", "precise3dm.com": "retailer",
         "b2b.offgridtec.com": "retailer", "bluetti.cn": "maker"}


def classify(domain: str) -> str:
    d = domain.lower().removeprefix("www.")
    if d in EXTRA:
        return EXTRA[d]
    if d in MANUALS:
        return "maker"      # a mirror of the maker's own manual: the maker's document is the source
    if d.endswith(".gov") or d.endswith(".edu") or d.endswith(".mil") or any(d == o or d.endswith("." + o) for o in OFFICIAL):
        return "official"
    for o in PUBLISHER:
        if d == o or d.endswith("." + o):
            return "publisher"
    for o in RETAILER:
        if d == o or d.endswith("." + o):
            return "retailer"
    for o in COMMUNITY:
        if d == o or d.endswith("." + o):
            return "community"
    if d == "dealectric.com":
        return "ours"
    parts = [p for p in re.split(r"[.\-]", d) if p]
    core = d.split(".")[-2] if d.count(".") else d
    for m in MAKER:
        if core == m or core.replace("-", "") == m.replace("-", "") or core.startswith(m + "power") or (len(m) >= 6 and m in parts):
            return "maker"
    if re.match(r"(support|help|docs|manual|kb|community|store|shop|us|uk|eu)\.", d) and any(m == d.split(".")[-2] for m in MAKER):
        return "maker"
    return "small"
