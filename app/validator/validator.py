from datetime import datetime
from typing import Dict, Any

def determine_status(normalized: Dict[str, Any]) -> str:
    # Determine NEW/UNVERIFIED/ACTIVE/EXPIRED/CONDITIONAL/UNKNOWN
    now = datetime.utcnow()
    start = normalized.get('start_at')
    end = normalized.get('end_at')
    if end and end < now:
        return 'EXPIRED'
    # If start in future
    if start and start > now:
        return 'UNVERIFIED'
    # If code exists but no conditions
    if not normalized.get('raw_evidence'):
        return 'UNVERIFIED'
    return 'NEW'

def make_check_record(coupon_id: int, method: str, result: str, evidence: dict = None, note: str = None) -> Dict[str, Any]:
    return {
        'coupon_id': coupon_id,
        'method': method,
        'result': result,
        'evidence': evidence or {},
        'note': note
    }
