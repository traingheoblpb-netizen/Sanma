from sqlalchemy.orm import Session
from app.db import models

class SourceService:
    def __init__(self, db: Session):
        self.db = db

    def list_sources(self):
        return self.db.query(models.Source).all()

    def create_source(self, data: dict):
        src = models.Source(
            platform_id=None,
            name=data['name'],
            source_type=data['source_type'],
            url=data.get('url'),
            enabled=data.get('enabled', True),
            crawl_interval_minutes=data.get('crawl_interval_minutes', 60)
        )
        self.db.add(src)
        self.db.commit()
        self.db.refresh(src)
        return src
