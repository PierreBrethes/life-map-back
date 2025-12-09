from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum as SqEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
from app.schemas.enums import MaintenanceUrgency

class PropertyValuation(Base):
    __tablename__ = "property_valuations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    estimatedValue = Column("estimated_value", Float, nullable=False)
    purchasePrice = Column("purchase_price", Float, nullable=False)
    purchaseDate = Column("purchase_date", Integer, nullable=False)
    loanAmount = Column("loan_amount", Float, nullable=True)
    loanMonthlyPayment = Column("loan_monthly_payment", Float, nullable=True)
    loanInterestRate = Column("loan_interest_rate", Float, nullable=True)
    loanStartDate = Column("loan_start_date", Integer, nullable=True)
    loanDurationMonths = Column("loan_duration_months", Integer, nullable=True)
    capitalRepaid = Column("capital_repaid", Float, nullable=True)

class EnergyConsumption(Base):
    __tablename__ = "energy_consumption"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    date = Column(Integer, nullable=False)
    electricityCost = Column("electricity_cost", Float, nullable=False)
    electricityKwh = Column("electricity_kwh", Float, nullable=True)
    gasCost = Column("gas_cost", Float, nullable=False)
    gasM3 = Column("gas_m3", Float, nullable=True)

class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    urgency = Column(SqEnum(MaintenanceUrgency), nullable=False)
    dueDate = Column("due_date", Integer, nullable=True)
    estimatedCost = Column("estimated_cost", Float, nullable=True)
    isCompleted = Column("is_completed", Boolean, default=False)
    completedAt = Column("completed_at", Integer, nullable=True)
    createdAt = Column("created_at", Integer, nullable=False)
