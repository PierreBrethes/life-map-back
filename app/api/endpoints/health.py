from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.health import (
    BodyMetric, BodyMetricCreate, BodyMetricUpdate,
    HealthAppointment, HealthAppointmentCreate, HealthAppointmentUpdate
)
from app.services.health_service import HealthService

router = APIRouter()

def get_health_service(db: AsyncSession = Depends(get_db)) -> HealthService:
    return HealthService(db)

# Body Metrics

@router.get("/body-metrics", response_model=List[BodyMetric])
async def read_metrics(
    item_id: Optional[UUID] = Query(None, description="Filter by Item ID"),
    skip: int = 0,
    limit: int = 100,
    service: HealthService = Depends(get_health_service)
):
    return await service.get_metrics(item_id=item_id, skip=skip, limit=limit)

@router.post("/body-metrics", response_model=BodyMetric, status_code=status.HTTP_201_CREATED)
async def create_metric(
    metric_in: BodyMetricCreate,
    service: HealthService = Depends(get_health_service)
):
    return await service.create_metric(metric_in)

@router.get("/body-metrics/{metric_id}", response_model=BodyMetric)
async def read_metric(
    metric_id: UUID,
    service: HealthService = Depends(get_health_service)
):
    metric = await service.get_metric(metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

@router.put("/body-metrics/{metric_id}", response_model=BodyMetric)
async def update_metric(
    metric_id: UUID,
    metric_in: BodyMetricUpdate,
    service: HealthService = Depends(get_health_service)
):
    metric = await service.update_metric(metric_id, metric_in)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

@router.delete("/body-metrics/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_metric(
    metric_id: UUID,
    service: HealthService = Depends(get_health_service)
):
    success = await service.delete_metric(metric_id)
    if not success:
        raise HTTPException(status_code=404, detail="Metric not found")

# Health Appointments

@router.get("/appointments", response_model=List[HealthAppointment])
async def read_appointments(
    item_id: Optional[UUID] = Query(None, description="Filter by Item ID"),
    skip: int = 0,
    limit: int = 100,
    service: HealthService = Depends(get_health_service)
):
    return await service.get_appointments(item_id=item_id, skip=skip, limit=limit)

@router.post("/appointments", response_model=HealthAppointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_in: HealthAppointmentCreate,
    service: HealthService = Depends(get_health_service)
):
    return await service.create_appointment(appointment_in)

@router.get("/appointments/{appointment_id}", response_model=HealthAppointment)
async def read_appointment(
    appointment_id: UUID,
    service: HealthService = Depends(get_health_service)
):
    appointment = await service.get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.put("/appointments/{appointment_id}", response_model=HealthAppointment)
async def update_appointment(
    appointment_id: UUID,
    appointment_in: HealthAppointmentUpdate,
    service: HealthService = Depends(get_health_service)
):
    appointment = await service.update_appointment(appointment_id, appointment_in)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: UUID,
    service: HealthService = Depends(get_health_service)
):
    success = await service.delete_appointment(appointment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found")
