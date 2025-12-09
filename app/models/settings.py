from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    theme = Column(String, default="dark")
    notificationsEnabled = Column("notifications_enabled", Boolean, default=True)
