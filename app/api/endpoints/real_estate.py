from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.real_estate import (
    PropertyValuation, PropertyValuationCreate, PropertyValuationUpdate,
    EnergyConsumption, EnergyConsumptionCreate, EnergyConsumptionUpdate,
    MaintenanceTask, MaintenanceTaskCreate, MaintenanceTaskUpdate
)
from app.services.real_estate_service import RealEstateService

router = APIRouter()

def get_real_estate_service(db: AsyncSession = Depends(get_db)) -> RealEstateService:
    return RealEstateService(db)

# Property Valuations

@router.get("/valuations", response_model=List[PropertyValuation])
async def read_valuations(
    item_id: Optional[UUID] = Query(None, description="Filter by Item ID"),
    skip: int = 0,
    limit: int = 100,
    service: RealEstateService = Depends(get_real_estate_service)
):
    return await service.get_valuations(item_id=item_id, skip=skip, limit=limit)

@router.post("/valuations", response_model=PropertyValuation, status_code=status.HTTP_201_CREATED)
async def create_valuation(
    valuation_in: PropertyValuationCreate,
    service: RealEstateService = Depends(get_real_estate_service)
):
    return await service.create_valuation(valuation_in)

@router.get("/valuations/{valuation_id}", response_model=PropertyValuation)
async def read_valuation(
    valuation_id: UUID,
    service: RealEstateService = Depends(get_real_estate_service)
):
    val = await service.get_valuation(valuation_id)
    if not val:
        raise HTTPException(status_code=404, detail="Valuation not found")
    return val

@router.put("/valuations/{valuation_id}", response_model=PropertyValuation)
async def update_valuation(
    valuation_id: UUID,
    valuation_in: PropertyValuationUpdate,
    service: RealEstateService = Depends(get_real_estate_service)
):
    val = await service.update_valuation(valuation_id, valuation_in)
    if not val:
        raise HTTPException(status_code=404, detail="Valuation not found")
    return val

@router.delete("/valuations/{valuation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_valuation(
    valuation_id: UUID,
    service: RealEstateService = Depends(get_real_estate_service)
):
    success = await service.delete_valuation(valuation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Valuation not found")

# Energy Consumption

@router.get("/energy-consumption", response_model=List[EnergyConsumption])
async def read_energy_records(
    item_id: Optional[UUID] = Query(None, description="Filter by Item ID"),
    skip: int = 0,
    limit: int = 100,
    service: RealEstateService = Depends(get_real_estate_service)
):
    return await service.get_energy_records(item_id=item_id, skip=skip, limit=limit)

@router.post("/energy-consumption", response_model=EnergyConsumption, status_code=status.HTTP_201_CREATED)
async def create_energy_record(
    record_in: EnergyConsumptionCreate,
    service: RealEstateService = Depends(get_real_estate_service)
):
    return await service.create_energy_record(record_in)

@router.get("/energy-consumption/{record_id}", response_model=EnergyConsumption)
async def read_energy_record(
    record_id: UUID,
    service: RealEstateService = Depends(get_real_estate_service)
):
    record = await service.get_energy_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Energy record not found")
    return record

@router.put("/energy-consumption/{record_id}", response_model=EnergyConsumption)
async def update_energy_record(
    record_id: UUID,
    record_in: EnergyConsumptionUpdate,
    service: RealEstateService = Depends(get_real_estate_service)
):
    record = await service.update_energy_record(record_id, record_in)
    if not record:
        raise HTTPException(status_code=404, detail="Energy record not found")
    return record

@router.delete("/energy-consumption/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_energy_record(
    record_id: UUID,
    service: RealEstateService = Depends(get_real_estate_service)
):
    success = await service.delete_energy_record(record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Energy record not found")

# Maintenance Tasks

@router.get("/maintenance-tasks", response_model=List[MaintenanceTask])
async def read_maintenance_tasks(
    item_id: Optional[UUID] = Query(None, description="Filter by Item ID"),
    skip: int = 0,
    limit: int = 100,
    service: RealEstateService = Depends(get_real_estate_service)
):
    return await service.get_maintenance_tasks(item_id=item_id, skip=skip, limit=limit)

@router.post("/maintenance-tasks", response_model=MaintenanceTask, status_code=status.HTTP_201_CREATED)
async def create_maintenance_task(
    task_in: MaintenanceTaskCreate,
    service: RealEstateService = Depends(get_real_estate_service)
):
    return await service.create_maintenance_task(task_in)

@router.get("/maintenance-tasks/{task_id}", response_model=MaintenanceTask)
async def read_maintenance_task(
    task_id: UUID,
    service: RealEstateService = Depends(get_real_estate_service)
):
    task = await service.get_maintenance_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/maintenance-tasks/{task_id}", response_model=MaintenanceTask)
async def update_maintenance_task(
    task_id: UUID,
    task_in: MaintenanceTaskUpdate,
    service: RealEstateService = Depends(get_real_estate_service)
):
    task = await service.update_maintenance_task(task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/maintenance-tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_maintenance_task(
    task_id: UUID,
    service: RealEstateService = Depends(get_real_estate_service)
):
    success = await service.delete_maintenance_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
