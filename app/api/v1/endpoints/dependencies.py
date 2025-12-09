from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.dependencies import Dependency, DependencyCreate, DependencyUpdate
from app.services.dependency_service import DependencyService

router = APIRouter()

def get_dependency_service(db: AsyncSession = Depends(get_db)) -> DependencyService:
    return DependencyService(db)

@router.get("", response_model=List[Dependency])
async def read_dependencies(
    skip: int = 0,
    limit: int = 100,
    service: DependencyService = Depends(get_dependency_service)
):
    return await service.get_dependencies(skip=skip, limit=limit)

@router.post("", response_model=Dependency, status_code=status.HTTP_201_CREATED)
async def create_dependency(
    dep_in: DependencyCreate,
    service: DependencyService = Depends(get_dependency_service)
):
    return await service.create_dependency(dep_in)

@router.get("/{dep_id}", response_model=Dependency)
async def read_dependency(
    dep_id: UUID,
    service: DependencyService = Depends(get_dependency_service)
):
    dep = await service.get_dependency(dep_id)
    if not dep:
        raise HTTPException(status_code=404, detail="Dependency not found")
    return dep

@router.put("/{dep_id}", response_model=Dependency)
async def update_dependency(
    dep_id: UUID,
    dep_in: DependencyUpdate,
    service: DependencyService = Depends(get_dependency_service)
):
    dep = await service.update_dependency(dep_id, dep_in)
    if not dep:
        raise HTTPException(status_code=404, detail="Dependency not found")
    return dep

@router.delete("/{dep_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dependency(
    dep_id: UUID,
    service: DependencyService = Depends(get_dependency_service)
):
    success = await service.delete_dependency(dep_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dependency not found")
