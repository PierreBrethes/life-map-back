from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.finance import (
    HistoryEntry, HistoryEntryCreate, HistoryEntryUpdate,
    Subscription, SubscriptionCreate, SubscriptionUpdate
)
from app.services.finance_service import FinanceService

router = APIRouter()

def get_finance_service(db: AsyncSession = Depends(get_db)) -> FinanceService:
    return FinanceService(db)

# History

@router.get("/history", response_model=List[HistoryEntry])
async def read_history(
    item_id: Optional[UUID] = Query(None, description="Filter by Item ID"),
    skip: int = 0,
    limit: int = 100,
    service: FinanceService = Depends(get_finance_service)
):
    return await service.get_history(item_id=item_id, skip=skip, limit=limit)

@router.post("/history", response_model=HistoryEntry, status_code=status.HTTP_201_CREATED)
async def create_history_entry(
    entry_in: HistoryEntryCreate,
    service: FinanceService = Depends(get_finance_service)
):
    return await service.create_history_entry(entry_in)

@router.get("/history/{entry_id}", response_model=HistoryEntry)
async def read_history_entry(
    entry_id: UUID,
    service: FinanceService = Depends(get_finance_service)
):
    entry = await service.get_history_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="History entry not found")
    return entry

@router.put("/history/{entry_id}", response_model=HistoryEntry)
async def update_history_entry(
    entry_id: UUID,
    entry_in: HistoryEntryUpdate,
    service: FinanceService = Depends(get_finance_service)
):
    entry = await service.update_history_entry(entry_id, entry_in)
    if not entry:
        raise HTTPException(status_code=404, detail="History entry not found")
    return entry

@router.delete("/history/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_history_entry(
    entry_id: UUID,
    service: FinanceService = Depends(get_finance_service)
):
    success = await service.delete_history_entry(entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="History entry not found")

# Subscriptions

@router.get("/subscriptions", response_model=List[Subscription])
async def read_subscriptions(
    item_id: Optional[UUID] = Query(None, description="Filter by Item ID"),
    skip: int = 0,
    limit: int = 100,
    service: FinanceService = Depends(get_finance_service)
):
    return await service.get_subscriptions(item_id=item_id, skip=skip, limit=limit)

@router.post("/subscriptions", response_model=Subscription, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription_in: SubscriptionCreate,
    service: FinanceService = Depends(get_finance_service)
):
    return await service.create_subscription(subscription_in)

@router.get("/subscriptions/{subscription_id}", response_model=Subscription)
async def read_subscription(
    subscription_id: UUID,
    service: FinanceService = Depends(get_finance_service)
):
    sub = await service.get_subscription(subscription_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub

@router.put("/subscriptions/{subscription_id}", response_model=Subscription)
async def update_subscription(
    subscription_id: UUID,
    subscription_in: SubscriptionUpdate,
    service: FinanceService = Depends(get_finance_service)
):
    sub = await service.update_subscription(subscription_id, subscription_in)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub

@router.delete("/subscriptions/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(
    subscription_id: UUID,
    service: FinanceService = Depends(get_finance_service)
):
    success = await service.delete_subscription(subscription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subscription not found")
