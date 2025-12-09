from typing import Optional
from pydantic import BaseModel
from app.schemas.enums import AlertSeverity

class AlertBase(BaseModel):
    itemId: str
    name: str
    severity: AlertSeverity
    dueDate: Optional[int] = None
    isActive: bool = True
    createdAt: int

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    name: Optional[str] = None
    severity: Optional[AlertSeverity] = None
    dueDate: Optional[int] = None
    isActive: Optional[bool] = None
    createdAt: Optional[int] = None # Generally shouldn't update creation time, but helpful for fixing data

class Alert(AlertBase):
    id: str

    class Config:
        from_attributes = True
