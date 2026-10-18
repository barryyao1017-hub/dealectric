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
  utm_source TEXT              -- parsed utm_source, for grouping clicks by assistant
);
-- Added 2026-10-18 for databases created before these columns existed (each fails harmlessly once applied):
-- ALTER TABLE clicks ADD COLUMN kind TEXT DEFAULT 'redirect';
-- ALTER TABLE clicks ADD COLUMN query TEXT;
-- ALTER TABLE clicks ADD COLUMN utm_source TEXT;
CREATE INDEX IF NOT EXISTS clicks_ts ON clicks (ts);
CREATE INDEX IF NOT EXISTS clicks_slug ON clicks (slug);
CREATE INDEX IF NOT EXISTS clicks_click_id ON clicks (click_id);

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
