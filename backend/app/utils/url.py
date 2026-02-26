from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import hashlib

def normalize_url(url: str) -> str:
    """Remove tracking parameters and normalize URL"""
    parsed = urlparse(url)
    # Remove utm_* parameters
    params = parse_qs(parsed.query)
    clean_params = {k: v for k, v in params.items() if not k.startswith('utm_')}
    query = urlencode(clean_params, doseq=True)
    return urlunparse(parsed._replace(query=query))

def content_hash(url: str, title: str) -> str:
    """Generate hash for deduplication"""
    combined = normalize_url(url) + title
    return hashlib.sha256(combined.encode()).hexdigest()
