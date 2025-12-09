from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum as SqEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
from app.schemas.enums import HistoryCategory

class HistoryEntry(Base):
    __tablename__ = "history_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    date = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    label = Column(String, nullable=False)
    category = Column(SqEnum(HistoryCategory), nullable=False)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    billingDay = Column("billing_day", Integer, nullable=False)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)
    isActive = Column("is_active", Boolean, default=True)
