from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.alerts import Alert
from app.schemas.alerts import AlertCreate, AlertUpdate

class AlertService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_alerts(self, item_id: Optional[UUID] = None, skip: int = 0, limit: int = 100) -> List[Alert]:
        query = select(Alert).offset(skip).limit(limit)
        if item_id:
            query = query.filter(Alert.itemId == item_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_alert(self, alert_id: UUID) -> Optional[Alert]:
        return await self.db.get(Alert, alert_id)

    async def create_alert(self, alert_in: AlertCreate) -> Alert:
        db_alert = Alert(**alert_in.model_dump())
        self.db.add(db_alert)
        await self.db.commit()
        await self.db.refresh(db_alert)
        return db_alert

    async def update_alert(self, alert_id: UUID, alert_in: AlertUpdate) -> Optional[Alert]:
        db_alert = await self.get_alert(alert_id)
        if not db_alert:
            return None
        
        update_data = alert_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_alert, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_alert)
        return db_alert

    async def delete_alert(self, alert_id: UUID) -> bool:
        db_alert = await self.get_alert(alert_id)
        if not db_alert:
            return False
        await self.db.delete(db_alert)
        await self.db.commit()
        return True
