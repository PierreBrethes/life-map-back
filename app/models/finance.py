from sqlalchemy import Column, String, Integer, BigInteger, Float, Boolean, ForeignKey, Enum as SqEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
from app.schemas.enums import HistoryCategory

class HistoryEntry(Base):
    __tablename__ = "history_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id", ondelete="CASCADE"), nullable=False)
    date = Column(BigInteger, nullable=False)
    value = Column(Float, nullable=False)
    label = Column(String, nullable=False)
    category = Column(SqEnum(HistoryCategory, values_callable=lambda x: [e.value for e in x]), nullable=False)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    billingDay = Column("billing_day", Integer, nullable=False)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)
    isActive = Column("is_active", Boolean, default=True)

class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sourceType = Column("source_type", String, nullable=False)  # subscription, salary, rent, insurance, custom
    sourceItemId = Column("source_item_id", UUID(as_uuid=True), nullable=True)  # Optional link to existing item
    targetAccountId = Column("target_account_id", UUID(as_uuid=True), ForeignKey("life_items.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)  # Positive = income, negative = expense
    dayOfMonth = Column("day_of_month", Integer, nullable=False)  # 1-31
    label = Column(String, nullable=False)
    category = Column(String, nullable=False)  # income, expense, transfer
    icon = Column(String, nullable=True)  # Icon identifier
    color = Column(String, nullable=True)  # Color hex code
    isActive = Column("is_active", Boolean, default=True)
    startDate = Column("start_date", BigInteger, nullable=False)  # Timestamp ms
    endDate = Column("end_date", BigInteger, nullable=True)  # Optional end date
    lastProcessedDate = Column("last_processed_date", BigInteger, nullable=True)  # Last processed timestamp
    createdAt = Column("created_at", BigInteger, nullable=False)
    updatedAt = Column("updated_at", BigInteger, nullable=False)

