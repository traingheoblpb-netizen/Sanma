from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SourceBase(BaseModel):
    name: str
    source_type: str
    url: Optional[str]
    platform_code: Optional[str]
    crawl_interval_minutes: Optional[int] = 60

class SourceOut(SourceBase):
    id: int
    enabled: bool
    last_synced_at: Optional[datetime]
    last_error: Optional[str]
    records_last_sync: int

    class Config:
        orm_mode = True
