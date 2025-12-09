from typing import List
from pydantic import BaseModel
from app.schemas.enums import WidgetType, AssetType

class WidgetConfig(BaseModel):
    type: WidgetType
    label: str
    icon: str
    applicableTo: List[AssetType]
