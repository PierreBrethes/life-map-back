from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.models.settings import UserSettings
from app.schemas.settings import UserSettingsCreate, UserSettingsUpdate

class SettingsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_settings(self) -> UserSettings:
        # Get the first settings object or create default
        result = await self.db.execute(select(UserSettings).limit(1))
        settings = result.scalars().first()
        if not settings:
            settings = UserSettings(theme="dark", notificationsEnabled=True)
            self.db.add(settings)
            await self.db.commit()
            await self.db.refresh(settings)
        return settings

    async def update_settings(self, settings_in: UserSettingsUpdate) -> UserSettings:
        settings = await self.get_settings()
        
        update_data = settings_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(settings, key, value)
            
        await self.db.commit()
        await self.db.refresh(settings)
        return settings
