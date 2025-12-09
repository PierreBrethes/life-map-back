from sqlalchemy import Column, String, BigInteger, Boolean, ForeignKey, Enum as SqEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
from app.schemas.enums import AlertSeverity

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    name = Column(String, nullable=False)
    severity = Column(SqEnum(AlertSeverity, values_callable=lambda x: [e.value for e in x]), nullable=False)
    dueDate = Column("due_date", BigInteger, nullable=True)
    isActive = Column("is_active", Boolean, default=True)
    createdAt = Column("created_at", BigInteger, nullable=False)
