from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.real_estate import PropertyValuation, EnergyConsumption, MaintenanceTask
from app.schemas.real_estate import (
    PropertyValuationCreate, PropertyValuationUpdate,
    EnergyConsumptionCreate, EnergyConsumptionUpdate,
    MaintenanceTaskCreate, MaintenanceTaskUpdate
)

class RealEstateService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Property Valuation
    async def get_valuations(self, item_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[PropertyValuation]:
        query = select(PropertyValuation).offset(skip).limit(limit)
        if item_id:
            query = query.filter(PropertyValuation.itemId == item_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_valuation(self, valuation_id: UUID) -> Optional[PropertyValuation]:
        return await self.db.get(PropertyValuation, valuation_id)

    async def create_valuation(self, valuation_in: PropertyValuationCreate) -> PropertyValuation:
        db_val = PropertyValuation(**valuation_in.model_dump())
        self.db.add(db_val)
        await self.db.commit()
        await self.db.refresh(db_val)
        return db_val

    async def update_valuation(self, valuation_id: UUID, valuation_in: PropertyValuationUpdate) -> Optional[PropertyValuation]:
        db_val = await self.get_valuation(valuation_id)
        if not db_val:
            return None
        
        update_data = valuation_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_val, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_val)
        return db_val

    async def delete_valuation(self, valuation_id: UUID) -> bool:
        db_val = await self.get_valuation(valuation_id)
        if not db_val:
            return False
        await self.db.delete(db_val)
        await self.db.commit()
        return True

    # Energy Consumption
    async def get_energy_records(self, item_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[EnergyConsumption]:
        query = select(EnergyConsumption).offset(skip).limit(limit)
        if item_id:
            query = query.filter(EnergyConsumption.itemId == item_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_energy_record(self, record_id: UUID) -> Optional[EnergyConsumption]:
        return await self.db.get(EnergyConsumption, record_id)

    async def create_energy_record(self, record_in: EnergyConsumptionCreate) -> EnergyConsumption:
        db_record = EnergyConsumption(**record_in.model_dump())
        self.db.add(db_record)
        await self.db.commit()
        await self.db.refresh(db_record)
        return db_record

    async def update_energy_record(self, record_id: UUID, record_in: EnergyConsumptionUpdate) -> Optional[EnergyConsumption]:
        db_record = await self.get_energy_record(record_id)
        if not db_record:
            return None
        
        update_data = record_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_record, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_record)
        return db_record

    async def delete_energy_record(self, record_id: UUID) -> bool:
        db_record = await self.get_energy_record(record_id)
        if not db_record:
            return False
        await self.db.delete(db_record)
        await self.db.commit()
        return True

    # Maintenance Tasks
    async def get_maintenance_tasks(self, item_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[MaintenanceTask]:
        query = select(MaintenanceTask).offset(skip).limit(limit)
        if item_id:
            query = query.filter(MaintenanceTask.itemId == item_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_maintenance_task(self, task_id: UUID) -> Optional[MaintenanceTask]:
        return await self.db.get(MaintenanceTask, task_id)

    async def create_maintenance_task(self, task_in: MaintenanceTaskCreate) -> MaintenanceTask:
        db_task = MaintenanceTask(**task_in.model_dump())
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def update_maintenance_task(self, task_id: UUID, task_in: MaintenanceTaskUpdate) -> Optional[MaintenanceTask]:
        db_task = await self.get_maintenance_task(task_id)
        if not db_task:
            return None
        
        update_data = task_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def delete_maintenance_task(self, task_id: UUID) -> bool:
        db_task = await self.get_maintenance_task(task_id)
        if not db_task:
            return False
        await self.db.delete(db_task)
        await self.db.commit()
        return True
