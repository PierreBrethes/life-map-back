from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.social import SocialEvent, Contact
from app.schemas.social import SocialEventCreate, SocialEventUpdate, ContactCreate, ContactUpdate

class SocialService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Social Events
    async def get_events(self, item_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[SocialEvent]:
        query = select(SocialEvent).offset(skip).limit(limit)
        if item_id:
            query = query.filter(SocialEvent.itemId == item_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_event(self, event_id: UUID) -> Optional[SocialEvent]:
        return await self.db.get(SocialEvent, event_id)

    async def create_event(self, event_in: SocialEventCreate) -> SocialEvent:
        db_event = SocialEvent(**event_in.model_dump())
        self.db.add(db_event)
        await self.db.commit()
        await self.db.refresh(db_event)
        return db_event

    async def update_event(self, event_id: UUID, event_in: SocialEventUpdate) -> Optional[SocialEvent]:
        db_event = await self.get_event(event_id)
        if not db_event:
            return None
        
        update_data = event_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_event, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_event)
        return db_event

    async def delete_event(self, event_id: UUID) -> bool:
        db_event = await self.get_event(event_id)
        if not db_event:
            return False
        await self.db.delete(db_event)
        await self.db.commit()
        return True

    # Contacts
    async def get_contacts(self, item_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[Contact]:
        query = select(Contact).offset(skip).limit(limit)
        if item_id:
            query = query.filter(Contact.itemId == item_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_contact(self, contact_id: UUID) -> Optional[Contact]:
        return await self.db.get(Contact, contact_id)

    async def create_contact(self, contact_in: ContactCreate) -> Contact:
        db_contact = Contact(**contact_in.model_dump())
        self.db.add(db_contact)
        await self.db.commit()
        await self.db.refresh(db_contact)
        return db_contact

    async def update_contact(self, contact_id: UUID, contact_in: ContactUpdate) -> Optional[Contact]:
        db_contact = await self.get_contact(contact_id)
        if not db_contact:
            return None
        
        update_data = contact_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_contact)
        return db_contact

    async def delete_contact(self, contact_id: UUID) -> bool:
        db_contact = await self.get_contact(contact_id)
        if not db_contact:
            return False
        await self.db.delete(db_contact)
        await self.db.commit()
        return True
