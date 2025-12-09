from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.dependencies import Dependency
from app.schemas.dependencies import DependencyCreate, DependencyUpdate

class DependencyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dependencies(self, skip: int = 0, limit: int = 100) -> List[Dependency]:
        result = await self.db.execute(select(Dependency).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_dependency(self, dependency_id: UUID) -> Optional[Dependency]:
        return await self.db.get(Dependency, dependency_id)

    async def create_dependency(self, dependency_in: DependencyCreate) -> Dependency:
        db_dep = Dependency(**dependency_in.model_dump())
        self.db.add(db_dep)
        await self.db.commit()
        await self.db.refresh(db_dep)
        return db_dep

    async def update_dependency(self, dependency_id: UUID, dependency_in: DependencyUpdate) -> Optional[Dependency]:
        db_dep = await self.get_dependency(dependency_id)
        if not db_dep:
            return None
        
        update_data = dependency_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_dep, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_dep)
        return db_dep

    async def delete_dependency(self, dependency_id: UUID) -> bool:
        db_dep = await self.get_dependency(dependency_id)
        if not db_dep:
            return False
        await self.db.delete(db_dep)
        await self.db.commit()
        return True
