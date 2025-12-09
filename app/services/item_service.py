from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.item import LifeItem
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
        await self.db.delete(db_item)
        await self.db.commit()
        return True
