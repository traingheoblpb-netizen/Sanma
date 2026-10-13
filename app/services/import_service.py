import io
from typing import Tuple
from app.collectors.generic_collector import GenericCollector
from app.services.coupon_service import CouponService
from app.db import models

class ImportService:
    def __init__(self, db):
        self.db = db
        self.coupon_svc = CouponService(db)

    def import_file(self, source: models.Source, file_bytes: bytes) -> dict:
        coll = GenericCollector({'name': source.name}, file_bytes=file_bytes)
        items = coll.collect()
        inserted = 0
        updated = 0
        errors = 0
        for item in items:
            try:
                coupon, created = self.coupon_svc.upsert_coupon(item, source)
                if created:
                    inserted += 1
                else:
                    updated += 1
            except Exception:
                errors += 1
        return {'total': len(items), 'inserted': inserted, 'updated': updated, 'errors': errors}
