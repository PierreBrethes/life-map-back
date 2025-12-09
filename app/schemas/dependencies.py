from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class DependencyBase(BaseModel):
    fromCategoryId: UUID
    fromItemId: UUID
    toCategoryId: UUID
    toItemId: UUID

class DependencyCreate(DependencyBase):
    pass

class DependencyUpdate(BaseModel):
    fromCategoryId: Optional[UUID] = None
    fromItemId: Optional[UUID] = None
    toCategoryId: Optional[UUID] = None
    toItemId: Optional[UUID] = None

class Dependency(DependencyBase):
    id: UUID

    class Config:
        from_attributes = True
