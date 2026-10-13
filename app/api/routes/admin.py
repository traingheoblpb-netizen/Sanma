from fastapi import APIRouter, Depends
from app.api.deps import admin_required
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.db import models

router = APIRouter()

@router.get('/')
def overview(authorized: bool = Depends(admin_required), db: Session = Depends(get_db)):
    total = db.query(models.Coupon).count()
    new = db.query(models.Coupon).filter(models.Coupon.status=='NEW').count()
    unverified = db.query(models.Coupon).filter(models.Coupon.verification_status=='UNVERIFIED').count()
    expired = db.query(models.Coupon).filter(models.Coupon.status=='EXPIRED').count()
    return {'total_coupons': total, 'new': new, 'unverified': unverified, 'expired': expired}

@router.get('/sync_jobs')
def list_sync_jobs(authorized: bool = Depends(admin_required), db: Session = Depends(get_db)):
    jobs = db.query(models.SyncJob).order_by(models.SyncJob.started_at.desc()).limit(50).all()
    return [ { 'id': j.id, 'status': j.status, 'started_at': j.started_at, 'finished_at': j.finished_at } for j in jobs ]

@router.get('/coupon_checks')
def list_checks(authorized: bool = Depends(admin_required), db: Session = Depends(get_db)):
    checks = db.query(models.CouponCheck).order_by(models.CouponCheck.checked_at.desc()).limit(200).all()
    return [ { 'id': c.id, 'coupon_id': c.coupon_id, 'result': c.result, 'checked_at': c.checked_at } for c in checks ]
