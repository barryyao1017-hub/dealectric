"""One-time Google OAuth sign-in for the Microsoft Advertising API (Ad Insight keyword volumes, DLC-168).

The Microsoft Ads account signs in with Google (barrryyao@gmail.com), so API calls carry a Google access token plus
the header IdentityProvider=Google (learn.microsoft.com/advertising/guides/authentication-oauth-consent). This script
runs a loopback server, prints the consent URL, waits for the redirect and stores the refresh token in the keychain
as `google-oauth-msads-refresh-token`. Barry clicks Allow on Google's consent page; nothing secret is printed.

Keychain items read: google-oauth-msads-client-id, google-oauth-msads-client-secret.
The OAuth app is in testing mode, so the refresh token lasts 7 days; re-run this when it expires.
"""
import http.server, json, secrets, subprocess, sys, urllib.parse, urllib.request

def kc(name):
    return subprocess.run(["security", "find-generic-password", "-s", name, "-w"], capture_output=True,
                          text=True, check=True).stdout.strip()

def main():
    cid, secret = kc("google-oauth-msads-client-id"), kc("google-oauth-msads-client-secret")
    state = secrets.token_urlsafe(16)
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(self.path).query))
            if "code" in q or "error" in q:
                got.update(q)
            self.send_response(200); self.end_headers()
            self.wfile.write(b"Done. You can close this tab.")
        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    redirect = f"http://127.0.0.1:{srv.server_port}"
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid, "response_type": "code", "redirect_uri": redirect, "scope": "openid profile email",
        "access_type": "offline", "prompt": "consent", "state": state, "login_hint": "barrryyao@gmail.com"})
    print("CONSENT_URL", url, flush=True)
    while not got:
        srv.handle_request()
    if got.get("state") != state or "code" not in got:
        sys.exit(f"consent failed: {got.get('error', 'state mismatch')}")
    body = urllib.parse.urlencode({"code": got["code"], "client_id": cid, "client_secret": secret,
                                   "redirect_uri": redirect, "grant_type": "authorization_code"}).encode()
    tok = json.loads(urllib.request.urlopen("https://oauth2.googleapis.com/token", body, timeout=30).read())
    if "refresh_token" not in tok:
        sys.exit("no refresh token returned")
    subprocess.run(["security", "add-generic-password", "-U", "-a", "dealectric", "-s",
                    "google-oauth-msads-refresh-token", "-w", tok["refresh_token"]], check=True)
    print("refresh token stored")

if __name__ == "__main__":
    main()
