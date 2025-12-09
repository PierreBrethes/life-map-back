from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.finance import HistoryEntry, Subscription
from app.schemas.finance import HistoryEntryCreate, HistoryEntryUpdate, SubscriptionCreate, SubscriptionUpdate

class FinanceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # History Entries
    async def get_history(self, item_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[HistoryEntry]:
        query = select(HistoryEntry).offset(skip).limit(limit)
        if item_id:
            query = query.filter(HistoryEntry.itemId == item_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_history_entry(self, entry_id: UUID) -> Optional[HistoryEntry]:
        return await self.db.get(HistoryEntry, entry_id)

    async def create_history_entry(self, entry_in: HistoryEntryCreate) -> HistoryEntry:
        db_entry = HistoryEntry(**entry_in.model_dump())
        self.db.add(db_entry)
        await self.db.commit()
        await self.db.refresh(db_entry)
        return db_entry

    async def update_history_entry(self, entry_id: UUID, entry_in: HistoryEntryUpdate) -> Optional[HistoryEntry]:
        db_entry = await self.get_history_entry(entry_id)
        if not db_entry:
            return None
        
        update_data = entry_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_entry, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_entry)
        return db_entry

    async def delete_history_entry(self, entry_id: UUID) -> bool:
        db_entry = await self.get_history_entry(entry_id)
        if not db_entry:
            return False
        await self.db.delete(db_entry)
        await self.db.commit()
        return True

    # Subscriptions
    async def get_subscriptions(self, item_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[Subscription]:
        query = select(Subscription).offset(skip).limit(limit)
        if item_id:
            query = query.filter(Subscription.itemId == item_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_subscription(self, subscription_id: UUID) -> Optional[Subscription]:
        return await self.db.get(Subscription, subscription_id)

    async def create_subscription(self, subscription_in: SubscriptionCreate) -> Subscription:
        db_sub = Subscription(**subscription_in.model_dump())
        self.db.add(db_sub)
        await self.db.commit()
        await self.db.refresh(db_sub)
        return db_sub

    async def update_subscription(self, subscription_id: UUID, subscription_in: SubscriptionUpdate) -> Optional[Subscription]:
        db_sub = await self.get_subscription(subscription_id)
        if not db_sub:
            return None
        
        update_data = subscription_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_sub, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_sub)
        return db_sub

    async def delete_subscription(self, subscription_id: UUID) -> bool:
        db_sub = await self.get_subscription(subscription_id)
        if not db_sub:
            return False
        await self.db.delete(db_sub)
        await self.db.commit()
        return True
