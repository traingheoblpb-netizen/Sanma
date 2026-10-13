from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.import_service import ImportService
from app.services.source_service import SourceService
from app.schemas.coupon import CouponOut
from app.db import models

router = APIRouter()

@router.get('/')
def list_coupons(q: Optional[str] = Query(None), page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    query = db.query(models.Coupon)
    if q:
        like = f"%{q}%"
        query = query.filter(models.Coupon.code.ilike(like) | models.Coupon.conditions.ilike(like))
    total = query.count()
    items = query.order_by(models.Coupon.updated_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    return { 'total': total, 'page': page, 'page_size': page_size, 'items': [CouponOut.from_orm(i) for i in items] }

@router.get('/{coupon_id}')
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    c = db.query(models.Coupon).filter(models.Coupon.id==coupon_id).first()
    if not c:
        raise HTTPException(status_code=404, detail='Coupon not found')
    return CouponOut.from_orm(c)

@router.post('/import')
def import_coupons(source_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    source = db.query(models.Source).filter(models.Source.id==source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail='Source not found')
    content = file.file.read()
    svc = ImportService(db)
    result = svc.import_file(source, content)
    return result

@router.post('/{coupon_id}/verify')
def verify_coupon(coupon_id: int, db: Session = Depends(get_db)):
    c = db.query(models.Coupon).filter(models.Coupon.id==coupon_id).first()
    if not c:
        raise HTTPException(status_code=404, detail='Coupon not found')
    # For MVP, verification just marks UNVERIFIED->NEW if evidence exists
    if c.verification_status == 'UNVERIFIED' and c.conditions:
        c.verification_status = 'ACTIVE'
    else:
        c.verification_status = 'UNVERIFIED'
    db.add(c)
    db.commit()
    return {'coupon_id': c.id, 'verification_status': c.verification_status}
