// Serves one recorded search result set per unguessable id (/<24 hex>), read from D1 replay_pages, for the fast
// loop's open-page replay. noindex, linked from nowhere; rows are deleted after each chat (growth/evals/fastloop.py).
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const id = url.pathname.replace(/^\/+|\/+$/g, "");
    const headers = { "X-Robots-Tag": "noindex, nofollow, noarchive", "Cache-Control": "no-store" };
    const row = /^[a-f0-9]{24}$/.test(id) ? await env.DB.prepare("SELECT html FROM replay_pages WHERE id = ?").bind(id).first() : null;
    if (!row) return new Response("Not found\n", { status: 404, headers: { ...headers, "Content-Type": "text/plain; charset=utf-8" } });
    await env.DB.prepare("UPDATE replay_pages SET fetches = fetches + 1, last_ua = ? WHERE id = ?")
      .bind((request.headers.get("user-agent") || "").slice(0, 200), id).run();
    return new Response(row.html, { headers: { ...headers, "Content-Type": "text/html; charset=utf-8" } });
  },
};
