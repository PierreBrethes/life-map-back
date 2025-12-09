from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Dependency(Base):
    __tablename__ = "dependencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Source
    fromCategoryId = Column("from_category_id", UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    fromItemId = Column("from_item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    
    # Target
    toCategoryId = Column("to_category_id", UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    toItemId = Column("to_item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    
    # Optional edges can have metadata if we want later
