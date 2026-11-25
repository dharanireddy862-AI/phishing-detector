from urllib.parse import urlparse

SUSPICIOUS_TLDS = {".xyz", ".top", ".click", ".gq", ".tk", ".ml", ".ga", ".cf", ".co"}
SUSPICIOUS_WORDS = {"login", "verify", "update", "secure", "account", "free", "bonus", "signin", "banking"}


def extract_url_features(url: str) -> dict:
    url_str = str(url).strip()
    lower_url = url_str.lower()
    parsed = urlparse(lower_url if "://" in lower_url else f"http://{lower_url}")
    host = parsed.hostname or ""

    tld = ""
    if "." in host:
        tld = "." + host.rsplit(".", 1)[-1]

    has_ip = host.replace(".", "").isdigit()

    return {
        "url_length": len(url_str),
        "host_length": len(host),
        "dot_count": url_str.count("."),
        "hyphen_count": url_str.count("-"),
        "at_count": url_str.count("@"),
        "slash_count": url_str.count("/"),
        "digit_count": sum(ch.isdigit() for ch in url_str),
        "uses_https": int(parsed.scheme == "https"),
        "has_ip_host": int(has_ip),
        "suspicious_tld": int(tld in SUSPICIOUS_TLDS),
        "suspicious_word_count": sum(word in lower_url for word in SUSPICIOUS_WORDS),
    }