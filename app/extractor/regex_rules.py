import re
from typing import List

# Very simple regex rules for coupon-like tokens
CODE_RE = re.compile(r"\b[A-Z0-9]{3,}(?:-[A-Z0-9]{2,})?\b")

CONTEXT_KEYWORDS = [
    'mã giảm giá', 'voucher', 'mã giảm', 'mã', 'coupon', 'discount', 'code'
]

def find_codes_in_text(text: str) -> List[str]:
    candidates = set(m.group(0) for m in CODE_RE.finditer(text))
    return list(candidates)
