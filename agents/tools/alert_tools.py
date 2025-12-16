"""
Alert tools for the LifeMap ADK Agent.

Async tools that directly call AlertService with database sessions.
"""
import time
from typing import Optional
from agents.dependencies import get_async_session
from app.services.alert_service import AlertService


def _serialize_alert(alert) -> dict:
    """Serialize an Alert ORM object to dict for agent response."""
    return {
        "id": str(alert.id),
        "item_id": str(alert.itemId) if alert.itemId else None,
        "name": alert.name,
        "severity": alert.severity.value if alert.severity else None,
        "due_date": alert.dueDate,
        "is_active": alert.isActive if hasattr(alert, 'isActive') else True,
        "created_at": alert.createdAt if hasattr(alert, 'createdAt') else None,
    }


# === ALERT TOOLS ===

async def get_alerts(item_id: Optional[str] = None) -> dict:
    """
    Récupère toutes les alertes.
    
    Args:
        item_id: Optionnel - filtrer par item
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = AlertService(session)
            uuid_filter = UUID(item_id) if item_id else None
            alerts = await service.get_alerts(item_id=uuid_filter)
            serialized = [_serialize_alert(a) for a in alerts]
            
            return {"status": "success", "count": len(serialized), "alerts": serialized}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_alert_by_id(alert_id: str) -> dict:
    """
    Récupère une alerte spécifique.
    
    Args:
        alert_id: ID de l'alerte
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = AlertService(session)
            alert = await service.get_alert(UUID(alert_id))
            
            if not alert:
                return {"status": "not_found", "message": f"Alerte {alert_id} non trouvée"}
            
            return {"status": "success", "alert": _serialize_alert(alert)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def create_alert(
    item_id: str,
    name: str,
    severity: str,
    due_date: Optional[int] = None,
    is_active: bool = True
) -> dict:
    """
    Crée une nouvelle alerte.
    
    Args:
        item_id: ID de l'item associé
        name: Nom de l'alerte
        severity: Sévérité ('low', 'medium', 'high', 'critical')
        due_date: Date d'échéance (timestamp ms, optionnel)
        is_active: Si l'alerte est active (défaut: True)
    """
    try:
        from uuid import UUID
        from app.schemas.alerts import AlertCreate
        from app.schemas.enums import AlertSeverity
        
        alert_data = AlertCreate(
            itemId=UUID(item_id),
            name=name,
            severity=AlertSeverity(severity),
            dueDate=due_date,
            isActive=is_active,
        )
        
        async with get_async_session() as session:
            service = AlertService(session)
            alert = await service.create_alert(alert_data)
            
            return {"status": "success", "alert": _serialize_alert(alert)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def update_alert(
    alert_id: str,
    name: Optional[str] = None,
    severity: Optional[str] = None,
    due_date: Optional[int] = None,
    is_active: Optional[bool] = None
) -> dict:
    """
    Met à jour une alerte.
    
    Args:
        alert_id: ID de l'alerte
        name: Nouveau nom (optionnel)
        severity: Nouvelle sévérité (optionnel)
        due_date: Nouvelle date d'échéance (optionnel)
        is_active: Activer/désactiver l'alerte (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.alerts import AlertUpdate
        from app.schemas.enums import AlertSeverity
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if severity is not None:
            update_data["severity"] = AlertSeverity(severity)
        if due_date is not None:
            update_data["dueDate"] = due_date
        if is_active is not None:
            update_data["isActive"] = is_active
        
        if not update_data:
            return {"status": "error", "message": "Aucun champ à modifier fourni"}
        
        async with get_async_session() as session:
            service = AlertService(session)
            alert = await service.update_alert(UUID(alert_id), AlertUpdate(**update_data))
            
            if not alert:
                return {"status": "not_found", "message": f"Alerte {alert_id} non trouvée"}
            
            return {"status": "success", "alert": _serialize_alert(alert)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def deactivate_alert(alert_id: str) -> dict:
    """
    Désactive une alerte (la marque comme traitée).
    
    Args:
        alert_id: ID de l'alerte
    """
    return await update_alert(alert_id, is_active=False)


async def delete_alert(alert_id: str) -> dict:
    """
    Supprime une alerte.
    
    Args:
        alert_id: ID de l'alerte à supprimer
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = AlertService(session)
            success = await service.delete_alert(UUID(alert_id))
            
            if not success:
                return {"status": "not_found", "message": f"Alerte {alert_id} non trouvée"}
            
            return {"status": "success", "message": f"Alerte {alert_id} supprimée"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_upcoming_alerts(days: int = 30) -> dict:
    """
    Récupère les alertes à venir dans les prochains jours.
    
    Args:
        days: Nombre de jours à considérer (défaut: 30)
    """
    try:
        async with get_async_session() as session:
            service = AlertService(session)
            alerts = await service.get_alerts()
            
            now = int(time.time() * 1000)
            future_limit = now + (days * 24 * 60 * 60 * 1000)
            
            upcoming = []
            for alert in alerts:
                due_date = alert.dueDate
                if due_date and now <= due_date <= future_limit:
                    upcoming.append(_serialize_alert(alert))
            
            # Sort by due date
            upcoming.sort(key=lambda x: x.get("due_date", 0))
            
            return {
                "status": "success",
                "count": len(upcoming),
                "days_range": days,
                "alerts": upcoming,
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
