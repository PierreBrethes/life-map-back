"""
Social tools for the LifeMap ADK Agent.

Async tools that directly call SocialService with database sessions.
"""
from typing import List, Optional
from agents.dependencies import get_async_session
from app.services.social_service import SocialService


def _serialize_event(event) -> dict:
    """Serialize a SocialEvent ORM object."""
    return {
        "id": str(event.id),
        "item_id": str(event.itemId) if event.itemId else None,
        "title": event.title,
        "type": event.type.value if event.type else None,
        "date": event.date,
        "location": event.location if hasattr(event, 'location') else None,
        "contact_ids": event.contactIds if hasattr(event, 'contactIds') else [],
    }


def _serialize_contact(contact) -> dict:
    """Serialize a Contact ORM object."""
    return {
        "id": str(contact.id),
        "item_id": str(contact.itemId) if contact.itemId else None,
        "name": contact.name,
        "birthday": contact.birthday if hasattr(contact, 'birthday') else None,
        "last_contact_date": contact.lastContactDate if hasattr(contact, 'lastContactDate') else None,
        "contact_frequency_days": contact.contactFrequencyDays if hasattr(contact, 'contactFrequencyDays') else None,
        "avatar": contact.avatar if hasattr(contact, 'avatar') else None,
        "notes": contact.notes if hasattr(contact, 'notes') else None,
    }


# === SOCIAL EVENTS TOOLS ===

async def get_social_events(item_id: Optional[str] = None) -> dict:
    """
    Récupère les événements sociaux.
    
    Args:
        item_id: Optionnel - filtrer par item social
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = SocialService(session)
            uuid_filter = UUID(item_id) if item_id else None
            events = await service.get_events(item_id=uuid_filter)
            serialized = [_serialize_event(e) for e in events]
            
            return {"status": "success", "count": len(serialized), "events": serialized}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def create_social_event(
    item_id: str,
    title: str,
    event_type: str,
    date: int,
    location: Optional[str] = None,
    contact_ids: Optional[List[str]] = None
) -> dict:
    """
    Crée un événement social.
    
    Args:
        item_id: ID de l'item social associé
        title: Titre de l'événement
        event_type: Type d'événement (birthday, meeting, celebration, other)
        date: Date en timestamp milliseconds
        location: Lieu (optionnel)
        contact_ids: Liste des IDs de contacts (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.social import SocialEventCreate
        from app.schemas.enums import SocialEventType
        
        event_data = SocialEventCreate(
            itemId=UUID(item_id),
            title=title,
            type=SocialEventType(event_type),
            date=date,
            location=location,
            contactIds=[UUID(cid) for cid in contact_ids] if contact_ids else [],
        )
        
        async with get_async_session() as session:
            service = SocialService(session)
            event = await service.create_event(event_data)
            
            return {"status": "success", "event": _serialize_event(event)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def update_social_event(
    event_id: str,
    title: Optional[str] = None,
    event_type: Optional[str] = None,
    date: Optional[int] = None,
    location: Optional[str] = None,
    contact_ids: Optional[List[str]] = None
) -> dict:
    """
    Met à jour un événement social.
    
    Args:
        event_id: ID de l'événement
        title: Nouveau titre (optionnel)
        event_type: Nouveau type (optionnel)
        date: Nouvelle date (optionnel)
        location: Nouveau lieu (optionnel)
        contact_ids: Nouvelle liste de contacts (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.social import SocialEventUpdate
        from app.schemas.enums import SocialEventType
        
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if event_type is not None:
            update_data["type"] = SocialEventType(event_type)
        if date is not None:
            update_data["date"] = date
        if location is not None:
            update_data["location"] = location
        if contact_ids is not None:
            update_data["contactIds"] = [UUID(cid) for cid in contact_ids]
        
        if not update_data:
            return {"status": "error", "message": "Aucun champ à modifier fourni"}
        
        async with get_async_session() as session:
            service = SocialService(session)
            event = await service.update_event(UUID(event_id), SocialEventUpdate(**update_data))
            
            if not event:
                return {"status": "not_found", "message": f"Événement {event_id} non trouvé"}
            
            return {"status": "success", "event": _serialize_event(event)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def delete_social_event(event_id: str) -> dict:
    """
    Supprime un événement social.
    
    Args:
        event_id: ID de l'événement à supprimer
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = SocialService(session)
            success = await service.delete_event(UUID(event_id))
            
            if not success:
                return {"status": "not_found", "message": f"Événement {event_id} non trouvé"}
            
            return {"status": "success", "message": f"Événement {event_id} supprimé"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# === CONTACTS TOOLS ===

async def get_contacts(item_id: Optional[str] = None) -> dict:
    """
    Récupère les contacts.
    
    Args:
        item_id: Optionnel - filtrer par item social
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = SocialService(session)
            uuid_filter = UUID(item_id) if item_id else None
            contacts = await service.get_contacts(item_id=uuid_filter)
            serialized = [_serialize_contact(c) for c in contacts]
            
            return {"status": "success", "count": len(serialized), "contacts": serialized}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def create_contact(
    item_id: str,
    name: str,
    birthday: Optional[int] = None,
    last_contact_date: Optional[int] = None,
    contact_frequency_days: Optional[int] = None,
    notes: Optional[str] = None
) -> dict:
    """
    Crée un contact.
    
    Args:
        item_id: ID de l'item social associé
        name: Nom du contact
        birthday: Date d'anniversaire (timestamp ms)
        last_contact_date: Date du dernier contact (timestamp ms)
        contact_frequency_days: Fréquence de contact souhaitée en jours
        notes: Notes
    """
    try:
        from uuid import UUID
        from app.schemas.social import ContactCreate
        
        contact_data = ContactCreate(
            itemId=UUID(item_id),
            name=name,
            birthday=birthday,
            lastContactDate=last_contact_date,
            contactFrequencyDays=contact_frequency_days,
            notes=notes,
        )
        
        async with get_async_session() as session:
            service = SocialService(session)
            contact = await service.create_contact(contact_data)
            
            return {"status": "success", "contact": _serialize_contact(contact)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def update_contact(
    contact_id: str,
    name: Optional[str] = None,
    birthday: Optional[int] = None,
    last_contact_date: Optional[int] = None,
    contact_frequency_days: Optional[int] = None,
    notes: Optional[str] = None
) -> dict:
    """
    Met à jour un contact.
    
    Args:
        contact_id: ID du contact
        name: Nouveau nom (optionnel)
        birthday: Nouvelle date d'anniversaire (optionnel)
        last_contact_date: Nouvelle date de dernier contact (optionnel)
        contact_frequency_days: Nouvelle fréquence de contact (optionnel)
        notes: Nouvelles notes (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.social import ContactUpdate
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if birthday is not None:
            update_data["birthday"] = birthday
        if last_contact_date is not None:
            update_data["lastContactDate"] = last_contact_date
        if contact_frequency_days is not None:
            update_data["contactFrequencyDays"] = contact_frequency_days
        if notes is not None:
            update_data["notes"] = notes
        
        if not update_data:
            return {"status": "error", "message": "Aucun champ à modifier fourni"}
        
        async with get_async_session() as session:
            service = SocialService(session)
            contact = await service.update_contact(UUID(contact_id), ContactUpdate(**update_data))
            
            if not contact:
                return {"status": "not_found", "message": f"Contact {contact_id} non trouvé"}
            
            return {"status": "success", "contact": _serialize_contact(contact)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def delete_contact(contact_id: str) -> dict:
    """
    Supprime un contact.
    
    Args:
        contact_id: ID du contact à supprimer
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = SocialService(session)
            success = await service.delete_contact(UUID(contact_id))
            
            if not success:
                return {"status": "not_found", "message": f"Contact {contact_id} non trouvé"}
            
            return {"status": "success", "message": f"Contact {contact_id} supprimé"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
