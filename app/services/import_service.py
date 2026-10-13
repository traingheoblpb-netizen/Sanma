import io
import csv
import json
from typing import Tuple
from app.collectors.generic_collector import GenericCollector
from app.services.coupon_service import CouponService
from app.db import models

MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB
MAX_ROWS = 5000

class ImportService:
    def __init__(self, db):
        self.db = db
        self.coupon_svc = CouponService(db)

    def import_file(self, source: models.Source, file_bytes: bytes) -> dict:
        if not file_bytes or len(file_bytes) == 0:
            return {'error': 'empty file'}
        if len(file_bytes) > MAX_FILE_BYTES:
            return {'error': 'file too large'}
        # Use GenericCollector to parse CSV or JSON
        coll = GenericCollector({'name': source.name}, file_bytes=file_bytes)
        try:
            items = coll.collect()
        except Exception as e:
            return {'error': 'parse_error', 'detail': str(e)}
        if not isinstance(items, list):
            return {'error': 'invalid content'}
        if len(items) > MAX_ROWS:
            return {'error': 'too_many_rows', 'rows': len(items)}
        inserted = 0
        updated = 0
        errors = 0
        for item in items:
            try:
                # Basic validation: must have code
                if 'code' not in item or not item.get('code'):
                    errors += 1
                    continue
                coupon, created = self.coupon_svc.upsert_coupon(item, source)
                if created:
                    inserted += 1
                else:
                    updated += 1
            except Exception:
                errors += 1
        # update source stats
        source.records_last_sync = (source.records_last_sync or 0) + len(items)
        self.db.add(source)
        self.db.commit()
        return {'total': len(items), 'inserted': inserted, 'updated': updated, 'errors': errors}
