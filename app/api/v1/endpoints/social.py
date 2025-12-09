from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.social import (
    SocialEvent, SocialEventCreate, SocialEventUpdate,
    Contact, ContactCreate, ContactUpdate
)
from app.services.social_service import SocialService

router = APIRouter()

def get_social_service(db: AsyncSession = Depends(get_db)) -> SocialService:
    return SocialService(db)

# Social Events

@router.get("/events", response_model=List[SocialEvent])
async def read_events(
    item_id: Optional[UUID] = Query(None, description="Filter by Item ID"),
    skip: int = 0,
    limit: int = 100,
    service: SocialService = Depends(get_social_service)
):
    return await service.get_events(item_id=item_id, skip=skip, limit=limit)

@router.post("/events", response_model=SocialEvent, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_in: SocialEventCreate,
    service: SocialService = Depends(get_social_service)
):
    return await service.create_event(event_in)

@router.get("/events/{event_id}", response_model=SocialEvent)
async def read_event(
    event_id: UUID,
    service: SocialService = Depends(get_social_service)
):
    event = await service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/events/{event_id}", response_model=SocialEvent)
async def update_event(
    event_id: UUID,
    event_in: SocialEventUpdate,
    service: SocialService = Depends(get_social_service)
):
    event = await service.update_event(event_id, event_in)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: UUID,
    service: SocialService = Depends(get_social_service)
):
    success = await service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")

# Contacts

@router.get("/contacts", response_model=List[Contact])
async def read_contacts(
    item_id: Optional[UUID] = Query(None, description="Filter by Item ID"),
    skip: int = 0,
    limit: int = 100,
    service: SocialService = Depends(get_social_service)
):
    return await service.get_contacts(item_id=item_id, skip=skip, limit=limit)

@router.post("/contacts", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_in: ContactCreate,
    service: SocialService = Depends(get_social_service)
):
    return await service.create_contact(contact_in)

@router.get("/contacts/{contact_id}", response_model=Contact)
async def read_contact(
    contact_id: UUID,
    service: SocialService = Depends(get_social_service)
):
    contact = await service.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/contacts/{contact_id}", response_model=Contact)
async def update_contact(
    contact_id: UUID,
    contact_in: ContactUpdate,
    service: SocialService = Depends(get_social_service)
):
    contact = await service.update_contact(contact_id, contact_in)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: UUID,
    service: SocialService = Depends(get_social_service)
):
    success = await service.delete_contact(contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
