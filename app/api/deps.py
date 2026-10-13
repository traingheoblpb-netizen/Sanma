from fastapi import Header, HTTPException, Depends
from app.config import settings

def admin_required(x_admin_token: str = Header(None)) -> bool:
    """Dependency to require admin token passed in X-Admin-Token header.
    If ADMIN_TOKEN is empty (not configured), deny by default for safety.
    """
    if not settings.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Admin token not configured")
    if not x_admin_token or x_admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return True
