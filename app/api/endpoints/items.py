from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.items import LifeItem, LifeItemCreate, LifeItemUpdate, WidgetOrderUpdate
from app.services.item_service import ItemService

router = APIRouter()

def get_item_service(db: AsyncSession = Depends(get_db)) -> ItemService:
    return ItemService(db)

@router.get("", response_model=List[LifeItem])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    service: ItemService = Depends(get_item_service)
):
    return await service.get_items(skip=skip, limit=limit)

@router.post("", response_model=LifeItem, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: LifeItemCreate,
    service: ItemService = Depends(get_item_service)
):
    return await service.create_item(item_in)

@router.get("/{item_id}", response_model=LifeItem)
async def read_item(
    item_id: UUID,
    service: ItemService = Depends(get_item_service)
):
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=LifeItem)
async def update_item(
    item_id: UUID,
    item_in: LifeItemUpdate,
    service: ItemService = Depends(get_item_service)
):
    item = await service.update_item(item_id, item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: UUID,
    service: ItemService = Depends(get_item_service)
):
    success = await service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")

@router.put("/{item_id}/widget-order", response_model=LifeItem)
async def update_widget_order(
    item_id: UUID,
    widget_order_in: WidgetOrderUpdate,
    service: ItemService = Depends(get_item_service)
):
    """Update the widget order for an item."""
    item = await service.update_widget_order(item_id, widget_order_in.order)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
