from io import BytesIO
from app.collectors.generic_collector import GenericCollector

CSV_SAMPLE = 'code,discount_value,min_order_value\nTEST10,10,100000\n'

def test_import_csv():
    coll = GenericCollector({'name':'t'}, file_bytes=CSV_SAMPLE.encode('utf-8'))
    items = coll.collect()
    assert len(items) == 1
    assert items[0]['code'] == 'TEST10'
