from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.alerts import Alert, AlertCreate, AlertUpdate
from app.services.alert_service import AlertService

router = APIRouter()

def get_alert_service(db: AsyncSession = Depends(get_db)) -> AlertService:
    return AlertService(db)

@router.get("", response_model=List[Alert])
async def read_alerts(
    item_id: Optional[UUID] = Query(None, description="Filter by Item ID"),
    skip: int = 0,
    limit: int = 100,
    service: AlertService = Depends(get_alert_service)
):
    return await service.get_alerts(item_id=item_id, skip=skip, limit=limit)

@router.post("", response_model=Alert, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_in: AlertCreate,
    service: AlertService = Depends(get_alert_service)
):
    return await service.create_alert(alert_in)

@router.get("/{alert_id}", response_model=Alert)
async def read_alert(
    alert_id: UUID,
    service: AlertService = Depends(get_alert_service)
):
    alert = await service.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.put("/{alert_id}", response_model=Alert)
async def update_alert(
    alert_id: UUID,
    alert_in: AlertUpdate,
    service: AlertService = Depends(get_alert_service)
):
    alert = await service.update_alert(alert_id, alert_in)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: UUID,
    service: AlertService = Depends(get_alert_service)
):
    success = await service.delete_alert(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
