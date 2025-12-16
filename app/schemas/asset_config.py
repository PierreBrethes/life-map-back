from pydantic import BaseModel
from typing import List, Tuple

class AssetConfigBase(BaseModel):
    asset_type: str
    glb_path: str
    scale: float
    position_x: float
    position_y: float
    position_z: float
    rotation_x: float
    rotation_y: float
    rotation_z: float
    preview_scale: float

class AssetConfigCreate(AssetConfigBase):
    pass

class AssetConfigUpdate(BaseModel):
    scale: float
    position_x: float
    position_y: float
    position_z: float
    rotation_x: float
    rotation_y: float
    rotation_z: float
    preview_scale: float

class AssetConfig(AssetConfigBase):
    class Config:
        from_attributes = True

# Helper to transform DB flat structure to Frontend nested structure
class FrontendAssetConfig(BaseModel):
    glbPath: str
    scale: float
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float]
    previewScale: float
