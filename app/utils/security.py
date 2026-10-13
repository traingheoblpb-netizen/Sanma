from urllib.parse import urlparse
import ipaddress

DISALLOWED_HOSTS = ['localhost']

def is_safe_url(url: str) -> bool:
    if not url:
        return False
    try:
        p = urlparse(url)
        if p.scheme not in ('http','https'):
            return False
        host = p.hostname
        if not host:
            return False
        # Reject obvious local names
        if host.lower() in DISALLOWED_HOSTS or host.lower().endswith('.local'):
            return False
        # If host is an IP literal, ensure it's not private
        try:
            ip = ipaddress.ip_address(host)
            if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_multicast:
                return False
        except ValueError:
            # not an IP, assume DNS name — cannot fully validate without DNS lookup
            # but reject single-label hostnames
            if '.' not in host:
                return False
        return True
    except Exception:
        return False
