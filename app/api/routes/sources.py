from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.source_service import SourceService
from app.schemas.source import SourceOut, SourceBase
from fastapi import Body

router = APIRouter()

@router.get('/')
def list_sources(db: Session = Depends(get_db)):
    svc = SourceService(db)
    items = svc.list_sources()
    return [SourceOut.from_orm(i) for i in items]

@router.post('/')
def create_source(payload: SourceBase = Body(...), db: Session = Depends(get_db)):
    svc = SourceService(db)
    src = svc.create_source(payload.dict())
    return SourceOut.from_orm(src)

@router.patch('/{source_id}')
def patch_source(source_id: int, payload: dict, db: Session = Depends(get_db)):
    src = db.query('')
    # simplified for MVP
    raise HTTPException(status_code=501, detail='Not implemented in MVP')

@router.post('/{source_id}/sync')
def sync_source(source_id: int, db: Session = Depends(get_db)):
    # For safety, do not fetch external URL in MVP. Require admin to upload file via import endpoint.
    raise HTTPException(status_code=501, detail='Manual sync not implemented for remote sources in MVP')
