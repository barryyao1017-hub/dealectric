# dealectric.com — site source

Live site: https://dealectric.com (GitHub Pages, branch `main`, folder `/` root).

## Layout
- Repo root = the files GitHub Pages serves (flat: `about.html`, `data.html`, `llms.txt`, `dealectric.json`, `CNAME`, `.nojekyll`, …).
- `src/` = the generator. Edit copy in `src/content.py`; brand/domain/email/verification tags in `src/build.py` (`SITE` and `VERIFY`).

## Rebuild & deploy
```bash
cd src
python3 build.py          # writes src/dist/ (nested) and src/dist-flat/ (what we serve)
cp -r dist-flat/. ..      # copy flat output to repo root
cd .. && git add -A && git commit -m "Update site" && git push
```
GitHub Pages redeploys in ~1 minute. (Without git: GitHub → "Add file → Upload files" replaces same-named files.)

## Infra
- DNS at Porkbun: A @ → 185.199.108/109/110/111.153; CNAME www → barryyao1017-hub.github.io. hello@dealectric.com forwards via Porkbun.
- Impact site verification is the `VERIFY` meta tag in `src/build.py` (keep it on every page).
- Planned: Cloudflare in front for analytics/AI-crawler insights and the `/go/` sub-ID redirect worker.
