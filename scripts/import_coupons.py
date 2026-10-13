import sys
from pathlib import Path
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import models
from app.collectors.generic_collector import GenericCollector

def import_file(source_id: int, file_path: str):
    db: Session = SessionLocal()
    try:
        src = db.query(models.Source).filter(models.Source.id==source_id).first()
        if not src:
            print('Source not found')
            return
        with open(file_path, 'rb') as f:
            content = f.read()
        coll = GenericCollector({'name': src.name}, file_bytes=content)
        items = coll.collect()
        inserted = 0
        for item in items:
            # naive insert
            from app.services.coupon_service import CouponService
            svc = CouponService(db)
            svc.upsert_coupon(item, src)
            inserted += 1
        print('Inserted', inserted)
    finally:
        db.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python scripts/import_coupons.py <source_id> <file_path>')
    else:
        import_file(int(sys.argv[1]), sys.argv[2])
