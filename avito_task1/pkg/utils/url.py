"""URL validation and short code generation."""

import random
import string
from urllib.parse import urlparse

import httpx


def generate_short_code(length: int = 6) -> str:
    """Generate a random alphanumeric short code of given length."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def validate_url(url: str, timeout: float = 5.0) -> bool:
    """Return True if url is http(s) and reachable (HEAD or GET < 400)."""
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return False
        if parsed.scheme not in ('http', 'https'):
            return False
    except (ValueError, AttributeError):
        return False

    for method in ('head', 'get'):
        try:
            if method == 'head':
                resp = httpx.head(url, timeout=timeout, follow_redirects=True)
            else:
                resp = httpx.get(url, timeout=timeout, follow_redirects=True)
            return resp.status_code < 400
        except (httpx.HTTPError, OSError):
            continue
    return False


def validate_short_code(code: str) -> bool:
    """Return True if code is 3–50 chars, alphanumeric plus hyphen/underscore."""
    if not code:
        return False
    if len(code) < 3 or len(code) > 50:
        return False
    allowed = string.ascii_letters + string.digits + '-_'
    return all(c in allowed for c in code)
