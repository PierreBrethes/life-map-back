from sqlalchemy import Column, String, ForeignKey, Enum as SqEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base
from enum import Enum


class LinkType(str, Enum):
    INSURANCE = "insurance"
    SUBSCRIPTION = "subscription"
    PAYMENT = "payment"
    MAINTENANCE = "maintenance"
    OWNERSHIP = "ownership"
    OTHER = "other"


class Dependency(Base):
    __tablename__ = "dependencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Source
    fromCategoryId = Column("from_category_id", UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    fromItemId = Column("from_item_id", UUID(as_uuid=True), ForeignKey("life_items.id", ondelete="CASCADE"), nullable=False)
    
    # Target
    toCategoryId = Column("to_category_id", UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    toItemId = Column("to_item_id", UUID(as_uuid=True), ForeignKey("life_items.id", ondelete="CASCADE"), nullable=False)
    
    # Link metadata
    description = Column(String, nullable=True)  # "Car insurance", "Monthly debit", etc.
    linkType = Column(
        "link_type", 
        SqEnum(LinkType, values_callable=lambda x: [e.value for e in x]), 
        default=LinkType.OTHER, 
        nullable=True
    )
    
    # Optional: Link to an existing item that represents the connection (e.g., insurance subscription)
    linkedItemId = Column("linked_item_id", UUID(as_uuid=True), ForeignKey("life_items.id", ondelete="CASCADE"), nullable=True)
    linkedItem = relationship("LifeItem", foreign_keys=[linkedItemId])
