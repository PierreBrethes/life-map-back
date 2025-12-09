from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.schemas.enums import HealthAppointmentType

class BodyMetricBase(BaseModel):
    itemId: UUID
    date: int
    weight: float
    height: Optional[float] = None
    bodyFat: Optional[float] = None
    muscleMass: Optional[float] = None
    note: Optional[str] = None

class BodyMetricCreate(BodyMetricBase):
    pass

class BodyMetricUpdate(BaseModel):
    date: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bodyFat: Optional[float] = None
    muscleMass: Optional[float] = None
    note: Optional[str] = None

class BodyMetric(BodyMetricBase):
    id: UUID

    class Config:
        from_attributes = True

class HealthAppointmentBase(BaseModel):
    itemId: UUID
    title: str
    date: int
    type: HealthAppointmentType
    doctorName: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    isCompleted: bool = False

class HealthAppointmentCreate(HealthAppointmentBase):
    pass

class HealthAppointmentUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[int] = None
    type: Optional[HealthAppointmentType] = None
    doctorName: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    isCompleted: Optional[bool] = None

class HealthAppointment(HealthAppointmentBase):
    id: UUID

    class Config:
        from_attributes = True
