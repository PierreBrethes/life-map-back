from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum as SqEnum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from app.core.database import Base
from app.schemas.enums import SocialEventType

class SocialEvent(Base):
    __tablename__ = "social_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    title = Column(String, nullable=False)
    date = Column(Integer, nullable=False) # Timestamp
    location = Column(String, nullable=True)
    type = Column(SqEnum(SocialEventType), nullable=False)
    contactIds = Column("contact_ids", ARRAY(String), nullable=True) # List of UUIDs as strings or just strings

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id"), nullable=False)
    name = Column(String, nullable=False)
    birthday = Column(Integer, nullable=True)
    lastContactDate = Column("last_contact_date", Integer, nullable=True)
    contactFrequencyDays = Column("contact_frequency_days", Integer, nullable=True)
    avatar = Column(String, nullable=True)
    notes = Column(String, nullable=True)
