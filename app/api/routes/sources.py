from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.import_service import ImportService
from app.schemas.coupon import CouponOut
from app.db import models
from app.api.deps import admin_required
from datetime import datetime

router = APIRouter()

@router.get('/')
def list_coupons(
    q: Optional[str] = Query(None),
    platform: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    coupon_type: Optional[str] = Query(None),
    min_discount: Optional[float] = Query(None),
    max_min_order: Optional[float] = Query(None),
    expires_before: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    sort: Optional[str] = Query('updated'),
    db: Session = Depends(get_db)
):
    query = db.query(models.Coupon)
    if q:
        like = f"%{q}%"
        query = query.filter(models.Coupon.code.ilike(like) | models.Coupon.conditions.ilike(like) | models.Coupon.source_url.ilike(like))
    if platform:
        query = query.join(models.Platform, models.Coupon.platform_id == models.Platform.id).filter(models.Platform.code == platform)
    if status:
        query = query.filter(models.Coupon.status == status)
    if coupon_type:
        query = query.filter(models.Coupon.coupon_type == coupon_type)
    if min_discount is not None:
        query = query.filter(models.Coupon.discount_value >= min_discount)
    if max_min_order is not None:
        query = query.filter(models.Coupon.min_order_value <= max_min_order)
    if expires_before:
        try:
            dt = datetime.fromisoformat(expires_before)
            query = query.filter(models.Coupon.end_at != None).filter(models.Coupon.end_at <= dt)
        except Exception:
            raise HTTPException(status_code=400, detail='Invalid expires_before datetime')
    total = query.count()
    if sort == 'saving':
        query = query.order_by(models.Coupon.discount_value.desc())
    elif sort == 'expires':
        query = query.order_by(models.Coupon.end_at.asc())
    else:
        query = query.order_by(models.Coupon.updated_at.desc())
    items = query.offset((page-1)*page_size).limit(page_size).all()
    return { 'total': total, 'page': page, 'page_size': page_size, 'items': [CouponOut.from_orm(i) for i in items] }

@router.get('/{coupon_id}')
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    c = db.query(models.Coupon).filter(models.Coupon.id==coupon_id).first()
    if not c:
        raise HTTPException(status_code=404, detail='Coupon not found')
    return CouponOut.from_orm(c)

@router.post('/import')
def import_coupons(
    source_id: int,
    file: UploadFile = File(...),
    _admin: bool = Depends(admin_required),
    db: Session = Depends(get_db)
):
    source = db.query(models.Source).filter(models.Source.id==source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail='Source not found')
    content = file.file.read()
    svc = ImportService(db)
    result = svc.import_file(source, content)
    if result.get('error'):
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post('/{coupon_id}/verify')
def verify_coupon(coupon_id: int, _admin: bool = Depends(admin_required), db: Session = Depends(get_db)):
    c = db.query(models.Coupon).filter(models.Coupon.id==coupon_id).first()
    if not c:
        raise HTTPException(status_code=404, detail='Coupon not found')
    if c.verification_status == 'UNVERIFIED' and c.conditions:
        c.verification_status = 'ACTIVE'
    else:
        c.verification_status = 'UNVERIFIED'
    db.add(c)
    db.commit()
    return {'coupon_id': c.id, 'verification_status': c.verification_status}
