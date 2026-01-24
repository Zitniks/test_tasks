import random
import string
from urllib.parse import urlparse

import httpx


def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def validate_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return False

        if parsed.scheme not in ['http', 'https']:
            return False

        try:
            resp = httpx.head(url, timeout=5.0, follow_redirects=True)
            return resp.status_code < 400
        except Exception:
            try:
                resp = httpx.get(url, timeout=5.0, follow_redirects=True)
                return resp.status_code < 400
            except Exception:
                return False
    except Exception:
        return False


def validate_short_code(code: str) -> bool:
    if not code:
        return False
    if len(code) < 3 or len(code) > 50:
        return False
    allowed = string.ascii_letters + string.digits + '-_'
    return all(c in allowed for c in code)
