from sqlalchemy import Column, String, BigInteger, Integer, Float, Boolean, ForeignKey, Enum as SqEnum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from app.core.database import Base
from app.schemas.enums import SocialEventType

class SocialEvent(Base):
    __tablename__ = "social_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    date = Column(BigInteger, nullable=False) # Timestamp in milliseconds
    location = Column(String, nullable=True)
    type = Column(SqEnum(SocialEventType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    contactIds = Column("contact_ids", ARRAY(String), nullable=True)

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column("item_id", UUID(as_uuid=True), ForeignKey("life_items.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    birthday = Column(BigInteger, nullable=True)
    lastContactDate = Column("last_contact_date", BigInteger, nullable=True)
    contactFrequencyDays = Column("contact_frequency_days", Integer, nullable=True) # Keep as Integer - not a timestamp
    avatar = Column(String, nullable=True)
    notes = Column(String, nullable=True)
