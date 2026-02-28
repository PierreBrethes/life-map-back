"""
Item tools for the LifeMap ADK Agent.

Async tools that directly call ItemService with database sessions.
"""
import logging
from typing import Optional
from agents.dependencies import get_async_session
from app.services.item_service import ItemService
from app.schemas.enums import ItemType, ItemStatus, AssetType
from app.schemas.items import LifeItemCreate, LifeItemUpdate
from uuid import UUID

logger = logging.getLogger(__name__)


def _serialize_item(item) -> dict:
    """Serialize a LifeItem ORM object to dict for agent response."""
    return {
        "id": str(item.id),
        "name": item.name,
        "value": item.value,
        "type": item.type.value if item.type else None,
        "status": item.status.value if item.status else None,
        "category_id": str(item.categoryId) if item.categoryId else None,
        "asset_type": item.assetType.value if item.assetType else None,
        "mileage": item.mileage,
        "last_updated": item.lastUpdated,
    }


# === PUBLIC TOOLS (Exposed to ADK Agent) ===

async def get_all_items() -> dict:
    """
    Récupère tous les items (blocs) de l'utilisateur.
    Retourne une liste de tous les items avec leurs détails.
    """
    try:
        async with get_async_session() as session:
            service = ItemService(session)
            items = await service.get_items()
            serialized = [_serialize_item(item) for item in items]
            
            return {"status": "success", "count": len(serialized), "items": serialized}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_item_by_id(item_id: str) -> dict:
    """
    Récupère un item spécifique par son ID.
    
    Args:
        item_id: L'identifiant UUID de l'item à récupérer
    """
    try:
        async with get_async_session() as session:
            service = ItemService(session)
            item = await service.get_item(UUID(item_id))
            
            if not item:
                return {"status": "not_found", "message": f"Item {item_id} non trouvé"}
            
            return {"status": "success", "item": _serialize_item(item)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def create_item(
    name: str,
    category_id: Optional[str] = None,
    category_name: Optional[str] = None,
    value: str = "",
    value_type: str = "text",
    status: str = "ok",
    asset_type: Optional[str] = None
) -> dict:
    """
    Crée un nouvel item (bloc) sur une île.
    
    Args:
        name: Nom de l'item
        category_id: ID de la catégorie (île) parent (Optionnel si category_name fourni)
        category_name: Nom de la catégorie (île) parent (ex: "Garage", "Immobilier")
        value: Valeur textuelle (défaut: "")
        value_type: Type de la valeur. Valeurs possibles : 'text', 'currency', 'percentage', 'date' (défaut: 'text')
        status: Statut de l'item. Valeurs possibles : 'ok', 'warning', 'critical' (défaut: 'ok')
        asset_type: Type d'asset 3D optionnel. Choix possibles :
            - Véhicules : car, motorbike, boat, plane
            - Immo : house, apartment
            - Finance : current_account, savings, investments, debt, finance
            - Pro : job, freelance, tech
            - Santé : medical, sport, insurance, health
            - Social : family, friends, pet, people
            - Divers : nature, default
    """
    try:
        from app.services.category_service import CategoryService

        # --- COERCE strings to Enum types (ADK passes args as raw strings) ---
        try:
            resolved_value_type = ItemType(value_type) if value_type else ItemType.TEXT
        except ValueError:
            return {"status": "error", "message": f"Type de valeur inconnu: '{value_type}'. Valeurs valides: {[e.value for e in ItemType]}"}

        try:
            resolved_status = ItemStatus(status) if status else ItemStatus.OK
        except ValueError:
            return {"status": "error", "message": f"Statut inconnu: '{status}'. Valeurs valides: {[e.value for e in ItemStatus]}"}

        resolved_asset_type = None
        if asset_type:
            try:
                resolved_asset_type = AssetType(asset_type)
            except ValueError:
                return {"status": "error", "message": f"Asset type inconnu: '{asset_type}'. Valeurs valides: {[e.value for e in AssetType]}"}
        # --- END COERCE ---
        
        logger.info(f"[TOOL] create_item called: name={name}, category_id={category_id}, category_name={category_name}, asset_type={resolved_asset_type}, value_type={resolved_value_type}")
        
        async with get_async_session() as session:
            # Resolve Category ID if not provided
            target_category_id = None
            
            if category_id:
                target_category_id = UUID(category_id)
            elif category_name:
                cat_service = CategoryService(session)
                categories = await cat_service.get_categories()
                for cat in categories:
                    if cat.name.lower() == category_name.lower():
                        target_category_id = cat.id
                        break
                
                if not target_category_id:
                    return {
                        "status": "error", 
                        "message": f"Catégorie '{category_name}' introuvable. Créez-la d'abord avec create_island."
                    }
            else:
                return {"status": "error", "message": "Vous devez fournir category_id OU category_name"}

            item_data = LifeItemCreate(
                name=name,
                categoryId=target_category_id,
                type=resolved_value_type,
                status=resolved_status,
                value=value,
                assetType=resolved_asset_type,
            )
        
            service = ItemService(session)
            item = await service.create_item(item_data)
            
            logger.info(f"[TOOL] create_item SUCCESS: {item.name} (id={item.id})")
            return {"status": "success", "item": _serialize_item(item)}
    except Exception as e:
        logger.error(f"[TOOL] create_item ERROR: {e}")
        return {"status": "error", "message": str(e)}


async def update_item(
    item_id: str,
    name: Optional[str] = None,
    value: Optional[str] = None,
    status: Optional[ItemStatus] = None,
    mileage: Optional[int] = None
) -> dict:
    """
    Met à jour un item existant.
    
    Args:
        item_id: ID de l'item à modifier
        name: Nouveau nom (optionnel)
        value: Nouvelle valeur textuelle (optionnel)
        status: Nouveau statut ('ok', 'warning', 'critical') (optionnel)
        mileage: Nouveau kilométrage pour véhicules (optionnel)
    """
    try:
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if value is not None:
            update_data["value"] = value
        if status is not None:
            update_data["status"] = status
        if mileage is not None:
            update_data["mileage"] = mileage
        
        if not update_data:
            return {"status": "error", "message": "Aucun champ à modifier fourni"}
        
        async with get_async_session() as session:
            service = ItemService(session)
            item = await service.update_item(UUID(item_id), LifeItemUpdate(**update_data))
            
            if not item:
                return {"status": "not_found", "message": f"Item {item_id} non trouvé"}
            
            return {"status": "success", "item": _serialize_item(item)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def delete_item(item_id: str) -> dict:
    """
    Supprime un item.
    
    Args:
        item_id: ID de l'item à supprimer
    """
    try:
        async with get_async_session() as session:
            service = ItemService(session)
            success = await service.delete_item(UUID(item_id))
            
            if not success:
                return {"status": "not_found", "message": f"Item {item_id} non trouvé"}
            
            return {"status": "success", "message": f"Item {item_id} supprimé"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
