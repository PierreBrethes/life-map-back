from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.schemas.enums import MaintenanceUrgency

# --- Property Valuation ---

class PropertyValuationBase(BaseModel):
    itemId: UUID
    estimatedValue: float
    purchasePrice: float
    purchaseDate: int
    loanAmount: Optional[float] = None
    loanMonthlyPayment: Optional[float] = None
    loanInterestRate: Optional[float] = None
    loanStartDate: Optional[int] = None
    loanDurationMonths: Optional[int] = None
    capitalRepaid: Optional[float] = None

class PropertyValuationCreate(PropertyValuationBase):
    pass

class PropertyValuationUpdate(BaseModel):
    estimatedValue: Optional[float] = None
    purchasePrice: Optional[float] = None
    purchaseDate: Optional[int] = None
    loanAmount: Optional[float] = None
    loanMonthlyPayment: Optional[float] = None
    loanInterestRate: Optional[float] = None
    loanStartDate: Optional[int] = None
    loanDurationMonths: Optional[int] = None
    capitalRepaid: Optional[float] = None

class PropertyValuation(PropertyValuationBase):
    id: UUID

    class Config:
        from_attributes = True

# --- Energy Consumption ---

class EnergyConsumptionBase(BaseModel):
    itemId: UUID
    date: int
    electricityCost: float
    electricityKwh: Optional[float] = None
    gasCost: float
    gasM3: Optional[float] = None

class EnergyConsumptionCreate(EnergyConsumptionBase):
    pass

class EnergyConsumptionUpdate(BaseModel):
    date: Optional[int] = None
    electricityCost: Optional[float] = None
    electricityKwh: Optional[float] = None
    gasCost: Optional[float] = None
    gasM3: Optional[float] = None

class EnergyConsumption(EnergyConsumptionBase):
    id: UUID

    class Config:
        from_attributes = True

# --- Maintenance Task ---

class MaintenanceTaskBase(BaseModel):
    itemId: UUID
    title: str
    description: Optional[str] = None
    urgency: MaintenanceUrgency
    dueDate: Optional[int] = None
    estimatedCost: Optional[float] = None
    isCompleted: bool = False
    completedAt: Optional[int] = None
    createdAt: int

class MaintenanceTaskCreate(MaintenanceTaskBase):
    pass

class MaintenanceTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    urgency: Optional[MaintenanceUrgency] = None
    dueDate: Optional[int] = None
    estimatedCost: Optional[float] = None
    isCompleted: Optional[bool] = None
    completedAt: Optional[int] = None
    # createdAt typically not updated

class MaintenanceTask(MaintenanceTaskBase):
    id: UUID

    class Config:
        from_attributes = True
