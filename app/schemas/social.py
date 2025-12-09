from typing import List, Optional
from pydantic import BaseModel
from app.schemas.enums import SocialEventType

class SocialEventBase(BaseModel):
    itemId: str
    title: str
    date: int
    location: Optional[str] = None
    type: SocialEventType
    contactIds: Optional[List[str]] = None

class SocialEventCreate(SocialEventBase):
    pass

class SocialEventUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[int] = None
    location: Optional[str] = None
    type: Optional[SocialEventType] = None
    contactIds: Optional[List[str]] = None

class SocialEvent(SocialEventBase):
    id: str

    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    itemId: str
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
    id: str

    class Config:
        from_attributes = True
