from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict

from app.core.database import get_db as get_async_session
from app.models.asset_config import AssetConfig
from app.schemas.asset_config import AssetConfig as AssetConfigSchema, AssetConfigUpdate, FrontendAssetConfig, AssetConfigUpdateInput

router = APIRouter()

@router.get("/config", response_model=Dict[str, FrontendAssetConfig])
async def get_all_asset_configs(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(AssetConfig))
    configs = result.scalars().all()
    
    # Auto-seed if empty
    if not configs:
        default_configs = {
          "car": {"glb_path": "/models/car.glb", "scale": 0.02, "position_y": 0.3, "preview_scale": 0.9},
          "plane": {"glb_path": "/models/plane.glb", "scale": 0.75, "position_y": 0.6, "rotation_y": 1.57079632679, "preview_scale": 0.7},
          "motorbike": {"glb_path": "/models/motorcycle.glb", "scale": 0.1, "preview_scale": 1.0},
          "boat": {"glb_path": "/models/ship.glb", "scale": 0.7, "position_y": 0.7, "preview_scale": 1.0},
          "house": {"glb_path": "/models/house.glb", "scale": 1.2, "position_y": 0.8, "preview_scale": 0.7},
          "home": {"glb_path": "/models/house.glb", "scale": 1.2, "position_y": 0.8, "preview_scale": 0.7},
          "apartment": {"glb_path": "/models/building.glb", "scale": 0.85, "preview_scale": 0.5},
          "pet": {"glb_path": "/models/dog.glb", "scale": 0.5, "preview_scale": 2.0},
          "family": {"glb_path": "/models/character-explorer.glb", "scale": 0.6, "preview_scale": 1.0},
          "friends": {"glb_path": "/models/character-explorer.glb", "scale": 0.6, "preview_scale": 1.0},
          "people": {"glb_path": "/models/character-explorer.glb", "scale": 0.6, "preview_scale": 1.0}
        }
        
        new_configs = []
        for asset_type, data in default_configs.items():
            conf = AssetConfig(
                asset_type=asset_type,
                glb_path=data["glb_path"],
                scale=data["scale"],
                position_x=data.get("position_x", 0.0),
                position_y=data.get("position_y", 0.0),
                position_z=data.get("position_z", 0.0),
                rotation_x=data.get("rotation_x", 0.0),
                rotation_y=data.get("rotation_y", 0.0),
                rotation_z=data.get("rotation_z", 0.0),
                preview_scale=data["preview_scale"]
            )
            session.add(conf)
            new_configs.append(conf)
        
        await session.commit()
        configs = new_configs

    # Transform to Frontend Format
    frontend_map = {}
    for c in configs:
        frontend_map[c.asset_type] = FrontendAssetConfig(
            glbPath=c.glb_path,
            scale=c.scale,
            position=(c.position_x, c.position_y, c.position_z),
            rotation=(c.rotation_x, c.rotation_y, c.rotation_z),
            previewScale=c.preview_scale
        )
    return frontend_map

@router.put("/config/{asset_type}", response_model=FrontendAssetConfig)
async def update_asset_config(
    asset_type: str,
    updates: AssetConfigUpdateInput,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(AssetConfig).where(AssetConfig.asset_type == asset_type))
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(status_code=404, detail="Asset config not found")
    
    # Apply updates from nested structure to flat DB structure
    config.scale = updates.scale
    
    # Position
    config.position_x = updates.position[0]
    config.position_y = updates.position[1]
    config.position_z = updates.position[2]
    
    # Rotation
    config.rotation_x = updates.rotation[0]
    config.rotation_y = updates.rotation[1]
    config.rotation_z = updates.rotation[2]
    
    config.preview_scale = updates.previewScale
    
    await session.commit()
    await session.refresh(config)
    
    return FrontendAssetConfig(
        glbPath=config.glb_path,
        scale=config.scale,
        position=(config.position_x, config.position_y, config.position_z),
        rotation=(config.rotation_x, config.rotation_y, config.rotation_z),
        previewScale=config.preview_scale
    )
