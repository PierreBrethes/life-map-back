from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.health import BodyMetric, HealthAppointment
from app.schemas.health import BodyMetricCreate, BodyMetricUpdate, HealthAppointmentCreate, HealthAppointmentUpdate

class HealthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Body Metrics
    async def get_metrics(self, item_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[BodyMetric]:
        query = select(BodyMetric).offset(skip).limit(limit)
        if item_id:
            query = query.filter(BodyMetric.itemId == item_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_metric(self, metric_id: UUID) -> Optional[BodyMetric]:
        return await self.db.get(BodyMetric, metric_id)

    async def create_metric(self, metric_in: BodyMetricCreate) -> BodyMetric:
        db_metric = BodyMetric(**metric_in.model_dump())
        self.db.add(db_metric)
        await self.db.commit()
        await self.db.refresh(db_metric)
        return db_metric

    async def update_metric(self, metric_id: UUID, metric_in: BodyMetricUpdate) -> Optional[BodyMetric]:
        db_metric = await self.get_metric(metric_id)
        if not db_metric:
            return None
        
        update_data = metric_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_metric, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_metric)
        return db_metric

    async def delete_metric(self, metric_id: UUID) -> bool:
        db_metric = await self.get_metric(metric_id)
        if not db_metric:
            return False
        await self.db.delete(db_metric)
        await self.db.commit()
        return True

    # Health Appointments
    async def get_appointments(self, item_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[HealthAppointment]:
        query = select(HealthAppointment).offset(skip).limit(limit)
        if item_id:
            query = query.filter(HealthAppointment.itemId == item_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_appointment(self, appointment_id: UUID) -> Optional[HealthAppointment]:
        return await self.db.get(HealthAppointment, appointment_id)

    async def create_appointment(self, appointment_in: HealthAppointmentCreate) -> HealthAppointment:
        db_appointment = HealthAppointment(**appointment_in.model_dump())
        self.db.add(db_appointment)
        await self.db.commit()
        await self.db.refresh(db_appointment)
        return db_appointment

    async def update_appointment(self, appointment_id: UUID, appointment_in: HealthAppointmentUpdate) -> Optional[HealthAppointment]:
        db_appointment = await self.get_appointment(appointment_id)
        if not db_appointment:
            return None
        
        update_data = appointment_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_appointment, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_appointment)
        return db_appointment

    async def delete_appointment(self, appointment_id: UUID) -> bool:
        db_appointment = await self.get_appointment(appointment_id)
        if not db_appointment:
            return False
        await self.db.delete(db_appointment)
        await self.db.commit()
        return True
