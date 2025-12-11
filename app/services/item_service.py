from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional

from app.models.item import LifeItem
from app.models.finance import HistoryEntry, Subscription, RecurringTransaction
from app.schemas.items import LifeItemCreate, LifeItemUpdate

class ItemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_items(self, skip: int = 0, limit: int = 100) -> List[LifeItem]:
        result = await self.db.execute(select(LifeItem).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_item(self, item_id: UUID) -> Optional[LifeItem]:
        return await self.db.get(LifeItem, item_id)

    async def create_item(self, item_in: LifeItemCreate) -> LifeItem:
        db_item = LifeItem(**item_in.model_dump())
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def update_item(self, item_id: UUID, item_in: LifeItemUpdate) -> Optional[LifeItem]:
        db_item = await self.get_item(item_id)
        if not db_item:
            return None
        
        update_data = item_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def delete_item(self, item_id: UUID) -> bool:
        db_item = await self.get_item(item_id)
        if not db_item:
            return False
        
        # Cascade delete related records
        await self.db.execute(delete(HistoryEntry).where(HistoryEntry.itemId == item_id))
        await self.db.execute(delete(Subscription).where(Subscription.itemId == item_id))
        await self.db.execute(delete(RecurringTransaction).where(RecurringTransaction.targetAccountId == item_id))
        
        # Delete the item itself
        await self.db.delete(db_item)
        await self.db.commit()
        return True

    async def update_widget_order(self, item_id: UUID, order: List[str]) -> Optional[LifeItem]:
        """Update the widget order for an item."""
        db_item = await self.get_item(item_id)
        if not db_item:
            return None
        
        db_item.widgetOrder = order if order else None
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item
