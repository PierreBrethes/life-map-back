from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum as SqEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base
from app.schemas.enums import ItemType, ItemStatus, AssetType

class LifeItem(Base):
    __tablename__ = "life_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    categoryId = Column("category_id", UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=True) # Nullable for now to ease migration, but should be required eventually
    
    name = Column(String, nullable=False)
    value = Column(String, nullable=True)
    
    # Relationship
    category = relationship("Category", back_populates="items")
    type = Column(SqEnum(ItemType), nullable=False)
    status = Column(SqEnum(ItemStatus), default=ItemStatus.OK)
    
    # Using camelCase attributes to match Pydantic schema, mapped to snake_case columns
    assetType = Column("asset_type", SqEnum(AssetType), nullable=True)
    lastUpdated = Column("last_updated", Integer, nullable=True)
    
    # Notification
    notificationDismissed = Column("notification_dismissed", Boolean, default=False)
    notificationLabel = Column("notification_label", String, nullable=True)
    
    # Finance
    syncBalanceWithBlock = Column("sync_balance_with_block", Boolean, default=False)
    initialBalance = Column("initial_balance", Float, nullable=True)
    
    # Real Estate
    rentAmount = Column("rent_amount", Float, nullable=True)
    rentDueDay = Column("rent_due_day", Integer, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    postalCode = Column("postal_code", String, nullable=True)
    
    # Garage/Vehicle
    mileage = Column(Integer, nullable=True)  # Current mileage in km
    
    # Widget customization
    widgetOrder = Column("widget_order", JSON, nullable=True, default=None)  # Array of widget type strings

