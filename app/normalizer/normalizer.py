from datetime import datetime
from typing import Dict, Any, Optional
import hashlib
import json
import re
import pytz

TZ = pytz.timezone('Asia/Ho_Chi_Minh')

def normalize_code(code: str) -> str:
    if not code:
        return ''
    # Remove surrounding whitespace and convert to upper
    return re.sub(r"\s+", "", code).upper()

def canonical_hash_for_coupon(coupon: Dict[str, Any]) -> str:
    # Use platform, code, coupon_type, min_order_value, end_at
    parts = [coupon.get('platform_code') or '', coupon.get('code') or '', coupon.get('coupon_type') or '']
    parts.append(str(coupon.get('min_order_value') or ''))
    parts.append(str(coupon.get('end_at') or ''))
    key = '|'.join(parts)
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def to_utc(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        local = TZ.localize(dt)
        return local.astimezone(pytz.UTC)
    return dt.astimezone(pytz.UTC)

def normalize_coupon(raw: Dict[str, Any]) -> Dict[str, Any]:
    c = {}
    c['code'] = normalize_code(raw.get('code'))
    c['platform_code'] = raw.get('platform_code')
    c['coupon_type'] = raw.get('coupon_type')
    # numeric fields
    for k in ('discount_value','discount_max','min_order_value'):
        v = raw.get(k)
        try:
            if v is None or v == '':
                c[k] = None
            else:
                c[k] = float(v)
        except Exception:
            c[k] = None
    # parse dates if provided as ISO strings
    for k in ('start_at','end_at'):
        v = raw.get(k)
        if not v:
            c[k] = None
        else:
            try:
                dt = datetime.fromisoformat(v)
                c[k] = to_utc(dt)
            except Exception:
                c[k] = None
    c['conditions'] = raw.get('conditions')
    c['categories'] = raw.get('categories')
    c['stores'] = raw.get('stores')
    c['source_url'] = raw.get('source_url')
    c['raw_evidence'] = raw.get('raw_text') or raw.get('raw_evidence')
    c['confidence'] = float(raw.get('confidence') or 0.0)
    c['canonical_hash'] = canonical_hash_for_coupon(c)
    return c
