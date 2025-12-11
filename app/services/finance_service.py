import time
from datetime import datetime, timezone
from calendar import monthrange
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.finance import HistoryEntry, Subscription, RecurringTransaction
from app.schemas.finance import (
    HistoryEntryCreate, HistoryEntryUpdate, 
    SubscriptionCreate, SubscriptionUpdate,
    RecurringTransactionCreate, RecurringTransactionUpdate
)


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

    # Recurring Transactions
    async def get_recurring_transactions(self, account_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[RecurringTransaction]:
        query = select(RecurringTransaction).offset(skip).limit(limit)
        if account_id:
            query = query.filter(RecurringTransaction.targetAccountId == account_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_recurring_transaction(self, recurring_id: UUID) -> Optional[RecurringTransaction]:
        return await self.db.get(RecurringTransaction, recurring_id)

    async def create_recurring_transaction(self, recurring_in: RecurringTransactionCreate) -> RecurringTransaction:
        now = int(time.time() * 1000)
        db_recurring = RecurringTransaction(
            **recurring_in.model_dump(),
            createdAt=now,
            updatedAt=now
        )
        self.db.add(db_recurring)
        await self.db.commit()
        await self.db.refresh(db_recurring)
        return db_recurring

    async def update_recurring_transaction(self, recurring_id: UUID, recurring_in: RecurringTransactionUpdate) -> Optional[RecurringTransaction]:
        db_recurring = await self.get_recurring_transaction(recurring_id)
        if not db_recurring:
            return None
        
        update_data = recurring_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_recurring, key, value)
        db_recurring.updatedAt = int(time.time() * 1000)
        
        await self.db.commit()
        await self.db.refresh(db_recurring)
        return db_recurring

    async def delete_recurring_transaction(self, recurring_id: UUID) -> bool:
        db_recurring = await self.get_recurring_transaction(recurring_id)
        if not db_recurring:
            return False
        await self.db.delete(db_recurring)
        await self.db.commit()
        return True

    async def process_recurring_transactions(self) -> dict:
        """Process all active recurring transactions and create missing history entries."""
        now_ms = int(time.time() * 1000)
        today = datetime.now(timezone.utc)
        processed_count = 0
        errors = []
        
        # Get all active recurring transactions
        query = select(RecurringTransaction).filter(RecurringTransaction.isActive == True)
        result = await self.db.execute(query)
        recurring_transactions = result.scalars().all()
        
        for recurring in recurring_transactions:
            try:
                # Skip if end_date has passed
                if recurring.endDate and recurring.endDate < now_ms:
                    continue
                
                # Determine start point for processing
                if recurring.lastProcessedDate:
                    start_date = datetime.fromtimestamp(recurring.lastProcessedDate / 1000, tz=timezone.utc)
                else:
                    start_date = datetime.fromtimestamp(recurring.startDate / 1000, tz=timezone.utc)
                
                # Calculate months to process
                current_year = start_date.year
                current_month = start_date.month
                
                last_processed_timestamp = recurring.lastProcessedDate
                
                while True:
                    # Move to next month if we've already processed this month
                    if recurring.lastProcessedDate:
                        if current_month == 12:
                            current_month = 1
                            current_year += 1
                        else:
                            current_month += 1
                    
                    # Check if we've gone past current date
                    if current_year > today.year or (current_year == today.year and current_month > today.month):
                        break
                    
                    # Calculate the actual day (handle short months)
                    _, days_in_month = monthrange(current_year, current_month)
                    actual_day = min(recurring.dayOfMonth, days_in_month)
                    
                    # Create the target date
                    target_date = datetime(current_year, current_month, actual_day, tzinfo=timezone.utc)
                    target_timestamp = int(target_date.timestamp() * 1000)
                    
                    # Only create entry if the day has passed (or it's today but we allow same-day processing)
                    if target_date.date() < today.date():
                        # Create history entry
                        history_entry = HistoryEntry(
                            itemId=recurring.targetAccountId,
                            date=target_timestamp,
                            value=recurring.amount,
                            label=recurring.label,
                            category=recurring.category
                        )
                        self.db.add(history_entry)
                        last_processed_timestamp = target_timestamp
                        processed_count += 1
                    elif target_date.date() == today.date():
                        # Today's date - don't process, wait for next cycle
                        break
                    
                    # Safety: always increment for next iteration if lastProcessedDate was set
                    if not recurring.lastProcessedDate:
                        recurring.lastProcessedDate = recurring.startDate  # Mark as started
                        if current_month == 12:
                            current_month = 1
                            current_year += 1
                        else:
                            current_month += 1
                
                # Update last processed date
                if last_processed_timestamp and last_processed_timestamp != recurring.lastProcessedDate:
                    recurring.lastProcessedDate = last_processed_timestamp
                    recurring.updatedAt = now_ms
                
            except Exception as e:
                errors.append(f"Error processing recurring {recurring.id}: {str(e)}")
        
        await self.db.commit()
        return {"processedCount": processed_count, "errors": errors}

    async def migrate_subscriptions_to_recurring(self) -> dict:
        """Migrate existing Subscription records to RecurringTransaction."""
        
        now_ms = int(time.time() * 1000)
        migrated_count = 0
        skipped_count = 0
        errors = []
        
        # Get all subscriptions
        result = await self.db.execute(select(Subscription))
        subscriptions = result.scalars().all()
        
        for sub in subscriptions:
            try:
                # Check if already migrated (by looking for matching recurring with sourceItemId)
                existing = await self.db.execute(
                    select(RecurringTransaction).filter(
                        RecurringTransaction.sourceItemId == sub.id,
                        RecurringTransaction.sourceType == "subscription"
                    )
                )
                if existing.scalars().first():
                    skipped_count += 1
                    continue
                
                # Create RecurringTransaction from Subscription
                recurring = RecurringTransaction(
                    sourceType="subscription",
                    sourceItemId=sub.id,
                    targetAccountId=sub.itemId,
                    amount=-abs(sub.amount),  # Negative because expense
                    dayOfMonth=sub.billingDay,
                    label=sub.name,
                    category="expense",
                    icon=sub.icon,
                    color=sub.color,
                    isActive=sub.isActive,
                    startDate=now_ms,
                    endDate=None,
                    lastProcessedDate=None,
                    createdAt=now_ms,
                    updatedAt=now_ms
                )
                self.db.add(recurring)
                migrated_count += 1
                
            except Exception as e:
                errors.append(f"Error migrating subscription {sub.id}: {str(e)}")
        
        await self.db.commit()
        return {"migratedCount": migrated_count, "skippedCount": skipped_count, "errors": errors}
