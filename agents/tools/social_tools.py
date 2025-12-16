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
        "date": event.date,
        "location": event.location if hasattr(event, 'location') else None,
        "description": event.description if hasattr(event, 'description') else None,
        "participants": event.participants if hasattr(event, 'participants') else [],
    }


def _serialize_contact(contact) -> dict:
    """Serialize a Contact ORM object."""
    return {
        "id": str(contact.id),
        "item_id": str(contact.itemId) if contact.itemId else None,
        "name": contact.name,
        "relationship": contact.relationship if hasattr(contact, 'relationship') else None,
        "phone": contact.phone if hasattr(contact, 'phone') else None,
        "email": contact.email if hasattr(contact, 'email') else None,
        "birthday": contact.birthday if hasattr(contact, 'birthday') else None,
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
    date: int,
    location: Optional[str] = None,
    description: Optional[str] = None,
    participants: Optional[List[str]] = None
) -> dict:
    """
    Crée un événement social.
    
    Args:
        item_id: ID de l'item social associé
        title: Titre de l'événement
        date: Date en timestamp milliseconds
        location: Lieu (optionnel)
        description: Description (optionnel)
        participants: Liste des participants (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.social import SocialEventCreate
        
        event_data = SocialEventCreate(
            itemId=UUID(item_id),
            title=title,
            date=date,
            location=location,
            description=description,
            participants=participants or [],
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
    date: Optional[int] = None,
    location: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Met à jour un événement social.
    
    Args:
        event_id: ID de l'événement
        title: Nouveau titre (optionnel)
        date: Nouvelle date (optionnel)
        location: Nouveau lieu (optionnel)
        description: Nouvelle description (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.social import SocialEventUpdate
        
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if date is not None:
            update_data["date"] = date
        if location is not None:
            update_data["location"] = location
        if description is not None:
            update_data["description"] = description
        
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
    relationship: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    birthday: Optional[int] = None,
    notes: Optional[str] = None
) -> dict:
    """
    Crée un contact.
    
    Args:
        item_id: ID de l'item social associé
        name: Nom du contact
        relationship: Type de relation (ami, famille, collègue...)
        phone: Numéro de téléphone
        email: Email
        birthday: Date d'anniversaire (timestamp ms)
        notes: Notes
    """
    try:
        from uuid import UUID
        from app.schemas.social import ContactCreate
        
        contact_data = ContactCreate(
            itemId=UUID(item_id),
            name=name,
            relationship=relationship,
            phone=phone,
            email=email,
            birthday=birthday,
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
    relationship: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    notes: Optional[str] = None
) -> dict:
    """
    Met à jour un contact.
    
    Args:
        contact_id: ID du contact
        name: Nouveau nom (optionnel)
        relationship: Nouvelle relation (optionnel)
        phone: Nouveau téléphone (optionnel)
        email: Nouvel email (optionnel)
        notes: Nouvelles notes (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.social import ContactUpdate
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if relationship is not None:
            update_data["relationship"] = relationship
        if phone is not None:
            update_data["phone"] = phone
        if email is not None:
            update_data["email"] = email
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
