from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, Index
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import JSON as SAJSON

Base = declarative_base()

class Platform(Base):
    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sources = relationship("Source", back_populates="platform")

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=True)
    name = Column(String(200), nullable=False)
    source_type = Column(String(50), nullable=False)
    url = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)
    crawl_interval_minutes = Column(Integer, default=60)
    last_synced_at = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)
    records_last_sync = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    platform = relationship("Platform", back_populates="sources")

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True)
    code = Column(String(200), nullable=False, index=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    coupon_type = Column(String(50), nullable=True)
    discount_value = Column(Float, nullable=True)
    discount_currency = Column(String(10), nullable=True)
    discount_max = Column(Float, nullable=True)
    min_order_value = Column(Float, nullable=True)
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True, index=True)
    conditions = Column(Text, nullable=True)
    categories = Column(SAJSON, nullable=True)
    stores = Column(SAJSON, nullable=True)
    source_url = Column(Text, nullable=True)
    status = Column(String(50), default="NEW")
    verification_status = Column(String(50), default="UNVERIFIED")
    canonical_hash = Column(String(128), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CouponCheck(Base):
    __tablename__ = "coupon_checks"
    id = Column(Integer, primary_key=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow)
    method = Column(String(100), nullable=False)
    result = Column(String(50), nullable=False)
    evidence = Column(SAJSON, nullable=True)
    note = Column(Text, nullable=True)

class SyncJob(Base):
    __tablename__ = "sync_jobs"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False)
    fetched_count = Column(Integer, default=0)
    inserted_count = Column(Integer, default=0)
    updated_count = Column(Integer, default=0)
    error = Column(Text, nullable=True)

class CouponCondition(Base):
    __tablename__ = "coupon_conditions"
    id = Column(Integer, primary_key=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=False)
    cond_type = Column(String(100), nullable=False)
    value = Column(Text, nullable=True)
    raw = Column(SAJSON, nullable=True)

# Indexes: created via Index if needed; many fields already indexed
Index('ix_coupon_canonical', Coupon.canonical_hash)
