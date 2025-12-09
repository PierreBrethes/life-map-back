from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.enums import HistoryCategory

class HistoryEntryBase(BaseModel):
    itemId: UUID
    date: int
    value: float
    label: str
    category: HistoryCategory

class HistoryEntryCreate(HistoryEntryBase):
    pass

class HistoryEntryUpdate(BaseModel):
    date: Optional[int] = None
    value: Optional[float] = None
    label: Optional[str] = None
    category: Optional[HistoryCategory] = None

class HistoryEntry(HistoryEntryBase):
    id: UUID

    class Config:
        from_attributes = True

class SubscriptionBase(BaseModel):
    itemId: UUID
    name: str
    amount: float
    billingDay: int = Field(..., ge=1, le=31)
    icon: Optional[str] = None
    color: Optional[str] = None
    isActive: bool = True

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    billingDay: Optional[int] = Field(None, ge=1, le=31)
    icon: Optional[str] = None
    color: Optional[str] = None
    isActive: Optional[bool] = None

class Subscription(SubscriptionBase):
    id: UUID

    class Config:
        from_attributes = True
