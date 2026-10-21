# dealectric.com — site source

Live site: https://dealectric.com (GitHub Pages, branch `main`, folder `/docs`, extensionless URLs; Cloudflare in front).

## Layout
- `src/` = the generator. Copy in `content.py`; product records, `VERIFIED` date and retired slugs in `products.py`;
  affiliate program IDs in `links.json`; tested discount codes in `coupons.json`; brand/domain/email/verification tags in `build.py` (`SITE`, `VERIFY`).
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
