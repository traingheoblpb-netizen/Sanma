from sqlalchemy.orm import Session
from app.db import models
from app.normalizer.normalizer import normalize_coupon
from typing import Dict, Any, Tuple
from datetime import datetime

class CouponService:
    def __init__(self, db: Session):
        self.db = db

    def upsert_coupon(self, raw: Dict[str, Any], source: models.Source) -> Tuple[models.Coupon, bool]:
        normalized = normalize_coupon(raw)
        # Defensive: require code
        if not normalized.get('code'):
            raise ValueError('Missing coupon code')
        existing = self.db.query(models.Coupon).filter(models.Coupon.canonical_hash == normalized['canonical_hash']).first()
        now = datetime.utcnow()
        if existing:
            updated = False
            # update fields if newer or missing
            if normalized.get('discount_value') is not None and existing.discount_value != normalized.get('discount_value'):
                existing.discount_value = normalized.get('discount_value'); updated = True
            if normalized.get('discount_max') is not None and existing.discount_max != normalized.get('discount_max'):
                existing.discount_max = normalized.get('discount_max'); updated = True
            if normalized.get('min_order_value') is not None and existing.min_order_value != normalized.get('min_order_value'):
                existing.min_order_value = normalized.get('min_order_value'); updated = True
            if normalized.get('conditions') and existing.conditions != normalized.get('conditions'):
                existing.conditions = normalized.get('conditions'); updated = True
            if normalized.get('source_url') and existing.source_url != normalized.get('source_url'):
                existing.source_url = normalized.get('source_url'); updated = True
            if updated:
                existing.updated_at = now
                self.db.add(existing)
                self.db.commit()
                self.db.refresh(existing)
            return existing, False
        # insert new
        coupon = models.Coupon(
            code=normalized['code'],
            platform_id=None,
            source_id=source.id if source else None,
            coupon_type=normalized.get('coupon_type'),
            discount_value=normalized.get('discount_value'),
            discount_currency=normalized.get('discount_currency'),
            discount_max=normalized.get('discount_max'),
            min_order_value=normalized.get('min_order_value'),
            start_at=normalized.get('start_at'),
            end_at=normalized.get('end_at'),
            conditions=normalized.get('conditions'),
            categories=normalized.get('categories'),
            stores=normalized.get('stores'),
            source_url=normalized.get('source_url'),
            canonical_hash=normalized.get('canonical_hash')
        )
        self.db.add(coupon)
        self.db.commit()
        self.db.refresh(coupon)
        return coupon, True
