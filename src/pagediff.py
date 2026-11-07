"""DLC-87 / DLC-94(a): tell a real page edit from the daily date bump.

The daily cart check rewrites "last passed <date>" and "last check <date>" on every coded page, so a byte compare calls
those pages changed every day. Bing asks IndexNow for changed URLs only, and a sitemap lastmod that moves daily tells
crawlers nothing. A page counts as changed when it differs after every date is blanked: a new price, code, product or
copy line still shows.
"""
import re

_DATE = re.compile(rb"\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)?"
                   rb"|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.? \d{1,2}(?:, \d{4})?\b")


def strip_dates(b: bytes) -> bytes:
    return _DATE.sub(b"<date>", b)


def real_change(old: bytes | None, new: bytes | None) -> bool:
    """True for a new or removed page, or one that still differs once dates are blanked."""
    if old is None or new is None:
        return old is not new
    return old != new and strip_dates(old) != strip_dates(new)
