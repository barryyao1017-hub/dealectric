"""Dashboard queries (SQLite / D1). Each is self-contained: one SELECT that the dashboard stores as a live query."""

# Pacific day of an ISO UTC timestamp (PST, UTC-8; Pacific Daylight Time is not modelled).
PT = "datetime({c}, '-8 hours')"

# Human /go/ clicks: browser redirects that no bot rule flagged, minus our own checks and scanner user agents
# (same rules as tools/dailyupdate.py real_ua), with the platform the click came from.
HC = """seen AS (SELECT user_agent AS ua, IFNULL(country, '') AS country, date(datetime(ts, '-8 hours')) AS day,
            COALESCE(MAX(CASE WHEN platform NOT IN ('internal', 'direct') THEN platform END), 'direct') AS platform
          FROM pageviews WHERE bot_like = 0 GROUP BY 1, 2, 3),
burst AS (SELECT user_agent AS ua, IFNULL(country, '') AS country, date(datetime(ts, '-8 hours')) AS day FROM clicks
          WHERE kind = 'redirect' GROUP BY 1, 2, 3 HAVING COUNT(DISTINCT slug) >= 5),
hc AS (
  SELECT c.*, date(datetime(c.ts, '-8 hours')) AS day,
    CASE
      WHEN c.tag LIKE 'chatgpt%' THEN 'chatgpt'
      WHEN c.tag IN ('muse', 'ref:muse', 'ref:meta.ai', 'ref:meta-app', 'meta.ai', 'meta-app') THEN 'meta'
      WHEN c.tag LIKE 'ref:%' THEN substr(c.tag, 5)
      WHEN c.tag <> '' THEN c.tag
      WHEN c.referrer LIKE '%perplexity.ai%' THEN 'perplexity'
      WHEN c.referrer LIKE '%claude.ai%' THEN 'claude'
      WHEN c.referrer LIKE '%gemini.google%' THEN 'gemini'
      WHEN c.referrer LIKE '%copilot.microsoft%' THEN 'copilot'
      WHEN c.referrer LIKE '%google.%' THEN 'google'
      WHEN c.referrer LIKE '%bing.com%' THEN 'bing'
      WHEN c.referrer LIKE 'https://dealectric.com%' THEN COALESCE((SELECT platform FROM seen WHERE seen.ua = substr(c.user_agent, 1, 300)
             AND seen.country = IFNULL(c.country, '') AND seen.day = date(datetime(c.ts, '-8 hours'))), 'direct')
      ELSE 'direct' END AS platform,
    CASE WHEN c.referrer LIKE 'https://dealectric.com/%'
         THEN replace(rtrim(CASE WHEN instr(substr(c.referrer, 24), '?') > 0
                                 THEN substr(substr(c.referrer, 24), 1, instr(substr(c.referrer, 24), '?') - 1)
                                 ELSE substr(c.referrer, 24) END, '/'), '.html', '')
         ELSE COALESCE(o.page, c.slug) END AS page,
    COALESCE(o.brand, '') AS brand
  FROM (SELECT clicks.*, lower(CASE WHEN instr(x, '&') > 0 THEN substr(x, 1, instr(x, '&') - 1) ELSE x END) AS tag
        FROM (SELECT clicks.*, COALESCE(NULLIF(utm_source, ''),
                CASE WHEN referrer LIKE '%utm_source=%' THEN substr(referrer, instr(referrer, 'utm_source=') + 11) END, '') AS x
              FROM clicks WHERE kind = 'redirect' AND bot_like = 0) clicks) c
  LEFT JOIN meta_offers o ON o.slug = c.slug
  WHERE c.kind = 'redirect' AND c.bot_like = 0 AND IFNULL(c.verified_bot, '') = '' AND IFNULL(c.method, 'GET') = 'GET'
    AND length(IFNULL(c.user_agent, '')) >= 60 AND c.user_agent NOT LIKE '%HeadlessChrome%'
    AND c.user_agent NOT LIKE '%Nexus 5X%' AND c.user_agent NOT LIKE '%iPhone OS 13_2_3%'
    AND c.user_agent NOT LIKE '%dealectric-%' AND IFNULL(c.query, '') NOT LIKE '%dlc_check%'
    AND IFNULL(c.utm_source, '') NOT IN ('test-probe', 'claude-check')
    -- A person's click names where it came from: an assistant's tag, an outside referrer, or one of our pages that the
    -- same browser opened as a person that day. Untagged clicks with neither are crawlers following our links.
    AND (c.tag <> '' OR (IFNULL(c.referrer, '') <> '' AND c.referrer NOT LIKE 'https://dealectric.com%')
         OR (c.referrer LIKE 'https://dealectric.com%' AND EXISTS (SELECT 1 FROM seen WHERE seen.ua = substr(c.user_agent, 1, 300)
               AND seen.country = IFNULL(c.country, '') AND seen.day = date(datetime(c.ts, '-8 hours')))))
    -- One browser opening 5+ different offers in a day is a link checker, not a shopper.
    AND NOT EXISTS (SELECT 1 FROM burst WHERE burst.ua = c.user_agent AND burst.country = IFNULL(c.country, '')
               AND burst.day = date(datetime(c.ts, '-8 hours')))
)"""

# Human page views (bot_like = 0) with a visitor key: one browser on one Pacific day.
HV = """hv AS (
  SELECT p.*, date(datetime(p.ts, '-8 hours')) AS day,
    date(datetime(p.ts, '-8 hours')) || '|' || IFNULL(p.user_agent, '') || '|' || IFNULL(p.country, '') || '|' || IFNULL(p.asn, 0) AS visitor
  FROM pageviews p WHERE p.bot_like = 0
)"""

# Sales with the click their sub-ID names: page, brand and platform. A sale without a sub-ID (a code used without our
# link) keeps its brand and counts under platform 'no click'.
SA = """sa AS (
  SELECT s.*, date(datetime(s.ts, '-8 hours')) AS day, CASE WHEN s.commission > 0 THEN 1 ELSE 0 END AS orders,
    COALESCE(c.page, o.page, '(no click)') AS page,
    COALESCE(NULLIF(o.brand, ''), al.brand, s.advertiser) AS brand,
    COALESCE(c.platform, CASE WHEN s.sub_id <> '' THEN 'direct' ELSE 'no click' END) AS platform
  FROM sales s
  LEFT JOIN meta_offers o ON o.slug = substr(s.sub_id, 1, instr(s.sub_id, '.') - 1)
  LEFT JOIN meta_brand_alias al ON al.alias = lower(s.advertiser)
  LEFT JOIN hc c ON s.sub_id <> '' AND c.click_id = substr(s.sub_id, instr(s.sub_id, '.') + 1)
)"""

WEEK = "date({d}, '-6 days', 'weekday 1')"   # Monday of the week that holds day d

SUMMARY = f"""WITH {HC}, {HV}, {SA},
wk AS (SELECT {WEEK.format(d="date(datetime('now', '-8 hours'))")} AS start, date(datetime('now', '-8 hours')) AS today),
s AS (SELECT IFNULL(SUM(commission), 0) AS c_all, IFNULL(SUM(orders), 0) AS o_all,
        IFNULL(SUM(CASE WHEN day >= wk.start THEN commission END), 0) AS c_wk, IFNULL(SUM(CASE WHEN day >= wk.start THEN orders END), 0) AS o_wk,
        IFNULL(SUM(CASE WHEN day >= date(wk.start, '-7 days') AND day <= date(wk.today, '-7 days') THEN commission END), 0) AS c_lw_td,
        IFNULL(SUM(CASE WHEN day >= date(wk.start, '-7 days') AND day < wk.start THEN orders END), 0) AS o_lw
      FROM sa, wk),
v AS (SELECT COUNT(DISTINCT visitor) AS v_all, COUNT(DISTINCT CASE WHEN day >= wk.start THEN visitor END) AS v_wk,
        COUNT(DISTINCT CASE WHEN day >= date(wk.start, '-7 days') AND day < wk.start THEN visitor END) AS v_lw
      FROM hv, wk),
c AS (SELECT COUNT(*) AS k_all, COUNT(CASE WHEN day >= wk.start THEN 1 END) AS k_wk FROM hc, wk)
SELECT wk.start AS week_start, wk.today AS today,
  ROUND(s.c_all, 2) AS commission_total, ROUND(s.c_wk, 2) AS commission_week, ROUND(s.c_lw_td, 2) AS commission_last_week_to_date,
  s.o_all AS orders_total, s.o_wk AS orders_week, v.v_all AS visitors_total, v.v_wk AS visitors_week,
  c.k_all AS clicks_total, c.k_wk AS clicks_week,
  ROUND(100.0 * s.o_all / NULLIF(v.v_all, 0), 2) AS conversion_total_pct,
  ROUND(100.0 * s.o_wk / NULLIF(v.v_wk, 0), 2) AS conversion_week_pct,
  ROUND(100.0 * s.o_lw / NULLIF(v.v_lw, 0), 2) AS conversion_last_week_pct,
  (SELECT MIN(ts) FROM pageviews WHERE backfill = 0) AS full_logging_since
FROM wk, s, v, c"""

def series(unit):
    if unit == "day":
        key, start, step = "day", "'2026-10-18'", "'+1 day'"
    else:
        key, start, step = "week", WEEK.format(d="'2026-10-18'"), "'+7 days'"
    k = (lambda col: col) if unit == "day" else (lambda col: WEEK.format(d=col))
    return f"""WITH RECURSIVE {HC}, {HV}, {SA},
cal(period) AS (SELECT {start} UNION ALL SELECT date(period, {step}) FROM cal
                WHERE date(period, {step}) <= date(datetime('now', '-8 hours'))),
v AS (SELECT {k('day')} AS period, COUNT(DISTINCT visitor) AS visitors, COUNT(*) AS views FROM hv GROUP BY 1),
c AS (SELECT {k('day')} AS period, COUNT(*) AS clicks FROM hc GROUP BY 1),
s AS (SELECT {k('day')} AS period, SUM(orders) AS orders, SUM(commission) AS commission FROM sa GROUP BY 1)
SELECT cal.period AS {key}, IFNULL(v.visitors, 0) AS visitors, IFNULL(v.views, 0) AS views, IFNULL(c.clicks, 0) AS clicks,
  IFNULL(s.orders, 0) AS orders, ROUND(IFNULL(s.commission, 0), 2) AS commission,
  ROUND(100.0 * IFNULL(s.orders, 0) / NULLIF(v.visitors, 0), 2) AS conversion_pct
FROM cal LEFT JOIN v USING (period) LEFT JOIN c USING (period) LEFT JOIN s USING (period)
ORDER BY cal.period"""

DAILY, WEEKLY = series("day"), series("week")

PAGES = f"""WITH {HC}, {HV}, {SA},
v AS (SELECT page, COUNT(*) AS views, COUNT(DISTINCT visitor) AS visitors FROM hv GROUP BY page),
c AS (SELECT page, COUNT(*) AS clicks FROM hc GROUP BY page),
s AS (SELECT page, SUM(orders) AS orders, SUM(commission) AS commission FROM sa GROUP BY page),
k AS (SELECT page FROM v UNION SELECT page FROM c UNION SELECT page FROM s)
SELECT CASE WHEN k.page = '' THEN '/' WHEN k.page = '(no click)' THEN 'Code used without our link' ELSE '/' || k.page END AS page,
  COALESCE(m.kind, CASE WHEN k.page = '(no click)' THEN 'none' ELSE 'unlisted' END) AS kind,
  COALESCE(m.topic, '') AS topic, COALESCE(m.experiment, '') AS experiment, COALESCE(m.hypothesis, '') AS hypothesis,
  COALESCE(m.batch, '') AS batch,
  IFNULL(v.views, 0) AS views, IFNULL(v.visitors, 0) AS visitors, IFNULL(c.clicks, 0) AS clicks,
  IFNULL(s.orders, 0) AS orders, ROUND(IFNULL(s.commission, 0), 2) AS commission,
  ROUND(100.0 * IFNULL(s.orders, 0) / NULLIF(v.visitors, 0), 2) AS conversion_pct
FROM k LEFT JOIN meta_pages m ON m.page = k.page LEFT JOIN v ON v.page = k.page LEFT JOIN c ON c.page = k.page
LEFT JOIN s ON s.page = k.page
ORDER BY commission DESC, views DESC, clicks DESC LIMIT 100"""

BRANDS = f"""WITH {HC}, {HV}, {SA},
v AS (SELECT m.brand, COUNT(*) AS views FROM hv JOIN meta_pages m ON m.page = hv.page WHERE m.brand <> '' GROUP BY 1),
c AS (SELECT brand, COUNT(*) AS clicks FROM hc WHERE brand <> '' GROUP BY 1),
s AS (SELECT brand, SUM(orders) AS orders, SUM(commission) AS commission, SUM(sale) AS sales FROM sa GROUP BY 1),
k AS (SELECT brand FROM meta_brands UNION SELECT brand FROM c UNION SELECT brand FROM s)
SELECT k.brand, COALESCE(b.network, '') AS network, COALESCE(b.rate, '') AS program_rate,
  COALESCE(b.topic, '') AS topic, COALESCE(b.experiment, '') AS experiment, COALESCE(b.hypothesis, '') AS hypothesis,
  COALESCE(b.added, '') AS added,
  IFNULL(v.views, 0) AS views, IFNULL(c.clicks, 0) AS clicks, IFNULL(s.orders, 0) AS orders,
  ROUND(IFNULL(s.commission, 0), 2) AS commission, ROUND(IFNULL(s.sales, 0), 2) AS sales,
  ROUND(100.0 * IFNULL(s.orders, 0) / NULLIF(c.clicks, 0), 2) AS conversion_pct,
  ROUND(100.0 * s.commission / NULLIF(s.sales, 0), 2) AS commission_rate_pct
FROM k LEFT JOIN meta_brands b ON b.brand = k.brand LEFT JOIN v ON v.brand = k.brand LEFT JOIN c ON c.brand = k.brand
LEFT JOIN s ON s.brand = k.brand
ORDER BY commission DESC, clicks DESC, views DESC LIMIT 100"""

PLATFORMS = f"""WITH {HC}, {HV}, {SA},
v AS (SELECT platform, COUNT(DISTINCT visitor) AS visitors, COUNT(*) AS views FROM hv WHERE platform <> 'internal' GROUP BY 1),
c AS (SELECT platform, COUNT(*) AS clicks FROM hc GROUP BY 1),
s AS (SELECT platform, SUM(orders) AS orders, SUM(commission) AS commission, SUM(sale) AS sales FROM sa GROUP BY 1),
k AS (SELECT platform FROM v UNION SELECT platform FROM c UNION SELECT platform FROM s)
SELECT k.platform, IFNULL(v.visitors, 0) AS visitors, IFNULL(v.views, 0) AS views, IFNULL(c.clicks, 0) AS clicks,
  IFNULL(s.orders, 0) AS orders, ROUND(IFNULL(s.commission, 0), 2) AS commission, ROUND(IFNULL(s.sales, 0), 2) AS sales,
  ROUND(100.0 * s.commission / NULLIF(s.sales, 0), 2) AS commission_rate_pct,
  ROUND(100.0 * IFNULL(s.orders, 0) / NULLIF(v.visitors, 0), 2) AS conversion_pct,
  ROUND(100.0 * IFNULL(s.orders, 0) / NULLIF(c.clicks, 0), 2) AS click_conversion_pct
FROM k LEFT JOIN v USING (platform) LEFT JOIN c USING (platform) LEFT JOIN s USING (platform)
ORDER BY commission DESC, visitors DESC, clicks DESC"""

ALL = {"summary": SUMMARY, "daily": DAILY, "weekly": WEEKLY, "pages": PAGES, "brands": BRANDS, "platforms": PLATFORMS}

# One-time production backfill (needs Barry's OK): earlier human visits from `landings`, and the 10-29 CJ sale that
# predates the sales table (CJ commission 3886659982, read from CJ's Commission Detail report on 2026-11-11).
BACKFILL = """INSERT INTO pageviews (ts, page, status, platform, tag, referrer, user_agent, country, asn, bot_like, backfill)
SELECT ts, page, status,
  CASE WHEN utm_source LIKE 'chatgpt%' THEN 'chatgpt' WHEN utm_source IN ('muse', 'ref:muse', 'ref:meta.ai', 'ref:meta-app') THEN 'meta'
       WHEN utm_source LIKE 'ref:%' THEN substr(utm_source, 5) ELSE lower(utm_source) END,
  utm_source, referrer, user_agent, country, asn, 0, 1
FROM landings WHERE bot_like = 0 AND IFNULL(verified_bot, '') = '' AND IFNULL(purpose, '') = '' AND IFNULL(status, 200) = 200
  AND IFNULL(method, 'GET') = 'GET' AND IFNULL(query, '') NOT LIKE '%dlc_check=%' AND length(IFNULL(user_agent, '')) >= 60
  AND user_agent NOT LIKE '%HeadlessChrome%' AND user_agent NOT LIKE '%dealectric-%'
  AND NOT EXISTS (SELECT 1 FROM pageviews WHERE backfill = 1);
INSERT OR IGNORE INTO sales (ts, network, txn_id, advertiser, commission, sale, currency, sub_id, event_date, voucher)
VALUES ('2026-10-29T15:30:00.000Z', 'cj', '3886659982', 'ALLPOWERS', 33.63, 672.52, 'USD', '', '2026-10-29T14:42:00Z', '');"""
