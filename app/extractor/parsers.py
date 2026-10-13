from bs4 import BeautifulSoup
import json
from typing import List, Dict, Any
from .regex_rules import find_codes_in_text

def parse_html_for_coupons(html: str, source_url: str = None) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, 'lxml')
    texts = []
    # Collect text from promotional sections heuristically
    for el in soup.find_all(['p','li','span','div','h1','h2','h3']):
        texts.append(el.get_text(separator=' ', strip=True))
    joined = '\n'.join(filter(None, texts))
    codes = find_codes_in_text(joined)
    results = []
    for c in codes:
        results.append({
            'code': c,
            'raw_text': joined,
            'source_url': source_url
        })
    # Also try JSON-LD
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            # naive search for coupon fields
            if isinstance(data, dict):
                if 'offers' in data:
                    # not detailed here
                    pass
        except Exception:
            continue
    return results

def parse_json_for_coupons(obj: Any, source_url: str = None) -> List[Dict[str, Any]]:
    results = []
    # Walk JSON to find strings that look like codes
    def walk(o):
        if isinstance(o, dict):
            for k,v in o.items():
                walk(v)
        elif isinstance(o, list):
            for item in o:
                walk(item)
        elif isinstance(o, str):
            for code in find_codes_in_text(o):
                results.append({'code': code, 'raw_text': o, 'source_url': source_url})
    walk(obj)
    return results
