from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum as SqEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
from app.schemas.enums import AlertSeverity

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    name = Column(String, nullable=False)
    severity = Column(SqEnum(AlertSeverity), nullable=False)
    dueDate = Column("due_date", Integer, nullable=True)
    isActive = Column("is_active", Boolean, default=True)
    createdAt = Column("created_at", Integer, nullable=False)
