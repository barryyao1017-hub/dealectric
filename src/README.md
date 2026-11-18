# dealectric.com — site source

Live site: https://dealectric.com (GitHub Pages, branch `main`, folder `/docs`, extensionless URLs; Cloudflare in front).

## Layout
- `src/` = the generator. Copy in `content.py`; product records, `VERIFIED` date and retired slugs in `products.py`;
  affiliate program IDs in `links.json`; tested discount codes in `coupons.json`; brand/domain/email/verification tags in `build.py` (`SITE`, `VERIFY`).
- `src/bestoffer.json` = the best-offer check (DLC-320), written by `tools/bestoffer.py decide`: per product, the same
  item's Amazon listing, the other sellers read that day and whether one beat or tied the price through our link.
  `build.py` leads a page with the tagged Amazon link while Amazon is cheaper (`amazon_lead`), adds "Lowest of N sellers
  checked <date>" where ours won (`lowest_tail`), and claims nothing where a seller we cannot link was cheaper.
  A re-check is: `tools/buycheck.py` (Google Shopping) → hand pass in `growth/buylink/<date>-bestoffer-hand.json` →
  `tools/bestoffer.py decide`; `tools/amzprice.py` re-reads the Amazon listings daily.
- `docs/` = what GitHub Pages serves, written by `build.py` (it replaces the folder; never hand-edit it).
- `worker/src/links-map.json` = the `/go/<slug>` → CJ/Awin link map for the Cloudflare Worker, also written by `build.py`.
- `src/dist/` = the nested intermediate build (git-ignored).

## Rebuild & deploy
```bash
python3.12 src/build.py        # writes src/dist/, docs/ and worker/src/links-map.json
git add -A && git commit -m "..." && git push
cd worker && npx wrangler deploy   # whenever a product, URL or price changed (links-map carries them); token: see worker/README.md
python3 tools/indexnow.py          # tell Bing & co. which pages changed
```
GitHub Pages redeploys in about a minute.

## Infra
- DNS and proxy at Cloudflare (zone dealectric.com); hello@dealectric.com forwards via Porkbun.
- Web Analytics is injected at Cloudflare's edge, so there is no analytics script in the HTML.
- Impact site verification is the `VERIFY` meta tag in `build.py` (keep it on every page).
