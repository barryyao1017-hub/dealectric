#!/usr/bin/env python3.12
"""DLC-45: does ChatGPT show Dealectric's own spec-card images (/img/<slug>.png, made by tools/images.py)?

    python3.12 growth/evals/image_probe.py              # all three prompts -> growth/evals/runs/<today>-images/
    python3.12 growth/evals/image_probe.py p3-url       # just one

Asks three prompts in chatgpt.com through the agent Chrome (same driver as ui.py; start the browser first with
uv --directory ~/Desktop/agent-vault run agent-vault browser) and saves, per prompt, a screenshot, the answer, and
every image the answer displayed. ChatGPT shows images through its own proxy (images.openai.com/static-rsc-...), so
the URL doesn't say whose image it is; the alt text is the source page's title, and a Dealectric page's title ends
in "· Dealectric". "ours" counts those; check the screenshots too (our cards are white with a green top bar).
First run 2026-10-21: no image of ours shown in any of the three; ChatGPT linked our PNG but displayed BLUETTI photos.
"""
import json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ui  # noqa: E402
import evallib as E  # noqa: E402

PROMPTS = {
    "p1-generic": "I want a portable power station around 1 kWh for weekend camping, under $600. Which one should I buy? Show me pictures of the options.",
    "p2-named": "What does Dealectric (dealectric.com) list for the BLUETTI AC180? Show me the image from their page and the buy link.",
    "p3-url": "Look at https://dealectric.com/bluetti-ac180 and show me the product image on that page, then summarize the specs.",
}
IMG_JS = """JSON.stringify([...document.querySelectorAll('main img')].map(i => ({src: i.currentSrc || i.src, alt: i.alt,
  w: i.naturalWidth, h: i.naturalHeight})).filter(i => i.w > 60))"""


def main(keys):
    out = Path(__file__).resolve().parent / "runs" / f"{E.today()}-images"
    out.mkdir(parents=True, exist_ok=True)
    seen = {}
    orig = ui.screenshot
    def shot(tab, path):  # read the images while the tab is still open (ask_chatgpt closes it after the screenshot)
        try:
            seen[path.name] = json.loads(tab.eval(IMG_JS))
        except Exception as e:  # noqa: BLE001
            seen[path.name] = [{"error": str(e)}]
        return orig(tab, path)
    ui.screenshot = shot
    summary = {}
    for k in keys or PROMPTS:
        r = ui.ask_chatgpt(PROMPTS[k], out / f"{k}.jpg")
        imgs = seen.get(f"{k}.jpg", [])
        r["images"] = imgs
        (out / f"{k}.json").write_text(json.dumps(r, indent=1, ensure_ascii=False))
        ours = [i for i in imgs if "dealectric" in (i.get("alt", "") + i.get("src", "")).lower()]
        summary[k] = {"account": r["account"], "images_shown": len(imgs), "ours": len(ours),
                      "image_sources": [i.get("alt", "")[:80] for i in imgs],
                      "dealectric_links": sorted({c["url"].split("?")[0] for c in r["citations"] if "dealectric.com" in c["url"]})}
        print(k, json.dumps(summary[k], ensure_ascii=False))
        time.sleep(5)
    (out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print("saved", out)


if __name__ == "__main__":
    main(sys.argv[1:])
