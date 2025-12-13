from typing import Optional, Literal
from uuid import UUID
from pydantic import BaseModel

# Link types matching the SQLAlchemy enum
LinkType = Literal["insurance", "subscription", "payment", "maintenance", "ownership", "other"]


class DependencyBase(BaseModel):
    fromCategoryId: UUID
    fromItemId: UUID
    toCategoryId: UUID
    toItemId: UUID
    description: Optional[str] = None
    linkType: Optional[LinkType] = "other"
    linkedItemId: Optional[UUID] = None  # Reference to an existing item (e.g., insurance subscription)


class DependencyCreate(DependencyBase):
    pass


class DependencyUpdate(BaseModel):
    fromCategoryId: Optional[UUID] = None
    fromItemId: Optional[UUID] = None
    toCategoryId: Optional[UUID] = None
    toItemId: Optional[UUID] = None
    description: Optional[str] = None
    linkType: Optional[LinkType] = None
    linkedItemId: Optional[UUID] = None


class Dependency(DependencyBase):
    id: UUID

    class Config:
        from_attributes = True
