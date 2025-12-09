from sqlalchemy import Column, String, BigInteger, Float, Boolean, ForeignKey, Enum as SqEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
from app.schemas.enums import HealthAppointmentType

class BodyMetric(Base):
    __tablename__ = "body_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    date = Column(BigInteger, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=True)
    bodyFat = Column("body_fat", Float, nullable=True)
    muscleMass = Column("muscle_mass", Float, nullable=True)
    note = Column(String, nullable=True)

class HealthAppointment(Base):
    __tablename__ = "health_appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    title = Column(String, nullable=False)
    date = Column(BigInteger, nullable=False)
    type = Column(SqEnum(HealthAppointmentType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    doctorName = Column("doctor_name", String, nullable=True)
    location = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    isCompleted = Column("is_completed", Boolean, default=False)
