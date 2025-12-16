from sqlalchemy import Column, String, Float
from app.core.database import Base

class AssetConfig(Base):
    __tablename__ = "asset_configs"

    asset_type = Column(String, primary_key=True, index=True)
    glb_path = Column(String, nullable=False)
    
    scale = Column(Float, default=1.0, nullable=False)
    
    position_x = Column(Float, default=0.0, nullable=False)
    position_y = Column(Float, default=0.0, nullable=False)
    position_z = Column(Float, default=0.0, nullable=False)
    
    rotation_x = Column(Float, default=0.0, nullable=False)
    rotation_y = Column(Float, default=0.0, nullable=False)
    rotation_z = Column(Float, default=0.0, nullable=False)
    
    preview_scale = Column(Float, default=1.0, nullable=False)
