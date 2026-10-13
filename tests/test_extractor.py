import pytest
from app.extractor.extractor import extract_from_text

HTML_SAMPLE = """
<div>
  <p>Nhận mã giảm giá: SALE50 cho đơn hàng trên 200000</p>
</div>
"""

def test_extract_html():
    results = extract_from_text(HTML_SAMPLE)
    assert any(r['code'] == 'SALE50' for r in results)
