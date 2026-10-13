import hashlib
import re
from datetime import datetime, timezone, timedelta
from decimal import Decimal, InvalidOperation
from typing import Optional

try:
    from zoneinfo import ZoneInfo
    VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
except Exception:
    VN_TZ = timezone(timedelta(hours=7))


def normalize_code(code: str) -> str:
    if not code:
        return ""
    return re.sub(r"\s+", "", code.strip()).upper()


def code_hash(code: str, platform_name: str) -> str:
    raw = f"{normalize_code(code)}|{(platform_name or '').strip().lower()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def normalize_decimal(value) -> Optional[Decimal]:
    if value is None or value == "":
        return None
    if isinstance(value, Decimal):
        return value
    try:
        s = str(value).replace(".", "").replace(",", "").strip()
        s = s.replace("đ", "").replace("VND", "").replace("vnd", "").strip()
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return None


def normalize_datetime(value) -> Optional[datetime]:
    """Chấp nhận datetime, timestamp (s), ISO string. Trả về datetime naive UTC."""
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        try:
            dt = datetime.fromtimestamp(float(value), tz=VN_TZ)
        except (OSError, ValueError):
            return None
    else:
        s = str(value).strip()
        if not s:
            return None
        try:
            if s.endswith("Z"):
                s = s[:-1] + "+00:00"
            dt = datetime.fromisoformat(s)
        except ValueError:
            return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=VN_TZ)

    if hasattr(dt, "astimezone"):
        try:
            return dt.astimezone(timezone.utc).replace(tzinfo=None)
        except Exception:
            pass
    return dt.replace(tzinfo=None)


def normalize_platform(raw: str) -> str:
    if not raw:
        return "unknown"
    r = raw.strip().lower()
    mapping = {
        "shopee": "shopee",
        "shopee vn": "shopee",
        "shopee vietnam": "shopee",
        "lazada": "lazada",
        "lazada vn": "lazada",
        "tiki": "tiki",
        "tiktok": "tiktok",
        "tiktok shop": "tiktok",
    }
    return mapping.get(r, r)
