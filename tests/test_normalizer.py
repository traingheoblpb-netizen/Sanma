from app.normalizer.normalizer import normalize_coupon

def test_normalize_basic():
    raw = {'code': ' sale50 ', 'discount_value': '50', 'min_order_value': '200000'}
    n = normalize_coupon(raw)
    assert n['code'] == 'SALE50'
    assert isinstance(n['discount_value'], float) or n['discount_value'] is None
