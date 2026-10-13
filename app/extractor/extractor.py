import json
from typing import List, Dict, Any
from .parsers import parse_html_for_coupons, parse_json_for_coupons

def extract_from_text(text: str, source_url: str = None) -> List[Dict[str, Any]]:
    # Try JSON
    try:
        obj = json.loads(text)
        return parse_json_for_coupons(obj, source_url)
    except Exception:
        pass
    # Try HTML
    return parse_html_for_coupons(text, source_url)
