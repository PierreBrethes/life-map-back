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
        "type": alert.type,
        "title": alert.title if hasattr(alert, 'title') else alert.name,
        "message": alert.message if hasattr(alert, 'message') else None,
        "due_date": alert.dueDate,
        "is_read": alert.isRead if hasattr(alert, 'isRead') else False,
        "priority": alert.priority if hasattr(alert, 'priority') else "medium",
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
    alert_type: str,
    title: str,
    due_date: int,
    message: Optional[str] = None,
    priority: str = "medium"
) -> dict:
    """
    Crée une nouvelle alerte.
    
    Args:
        item_id: ID de l'item associé
        alert_type: Type d'alerte ('insurance', 'maintenance', 'payment', 'expiry', 'custom')
        title: Titre de l'alerte
        due_date: Date d'échéance (timestamp ms)
        message: Message détaillé (optionnel)
        priority: Priorité ('low', 'medium', 'high')
    """
    try:
        from uuid import UUID
        from app.schemas.alerts import AlertCreate
        
        alert_data = AlertCreate(
            itemId=UUID(item_id),
            type=alert_type,
            name=title,
            dueDate=due_date,
            message=message,
            priority=priority,
            isRead=False,
        )
        
        async with get_async_session() as session:
            service = AlertService(session)
            alert = await service.create_alert(alert_data)
            
            return {"status": "success", "alert": _serialize_alert(alert)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def update_alert(
    alert_id: str,
    title: Optional[str] = None,
    message: Optional[str] = None,
    due_date: Optional[int] = None,
    is_read: Optional[bool] = None,
    priority: Optional[str] = None
) -> dict:
    """
    Met à jour une alerte.
    
    Args:
        alert_id: ID de l'alerte
        title: Nouveau titre (optionnel)
        message: Nouveau message (optionnel)
        due_date: Nouvelle date d'échéance (optionnel)
        is_read: Marquer comme lue/non lue (optionnel)
        priority: Nouvelle priorité (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.alerts import AlertUpdate
        
        update_data = {}
        if title is not None:
            update_data["name"] = title
        if message is not None:
            update_data["message"] = message
        if due_date is not None:
            update_data["dueDate"] = due_date
        if is_read is not None:
            update_data["isRead"] = is_read
        if priority is not None:
            update_data["priority"] = priority
        
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


async def mark_alert_as_read(alert_id: str) -> dict:
    """
    Marque une alerte comme lue.
    
    Args:
        alert_id: ID de l'alerte
    """
    return await update_alert(alert_id, is_read=True)


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
