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

# Recurring Transactions

class RecurringTransactionBase(BaseModel):
    sourceType: str  # subscription, salary, rent, insurance, custom
    sourceItemId: Optional[UUID] = None
    targetAccountId: UUID
    amount: float
    dayOfMonth: int = Field(..., ge=1, le=31)
    label: str
    category: HistoryCategory
    icon: Optional[str] = None
    color: Optional[str] = None
    isActive: bool = True
    startDate: int  # Timestamp ms
    endDate: Optional[int] = None

class RecurringTransactionCreate(RecurringTransactionBase):
    pass

class RecurringTransactionUpdate(BaseModel):
    sourceType: Optional[str] = None
    sourceItemId: Optional[UUID] = None
    targetAccountId: Optional[UUID] = None
    amount: Optional[float] = None
    dayOfMonth: Optional[int] = Field(None, ge=1, le=31)
    label: Optional[str] = None
    category: Optional[HistoryCategory] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    isActive: Optional[bool] = None
    startDate: Optional[int] = None
    endDate: Optional[int] = None

class RecurringTransaction(RecurringTransactionBase):
    id: UUID
    lastProcessedDate: Optional[int] = None
    createdAt: int
    updatedAt: int

    class Config:
        from_attributes = True

class SyncResult(BaseModel):
    processedCount: int
    errors: list[str] = []

class MigrationResult(BaseModel):
    migratedCount: int
    skippedCount: int
    errors: list[str] = []
