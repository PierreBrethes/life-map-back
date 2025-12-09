from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.settings import UserSettings, UserSettingsUpdate
from app.services.settings_service import SettingsService

router = APIRouter()

def get_settings_service(db: AsyncSession = Depends(get_db)) -> SettingsService:
    return SettingsService(db)

@router.get("", response_model=UserSettings)
async def read_settings(
    service: SettingsService = Depends(get_settings_service)
):
    return await service.get_settings()

@router.put("", response_model=UserSettings)
async def update_settings(
    settings_in: UserSettingsUpdate,
    service: SettingsService = Depends(get_settings_service)
):
    return await service.update_settings(settings_in)
