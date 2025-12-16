"""
Health tools for the LifeMap ADK Agent.

Async tools that directly call HealthService with database sessions.
"""
from typing import Optional
from agents.dependencies import get_async_session
from app.services.health_service import HealthService


def _serialize_metric(metric) -> dict:
    """Serialize a BodyMetric ORM object."""
    return {
        "id": str(metric.id),
        "item_id": str(metric.itemId) if metric.itemId else None,
        "date": metric.date,
        "weight": metric.weight,
        "height": metric.height,
        "body_fat": metric.bodyFat,
        "bmi": metric.bmi if hasattr(metric, 'bmi') else None,
    }


def _serialize_appointment(apt) -> dict:
    """Serialize a HealthAppointment ORM object."""
    return {
        "id": str(apt.id),
        "item_id": str(apt.itemId) if apt.itemId else None,
        "type": apt.type,
        "title": apt.title,
        "date": apt.date,
        "doctor_name": apt.doctorName if hasattr(apt, 'doctorName') else None,
        "location": apt.location if hasattr(apt, 'location') else None,
        "notes": apt.notes if hasattr(apt, 'notes') else None,
        "reminder_days": apt.reminderDays if hasattr(apt, 'reminderDays') else 7,
    }


# === BODY METRICS TOOLS ===

async def get_body_metrics(item_id: Optional[str] = None) -> dict:
    """
    Récupère les métriques corporelles.
    
    Args:
        item_id: Optionnel - filtrer par item santé
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = HealthService(session)
            uuid_filter = UUID(item_id) if item_id else None
            metrics = await service.get_metrics(item_id=uuid_filter)
            serialized = [_serialize_metric(m) for m in metrics]
            
            return {"status": "success", "count": len(serialized), "metrics": serialized}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def add_body_metric(
    item_id: str,
    date: int,
    weight: Optional[float] = None,
    height: Optional[float] = None,
    body_fat: Optional[float] = None
) -> dict:
    """
    Ajoute une mesure corporelle.
    
    Args:
        item_id: ID de l'item santé associé
        date: Date en timestamp milliseconds
        weight: Poids en kg (optionnel)
        height: Taille en cm (optionnel)
        body_fat: Masse grasse en % (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.health import BodyMetricCreate
        
        metric_data = BodyMetricCreate(
            itemId=UUID(item_id),
            date=date,
            weight=weight,
            height=height,
            bodyFat=body_fat,
        )
        
        async with get_async_session() as session:
            service = HealthService(session)
            metric = await service.create_metric(metric_data)
            
            return {"status": "success", "metric": _serialize_metric(metric)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def delete_body_metric(metric_id: str) -> dict:
    """
    Supprime une mesure corporelle.
    
    Args:
        metric_id: ID de la mesure à supprimer
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = HealthService(session)
            success = await service.delete_metric(UUID(metric_id))
            
            if not success:
                return {"status": "not_found", "message": f"Mesure {metric_id} non trouvée"}
            
            return {"status": "success", "message": f"Mesure {metric_id} supprimée"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# === HEALTH APPOINTMENTS TOOLS ===

async def get_health_appointments(item_id: Optional[str] = None) -> dict:
    """
    Récupère les rendez-vous santé.
    
    Args:
        item_id: Optionnel - filtrer par item santé
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = HealthService(session)
            uuid_filter = UUID(item_id) if item_id else None
            appointments = await service.get_appointments(item_id=uuid_filter)
            serialized = [_serialize_appointment(a) for a in appointments]
            
            return {"status": "success", "count": len(serialized), "appointments": serialized}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def create_health_appointment(
    item_id: str,
    appointment_type: str,
    title: str,
    date: int,
    doctor_name: Optional[str] = None,
    location: Optional[str] = None,
    notes: Optional[str] = None,
    reminder_days: int = 7
) -> dict:
    """
    Crée un rendez-vous santé.
    
    Args:
        item_id: ID de l'item santé associé
        appointment_type: Type de RDV ('dentist', 'gp', 'specialist', 'vaccine', etc)
        title: Titre du rendez-vous
        date: Date en timestamp milliseconds
        doctor_name: Nom du médecin (optionnel)
        location: Lieu (optionnel)
        notes: Notes (optionnel)
        reminder_days: Jours avant rappel (défaut: 7)
    """
    try:
        from uuid import UUID
        from app.schemas.health import HealthAppointmentCreate
        
        apt_data = HealthAppointmentCreate(
            itemId=UUID(item_id),
            type=appointment_type,
            title=title,
            date=date,
            doctorName=doctor_name,
            location=location,
            notes=notes,
            reminderDays=reminder_days,
        )
        
        async with get_async_session() as session:
            service = HealthService(session)
            apt = await service.create_appointment(apt_data)
            
            return {"status": "success", "appointment": _serialize_appointment(apt)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def update_health_appointment(
    appointment_id: str,
    title: Optional[str] = None,
    date: Optional[int] = None,
    doctor_name: Optional[str] = None,
    location: Optional[str] = None,
    notes: Optional[str] = None
) -> dict:
    """
    Met à jour un rendez-vous santé.
    
    Args:
        appointment_id: ID du rendez-vous
        title: Nouveau titre (optionnel)
        date: Nouvelle date (optionnel)
        doctor_name: Nouveau médecin (optionnel)
        location: Nouveau lieu (optionnel)
        notes: Nouvelles notes (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.health import HealthAppointmentUpdate
        
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if date is not None:
            update_data["date"] = date
        if doctor_name is not None:
            update_data["doctorName"] = doctor_name
        if location is not None:
            update_data["location"] = location
        if notes is not None:
            update_data["notes"] = notes
        
        if not update_data:
            return {"status": "error", "message": "Aucun champ à modifier fourni"}
        
        async with get_async_session() as session:
            service = HealthService(session)
            apt = await service.update_appointment(UUID(appointment_id), HealthAppointmentUpdate(**update_data))
            
            if not apt:
                return {"status": "not_found", "message": f"Rendez-vous {appointment_id} non trouvé"}
            
            return {"status": "success", "appointment": _serialize_appointment(apt)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def delete_health_appointment(appointment_id: str) -> dict:
    """
    Supprime un rendez-vous santé.
    
    Args:
        appointment_id: ID du rendez-vous à supprimer
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = HealthService(session)
            success = await service.delete_appointment(UUID(appointment_id))
            
            if not success:
                return {"status": "not_found", "message": f"Rendez-vous {appointment_id} non trouvé"}
            
            return {"status": "success", "message": f"Rendez-vous {appointment_id} supprimé"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
