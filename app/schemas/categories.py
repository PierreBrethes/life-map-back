from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.schemas.items import LifeItem

class CategoryBase(BaseModel):
    name: str # Renamed from 'category' to 'name' to match model, but we might need alias if frontend sends 'category'
    color: str
    icon: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None

class Category(CategoryBase):
    id: UUID
    items: List[LifeItem] = []

    class Config:
        from_attributes = True

class SelectionState(BaseModel):
    categoryName: str
    item: LifeItem

class SelectionState(BaseModel):
    categoryName: str
    item: LifeItem
