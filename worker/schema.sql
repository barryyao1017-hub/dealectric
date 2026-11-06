-- D1 schema for the Dealectric edge Worker. Apply with:
--   npx wrangler d1 execute dealectric --remote --file schema.sql   (or --local for wrangler dev)
CREATE TABLE IF NOT EXISTS clicks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,            -- ISO 8601 UTC
  slug TEXT NOT NULL,          -- product id, as in offers.json
  click_id TEXT NOT NULL,      -- random id passed to the network as <slug>.<click_id> (CJ sid / Awin clickref)
  network TEXT,                -- cj | awin
  method TEXT,                 -- GET or HEAD (link checkers)
  referrer TEXT,
  user_agent TEXT,
  country TEXT,
  verified_bot TEXT,           -- Cloudflare verified-bot category, if any
  bot_like INTEGER DEFAULT 0,  -- crude user-agent heuristic
  kind TEXT DEFAULT 'redirect', -- redirect (302 issued) | ai_fetch (AI assistant got the text page, no redirect)
  query TEXT,                  -- raw query string of the /go/ request, e.g. utm_source=chatgpt.com (ChatGPT sends no referrer)
  utm_source TEXT,             -- parsed utm_source, for grouping clicks by assistant
  asn INTEGER                  -- client network (Cloudflare cf.asn); Google's networks count as bot_like
);
-- Added 2026-10-18 for databases created before these columns existed (each fails harmlessly once applied):
-- ALTER TABLE clicks ADD COLUMN kind TEXT DEFAULT 'redirect';
-- ALTER TABLE clicks ADD COLUMN query TEXT;
-- ALTER TABLE clicks ADD COLUMN utm_source TEXT;
-- Added 2026-11-06 (YouTube's link scanners posed as Windows Chrome; index.js SCANNER_ASNS):
-- ALTER TABLE clicks ADD COLUMN asn INTEGER;
-- ALTER TABLE landings ADD COLUMN asn INTEGER;
CREATE INDEX IF NOT EXISTS clicks_ts ON clicks (ts);
CREATE INDEX IF NOT EXISTS clicks_slug ON clicks (slug);
CREATE INDEX IF NOT EXISTS clicks_click_id ON clicks (click_id);

-- Added 2026-10-28 (W3 step 0): page requests that arrive with a utm_source tag. The Worker passes every page through
-- to GitHub Pages unchanged and logs only these. ChatGPT tags its links utm_source=chatgpt.com.
CREATE TABLE IF NOT EXISTS landings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,            -- ISO 8601 UTC
  page TEXT NOT NULL,          -- path without slashes or .html ("" = home); equals clicks.slug on a product page
  path TEXT NOT NULL,          -- raw request path
  method TEXT,                 -- GET or HEAD
  status INTEGER,              -- status the origin answered with (200, 301, 404)
  query TEXT,                  -- raw query string
  utm_source TEXT,             -- parsed utm_source, e.g. chatgpt.com
  referrer TEXT,
  user_agent TEXT,
  country TEXT,
  verified_bot TEXT,           -- Cloudflare verified-bot category, if any
  bot_like INTEGER DEFAULT 0,  -- same user-agent heuristic as clicks
  purpose TEXT,                -- Sec-Purpose / Purpose header: set on browser prefetches and prerenders
  asn INTEGER                  -- client network (Cloudflare cf.asn)
);
CREATE INDEX IF NOT EXISTS landings_ts ON landings (ts);
CREATE INDEX IF NOT EXISTS landings_page ON landings (page);

-- Added 2026-11-03 (DLC-146): pages served to a verified agent browser (Muse and the like; index.js agentBrowser),
-- whose HTML got utm_source=<agent> on our links. Logged with the Web Bot Auth headers and the network, to learn
-- what each agent sends. No IP.
CREATE TABLE IF NOT EXISTS agent_pages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,            -- ISO 8601 UTC
  agent TEXT NOT NULL,         -- tag put on the links: muse | chatgpt-agent | signed-agent
  path TEXT NOT NULL,          -- path and query requested
  status INTEGER,
  user_agent TEXT,
  country TEXT,
  asn INTEGER,                 -- Cloudflare request.cf.asn
  as_org TEXT,                 -- request.cf.asOrganization
  verified_bot TEXT,
  signature_agent TEXT,        -- Signature-Agent header (Web Bot Auth key directory)
  signature_input TEXT         -- Signature-Input header (keyid, created, expires, tag)
);
CREATE INDEX IF NOT EXISTS agent_pages_ts ON agent_pages (ts);

-- Added 2026-11-05: one row per commission the Worker has alerted on (index.js "sale alerts"). CJ rows come from the
-- 30-minute commissions API poll, Awin rows from its Transaction Notifications callback. Never written to the repo.
CREATE TABLE IF NOT EXISTS sales (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,            -- ISO 8601 UTC, when the Worker first saw it
  network TEXT NOT NULL,       -- cj | awin
  txn_id TEXT NOT NULL,        -- CJ commissionId / Awin transactionId
  advertiser TEXT,
  commission REAL,             -- publisher commission (USD on CJ; Awin's own currency field otherwise)
  sale REAL,
  currency TEXT,
  sub_id TEXT,                 -- CJ shopperId (our sid) / Awin clickRef: <slug>.<click_id>, matches clicks.click_id
  event_date TEXT,
  UNIQUE (network, txn_id)
);

CREATE TABLE IF NOT EXISTS feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  ticket TEXT NOT NULL,        -- 8-char id returned to the sender
  kind TEXT NOT NULL,          -- missing_product | wrong_price | broken_link | wrong_spec | question | other
  page TEXT,
  message TEXT NOT NULL,
  agent TEXT,
  contact TEXT,
  method TEXT,                 -- GET or POST
  user_agent TEXT,
  country TEXT,
  reviewed_at TEXT             -- set by hand when acted on
);
CREATE INDEX IF NOT EXISTS feedback_ts ON feedback (ts);

-- DLC-182: one row per MCP tool call on /mcp (src/mcp.js). No IP and no chat text.
CREATE TABLE IF NOT EXISTS mcp_calls (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  tool TEXT NOT NULL,          -- search_products | check_codes | price_history
  args TEXT,                   -- the tool arguments as JSON, clipped to 500 chars
  results INTEGER,             -- how many products / codes / readings the call returned
  client TEXT,                 -- the client's own name when it sends one in _meta
  user_agent TEXT,
  country TEXT,
  verified_bot TEXT
);
CREATE INDEX IF NOT EXISTS mcp_calls_ts ON mcp_calls (ts);
