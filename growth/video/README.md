# YouTube pilot (DLC-187)

Barry, 2026-11-06: AI-made videos on YouTube, for exposure. Scoped that day (Barry: "Yes, as scoped"):

- **Five long-form videos (3–4 min) plus a Short for each.** Description links in Shorts can't be clicked, and Shorts
  get about 6% of YouTube's AI-search citations; long-form gets the citations and the clickable links. Each Short
  points to its video through the Related Video link.
- **No video on dealectric.com.** A YouTube embed is JavaScript plus third-party cookies, which the site rule forbids,
  and only about 88 tagged human landings arrived in the 30 days to 11-06.
- **Topics follow real demand**: the pages that drew the most tagged human landings in those 30 days (solar kits with
  panels, 24; AC200L/RV, 15; small kits, 6–8).

| id | topic | page it points to |
|---|---|---|
| `solar-kits-1kwh` | Solar generators with panels included: comparing 1 kWh kits | solar-generator-with-panels-included |
| `solar-kits-under-500` | Solar generator kits under $500: 288 Wh or 1 kWh | best-solar-generator-kit-under-500 |
| `rv-2kwh` | 2 kWh for an RV: the 30-amp plug catch | best-2kwh-power-station-for-rv |
| `ac180-kit` | BLUETTI AC180 + 200 W: what it runs, refill time | bluetti-ac180-200w-solar-kit |
| `solar-refill-math` | How long a 100/200/400 W panel takes to refill a station | solar-generator-with-panels-included |

## Making a video

    python3.12 growth/video/render.py <id>            # long.mp4 + short.mp4, captions, descriptions
    python3.12 growth/video/render.py <id> --slides   # slides only, to check the layout

Scripts live in `scripts/<id>.json`: a `say` line and a `slide` for each scene, with `chapter` names that become the
description's chapter list. Output goes to `out/<id>/` (gitignored). The voice is OpenAI `gpt-4o-mini-tts` (about a
cent per video), and audio is cached by text, so changing a single line re-voices only that scene. No prices are
spoken or drawn. The description is rebuilt from `src/` at each render with today's price, code and last-pass date,
so re-render before uploading.

Checks done 2026-11-06: transcribed the first render with whisper-1. The voice said "Dielectric" for Dealectric and
"LEAF P04" for LiFePO4, so `render.py` swaps in spoken forms (`SPEAK`): "Deal Electric" (the only spelling of four
that transcribed back as "Deal...") and "lithium iron phosphate". Captions keep the written spelling.

## Uploading (after DLC-185 and the checklist in growth/social/README.md)

- Barry approves each video before it goes up (outward-facing). Claude uploads through YouTube Studio in the Agent
  Chrome, signed in through agent-vault.
- One video and its Short every 2–3 days, not all at once: YouTube's spam policy targets "high volumes of similar content".
- Per upload: the title, description and tags from `out/<id>/long.txt` (or `short.txt`); captions from `long.srt` /
  `short.srt` (English); altered content: No; made for kids: No; category Science & Technology. Paid promotion: tick
  it only if a brand paid for the video (none has); affiliate links alone don't need it.
- On each Short, set the Related Video to its long video.

## Reading the result (30 days after the first upload)

    npx wrangler d1 execute dealectric --remote --command "SELECT utm_campaign, COUNT(*) FROM (SELECT substr(query, instr(query,'utm_campaign=')+13) AS utm_campaign FROM clicks WHERE utm_source='youtube' AND bot_like=0) GROUP BY 1"

Plus the same from `landings`, and YouTube Studio views and outbound clicks. Scale it if YouTube adds at least 10% to
monthly tagged human landings, or brings a credited sale. Otherwise stop.
