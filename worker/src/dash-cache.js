// Dashboard cache (2026-11-17, Barry: "fix it" after D1 hit its free 5M rows/day read cap on 11-15).
// The sales dashboard (claude.ai artifact TpCiDy6fNvUTHaifH3LyWA) re-derived "which clicks and page views are people"
// from all history in each of its nine queries, about 136k rows read per refresh. dash_hc / dash_hv hold exactly the
// hc / hv rows of those queries; the dashboard reads them for past days and computes only today live (~28k per refresh).
// This cron step recomputes yesterday and today every 30 minutes, so a later bot_like re-flag of a recent row lands.
// Older days stay as cached: after a backfill that re-judges older rows, rebuild both tables (worker/README.md).
// The SQL is the dashboard's own hc / hv definition, limited to rows since yesterday 00:00 Pacific (index-bound).
const SINCE_DAY = "date(datetime('now', '-8 hours'), '-1 day')";

const REFRESH_HC = `WITH seen AS (SELECT user_agent AS ua, IFNULL(country, '') AS country, date(datetime(ts, '-8 hours')) AS day,
            COALESCE(MAX(CASE WHEN platform NOT IN ('internal', 'direct') THEN platform END), 'direct') AS platform
          FROM pageviews INDEXED BY pageviews_ts WHERE ts >= strftime('%Y-%m-%dT%H:%M:%S', date(datetime('now', '-8 hours'), '-1 day'), '+8 hours') AND bot_like = 0 GROUP BY 1, 2, 3),
burst AS (SELECT user_agent AS ua, IFNULL(country, '') AS country, date(datetime(ts, '-8 hours')) AS day FROM clicks INDEXED BY clicks_ts
          WHERE ts >= strftime('%Y-%m-%dT%H:%M:%S', date(datetime('now', '-8 hours'), '-1 day'), '+8 hours') AND kind = 'redirect' AND bot_like = 0 GROUP BY 1, 2, 3 HAVING COUNT(DISTINCT slug) >= 5),
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
              FROM clicks INDEXED BY clicks_ts WHERE ts >= strftime('%Y-%m-%dT%H:%M:%S', date(datetime('now', '-8 hours'), '-1 day'), '+8 hours') AND kind = 'redirect' AND bot_like = 0) clicks) c
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
)
INSERT INTO dash_hc SELECT * FROM hc`;

const REFRESH_HV = `WITH hv AS (
  SELECT p.*, date(datetime(p.ts, '-8 hours')) AS day,
    date(datetime(p.ts, '-8 hours')) || '|' || IFNULL(p.user_agent, '') || '|' || IFNULL(p.country, '') || '|' || IFNULL(p.asn, 0) AS visitor
  FROM pageviews p INDEXED BY pageviews_ts WHERE p.ts >= strftime('%Y-%m-%dT%H:%M:%S', date(datetime('now', '-8 hours'), '-1 day'), '+8 hours') AND p.bot_like = 0
)
INSERT INTO dash_hv SELECT * FROM hv`;

export async function refreshDashCache(env) {
  await env.DB.batch([
    env.DB.prepare(`DELETE FROM dash_hc WHERE day >= ${SINCE_DAY}`),
    env.DB.prepare(REFRESH_HC),
    env.DB.prepare(`DELETE FROM dash_hv WHERE day >= ${SINCE_DAY}`),
    env.DB.prepare(REFRESH_HV),
  ]);
}

export const DASH_SQL = { REFRESH_HC, REFRESH_HV, SINCE_DAY };
