from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class CouponBase(BaseModel):
    code: str
    platform_code: Optional[str]
    coupon_type: Optional[str]
    discount_value: Optional[float]
    discount_currency: Optional[str]
    discount_max: Optional[float]
    min_order_value: Optional[float]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    conditions: Optional[str]
    categories: Optional[Any]
    stores: Optional[Any]
    source_url: Optional[str]

class CouponCreate(CouponBase):
    raw_evidence: Optional[Any]
    confidence: Optional[float] = Field(default=0.0)

class CouponOut(CouponBase):
    id: int
    status: str
    verification_status: str
    canonical_hash: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
