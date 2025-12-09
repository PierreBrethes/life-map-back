from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.enums import AlertSeverity
import time

class AlertBase(BaseModel):
    itemId: UUID
    name: str
    severity: AlertSeverity
    dueDate: Optional[int] = None
    isActive: bool = True
    createdAt: Optional[int] = Field(default_factory=lambda: int(time.time() * 1000))

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    name: Optional[str] = None
    severity: Optional[AlertSeverity] = None
    dueDate: Optional[int] = None
    isActive: Optional[bool] = None
    createdAt: Optional[int] = None # Generally shouldn't update creation time, but helpful for fixing data

class Alert(AlertBase):
    id: UUID

    class Config:
        from_attributes = True
