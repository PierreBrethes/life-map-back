"""
Category (Island) tools for the LifeMap ADK Agent.

Async tools that directly call services with database sessions.
"""
import logging
from typing import Optional
from agents.dependencies import get_async_session
from app.services.category_service import CategoryService

logger = logging.getLogger(__name__)


def _serialize_island(category) -> dict:
    """Serialize a Category ORM object to dict for agent response."""
    items = []
    if hasattr(category, 'items') and category.items:
        items = [
            {
                "id": str(item.id),
                "name": item.name,
                "value": item.value,
                "status": item.status,
                "asset_type": item.assetType,
            }
            for item in category.items
        ]
    
    return {
        "id": str(category.id),
        "name": category.name,
        "color": category.color,
        "icon": category.icon,
        "items_count": len(items),
        "items": items,
    }


# === PUBLIC TOOLS (Exposed to ADK Agent) ===

async def get_all_islands() -> dict:
    """
    Récupère toutes les îles (catégories) de l'utilisateur avec leurs items.
    Retourne une liste d'îles avec leurs blocs associés.
    """
    try:
        async with get_async_session() as session:
            service = CategoryService(session)
            categories = await service.get_categories()
            # Serialize islands but exclude full item list for efficiency
            islands = []
            for cat in categories:
                cat_dict = _serialize_island(cat)
                # Remove full items list to save tokens, keep count
                if "items" in cat_dict:
                    del cat_dict["items"]
                islands.append(cat_dict)
            
            return {
                "status": "success",
                "count": len(islands),
                "islands": islands,
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_island_by_name(island_name: str) -> dict:
    """
    Récupère une île spécifique par son nom.
    
    Args:
        island_name: Le nom de l'île à récupérer (ex: "Finance", "Santé", "Social")
    """
    try:
        async with get_async_session() as session:
            service = CategoryService(session)
            categories = await service.get_categories()
            
            # Find matching island by name (case-insensitive)
            for category in categories:
                if category.name.lower() == island_name.lower():
                    return {
                        "status": "success",
                        "island": _serialize_island(category),
                    }
            
            return {
                "status": "not_found",
                "message": f"Île '{island_name}' non trouvée",
                "available_islands": [cat.name for cat in categories],
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_island_by_id(island_id: str) -> dict:
    """
    Récupère une île spécifique par son ID.
    
    Args:
        island_id: L'identifiant UUID de l'île
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = CategoryService(session)
            category = await service.get_category(UUID(island_id))
            
            if not category:
                return {"status": "not_found", "message": f"Île {island_id} non trouvée"}
            
            return {"status": "success", "island": _serialize_island(category)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def create_island(
    name: str,
    color: str = "#3B82F6",
    icon: str = "circle"
) -> dict:
    """
    Crée une nouvelle île (catégorie).
    
    Args:
        name: Nom de l'île
        color: Couleur hex (défaut: bleu)
        icon: Nom de l'icône (défaut: circle)
    """
    try:
        from app.schemas.categories import CategoryCreate
        async with get_async_session() as session:
            service = CategoryService(session)
            category_data = CategoryCreate(name=name, color=color, icon=icon)
            logger.info(f"[TOOL] create_island called: name={name}, color={color}, icon={icon}")
            category = await service.create_category(category_data)
            
            logger.info(f"[TOOL] create_island SUCCESS: {category.name} (id={category.id})")
            return {"status": "success", "island": _serialize_island(category)}
    except Exception as e:
        logger.error(f"[TOOL] create_island ERROR: {e}")
        return {"status": "error", "message": str(e)}


async def update_island(
    island_id: str,
    name: Optional[str] = None,
    color: Optional[str] = None,
    icon: Optional[str] = None
) -> dict:
    """
    Met à jour une île existante.
    
    Args:
        island_id: ID de l'île à modifier
        name: Nouveau nom (optionnel)
        color: Nouvelle couleur hex (optionnel)
        icon: Nouvelle icône (optionnel)
    """
    try:
        from uuid import UUID
        from app.schemas.categories import CategoryUpdate
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if color is not None:
            update_data["color"] = color
        if icon is not None:
            update_data["icon"] = icon
        
        if not update_data:
            return {"status": "error", "message": "Aucun champ à modifier fourni"}
        
        async with get_async_session() as session:
            service = CategoryService(session)
            category = await service.update_category(UUID(island_id), CategoryUpdate(**update_data))
            
            if not category:
                return {"status": "not_found", "message": f"Île {island_id} non trouvée"}
            
            return {"status": "success", "island": _serialize_island(category)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def delete_island(island_id: str) -> dict:
    """
    Supprime une île et tous ses items.
    
    Args:
        island_id: ID de l'île à supprimer
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = CategoryService(session)
            success = await service.delete_category(UUID(island_id))
            
            if not success:
                return {"status": "not_found", "message": f"Île {island_id} non trouvée"}
            
            return {"status": "success", "message": f"Île {island_id} supprimée"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
