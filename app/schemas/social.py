from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.schemas.enums import SocialEventType

class SocialEventBase(BaseModel):
    itemId: UUID
    title: str
    date: int
    location: Optional[str] = None
    type: SocialEventType
    contactIds: Optional[List[UUID]] = None

class SocialEventCreate(SocialEventBase):
    pass

class SocialEventUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[int] = None
    location: Optional[str] = None
    type: Optional[SocialEventType] = None
    contactIds: Optional[List[UUID]] = None

class SocialEvent(SocialEventBase):
    id: UUID

    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    itemId: UUID
    name: str
    birthday: Optional[int] = None
    lastContactDate: Optional[int] = None
    contactFrequencyDays: Optional[int] = None
    avatar: Optional[str] = None
    notes: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    birthday: Optional[int] = None
    lastContactDate: Optional[int] = None
    contactFrequencyDays: Optional[int] = None
    avatar: Optional[str] = None
    notes: Optional[str] = None

class Contact(ContactBase):
    id: UUID

    class Config:
        from_attributes = True
