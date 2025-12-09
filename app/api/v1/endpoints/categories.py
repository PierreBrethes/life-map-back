from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.categories import Category, CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter()

def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(db)

@router.get("", response_model=List[Category])
async def read_categories(
    skip: int = 0,
    limit: int = 100,
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_categories(skip=skip, limit=limit)

@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    service: CategoryService = Depends(get_category_service)
):
    return await service.create_category(category_in)

@router.get("/{category_id}", response_model=Category)
async def read_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service)
):
    category = await service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: UUID,
    category_in: CategoryUpdate,
    service: CategoryService = Depends(get_category_service)
):
    category = await service.update_category(category_id, category_in)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service)
):
    success = await service.delete_category(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
