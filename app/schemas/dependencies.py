from typing import Optional
from pydantic import BaseModel

class DependencyBase(BaseModel):
    fromCategoryId: str
    fromItemId: str
    toCategoryId: str
    toItemId: str

class DependencyCreate(DependencyBase):
    pass

class DependencyUpdate(BaseModel):
    fromCategoryId: Optional[str] = None
    fromItemId: Optional[str] = None
    toCategoryId: Optional[str] = None
    toItemId: Optional[str] = None

class Dependency(DependencyBase):
    id: str

    class Config:
        from_attributes = True
