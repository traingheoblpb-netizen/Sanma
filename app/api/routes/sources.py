from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.source_service import SourceService
from app.schemas.source import SourceOut, SourceBase
from app.api.deps import admin_required
from app.utils.security import is_safe_url
from app.db import models

router = APIRouter()

@router.get('/')
def list_sources(db: Session = Depends(get_db)):
    svc = SourceService(db)
    items = svc.list_sources()
    return [SourceOut.from_orm(i) for i in items]

@router.post('/')
def create_source(payload: SourceBase = Body(...), authorized: bool = Depends(admin_required), db: Session = Depends(get_db)):
    # Validate URL to avoid SSRF risks
    if payload.url and not is_safe_url(payload.url):
        raise HTTPException(status_code=400, detail='Unsafe or invalid URL')
    svc = SourceService(db)
    src = svc.create_source(payload.dict())
    return SourceOut.from_orm(src)

@router.patch('/{source_id}')
def patch_source(source_id: int, payload: dict, authorized: bool = Depends(admin_required), db: Session = Depends(get_db)):
    src = db.query(models.Source).filter(models.Source.id==source_id).first()
    if not src:
        raise HTTPException(status_code=404, detail='Source not found')
    allowed = {'name','enabled','crawl_interval_minutes'}
    for k,v in payload.items():
        if k in allowed:
            setattr(src, k, v)
    db.add(src)
    db.commit()
    db.refresh(src)
    return SourceOut.from_orm(src)

@router.post('/{source_id}/sync')
def sync_source(source_id: int, authorized: bool = Depends(admin_required), db: Session = Depends(get_db)):
    # For safety, MVP requires file import. Remote sync not implemented.
    raise HTTPException(status_code=501, detail='Manual sync not implemented for remote sources in MVP')
