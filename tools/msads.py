"""Microsoft Advertising Ad Insight: Bing search counts for up to 1,000 keywords per call (DLC-168).

Auth: Google OAuth (the Ads login is barrryyao@gmail.com via Google), header IdentityProvider=Google. Keychain:
msads-developer-token, google-oauth-msads-client-id/-client-secret/-refresh-token (tools/msads_auth.py makes the
last one; in testing mode it lasts 7 days). Account: customer 255121540, ad account 187335032 (no campaigns).
"""
import datetime as dt, json, subprocess, time, urllib.parse, urllib.request, urllib.error

CUSTOMER_ID, ACCOUNT_ID = "255121540", "187335032"
URL = "https://adinsight.api.bingads.microsoft.com/AdInsight/v13/HistoricalSearchCount/Query"
DEVICES = ["Computers", "Smartphones", "Tablets"]
_tok = {"value": None, "exp": 0}


def kc(name: str) -> str:
    return subprocess.run(["security", "find-generic-password", "-s", name, "-w"], capture_output=True, text=True,
                          check=True).stdout.strip()


def access_token() -> str:
    if _tok["value"] and time.time() < _tok["exp"] - 60:
        return _tok["value"]
    body = urllib.parse.urlencode({"client_id": kc("google-oauth-msads-client-id"),
                                   "client_secret": kc("google-oauth-msads-client-secret"),
                                   "refresh_token": kc("google-oauth-msads-refresh-token"),
                                   "grant_type": "refresh_token"}).encode()
    r = json.loads(urllib.request.urlopen("https://oauth2.googleapis.com/token", body, timeout=30).read())
    # Microsoft accepts the Google ID token or access token depending on setup; keep both.
    _tok.update(value=r.get("id_token") or r["access_token"], access=r["access_token"], exp=time.time() + r["expires_in"])
    return _tok["value"]


def _d(d: dt.date) -> dict:
    return {"Day": d.day, "Month": d.month, "Year": d.year}


def search_counts(keywords: list[str], months: int = 3, use_access: bool = False) -> dict[str, int | None]:
    """Sum of monthly US English search counts over the last `months` complete months, all devices. None = no data."""
    end = dt.date.today().replace(day=1) - dt.timedelta(days=1)
    start = (end.replace(day=1) - dt.timedelta(days=31 * (months - 1))).replace(day=1)
    req = {"Keywords": keywords, "Language": "English", "PublisherCountries": ["US"], "StartDate": _d(start),
           "EndDate": _d(end), "TimePeriodRollup": "Monthly", "Devices": DEVICES}
    tok = access_token()
    if use_access:
        tok = _tok["access"]
    h = {"Authorization": f"Bearer {tok}", "DeveloperToken": kc("msads-developer-token"), "CustomerId": CUSTOMER_ID,
         "CustomerAccountId": ACCOUNT_ID, "IdentityProvider": "Google", "Content-Type": "application/json"}
    try:
        r = json.loads(urllib.request.urlopen(urllib.request.Request(URL, json.dumps(req).encode(), h), timeout=120).read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read()[:600].decode(errors='replace')}")
    # Match rows by the keyword Microsoft echoes, not by position: in 1,000-keyword batches rows can be missing,
    # which shifted every later count (2026-11-05: "power bank" read None in a batch, 66,119 alone).
    items = r.get("KeywordSearchCounts") or []
    by_kw = {}
    for item in items:
        if not item or not item.get("Keyword"):
            continue
        tot, seen = 0, False
        for dev in item.get("SearchCountsByAttributes") or []:
            for p in dev.get("HistoricalSearchCounts") or []:
                tot += int(p["SearchCount"]); seen = True
        by_kw[item["Keyword"].strip().lower()] = tot if seen else None
    return {kw: by_kw.get(kw.strip().lower()) for kw in keywords}


if __name__ == "__main__":
    import sys
    kws = sys.argv[1:] or ["power bank", "portable power station", "travel router with vpn"]
    for mode in (False, True):
        try:
            print("access" if mode else "id", search_counts(kws, use_access=mode)); break
        except RuntimeError as e:
            print("access" if mode else "id", e)
