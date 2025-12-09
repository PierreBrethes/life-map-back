from typing import Optional
from pydantic import BaseModel

class UserSettingsBase(BaseModel):
    theme: str = "dark"
    notificationsEnabled: bool = True

class UserSettingsCreate(UserSettingsBase):
    pass

class UserSettingsUpdate(BaseModel):
    theme: Optional[str] = None
    notificationsEnabled: Optional[bool] = None

from uuid import UUID

class UserSettings(UserSettingsBase):
    id: UUID

    class Config:
        from_attributes = True
