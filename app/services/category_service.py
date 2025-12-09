from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models.categories import Category
from app.schemas.categories import CategoryCreate, CategoryUpdate

class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        # Eager load items
        result = await self.db.execute(
            select(Category).options(selectinload(Category.items)).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_category(self, category_id: UUID) -> Optional[Category]:
        result = await self.db.execute(
            select(Category).options(selectinload(Category.items)).where(Category.id == category_id)
        )
        return result.scalars().first()

    async def create_category(self, category_in: CategoryCreate) -> Category:
        db_category = Category(**category_in.model_dump())
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        return db_category

    async def update_category(self, category_id: UUID, category_in: CategoryUpdate) -> Optional[Category]:
        # We need to fetch without eager loading if we just update simple fields, but to return consistent object we might as well load
        db_category = await self.get_category(category_id)
        if not db_category:
            return None
        
        update_data = category_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_category)
        return db_category

    async def delete_category(self, category_id: UUID) -> bool:
        # Note: Depending on cascade rules, items might be deleted or set to null
        db_category = await self.get_category(category_id)
        if not db_category:
            return False
        await self.db.delete(db_category)
        await self.db.commit()
        return True
