from fastapi import APIRouter
from app.db.session import engine

router = APIRouter()

@router.get('/')
def health():
    try:
        conn = engine.connect()
        conn.close()
        return {'status': 'ok'}
    except Exception as e:
        return {'status': 'error', 'detail': str(e)}
