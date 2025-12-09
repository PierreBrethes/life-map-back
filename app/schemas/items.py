from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.enums import ItemType, ItemStatus, AssetType

class LifeItemBase(BaseModel):
    name: str
    value: str
    type: ItemType
    status: ItemStatus
    categoryId: Optional[UUID] = None
    assetType: Optional[AssetType] = None
    lastUpdated: Optional[int] = None
    
    # Notification system
    notificationDismissed: Optional[bool] = None
    notificationLabel: Optional[str] = None
    
    # Finance sync
    syncBalanceWithBlock: Optional[bool] = None
    initialBalance: Optional[float] = None
    
    # Real estate specific
    rentAmount: Optional[float] = None
    rentDueDay: Optional[int] = Field(None, ge=1, le=31)
    address: Optional[str] = None
    city: Optional[str] = None
    postalCode: Optional[str] = None

class LifeItem(LifeItemBase):
    id: UUID

    class Config:
        from_attributes = True

class LifeItemCreate(LifeItemBase):
    pass

class LifeItemUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    type: Optional[ItemType] = None
    status: Optional[ItemStatus] = None
    categoryId: Optional[UUID] = None
    assetType: Optional[AssetType] = None
    lastUpdated: Optional[int] = None
    
    # Notification system
    notificationDismissed: Optional[bool] = None
    notificationLabel: Optional[str] = None
    
    # Finance sync
    syncBalanceWithBlock: Optional[bool] = None
    initialBalance: Optional[float] = None
    
    # Real estate specific
    rentAmount: Optional[float] = None
    rentDueDay: Optional[int] = Field(None, ge=1, le=31)
    address: Optional[str] = None
    city: Optional[str] = None
    postalCode: Optional[str] = None
