from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True) # "Finance", "Health", etc.
    color = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    
    # Relationship to Items (One-to-Many)
    # Using string reference to avoid circular imports if possible, or we'll solve it in item.py
    items = relationship("LifeItem", back_populates="category", lazy="selectin")
