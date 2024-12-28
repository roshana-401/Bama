from sqlalchemy import Column, String, TIMESTAMP, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from .operation_status import OperationStatus
from ...core.db.database import get_Base_Class
from sqlalchemy.orm import relationship
Base=get_Base_Class()

class spareParts(Base):
    __tablename__="spare_parts"
    spare_parts_id=Column(UUID(as_uuid=True),primary_key=True,nullable=False,server_default=text("gen_random_uuid()"))
    spare_parts_name=Column(String,nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey("model.model_id",ondelete="CASCADE"), nullable=False)
    price=Column(String, nullable=False)
    Operation=Column(Enum(OperationStatus), nullable=False)
    model=relationship("model")

class SellSpareParts(Base):
    __tablename__ = "Sell_spare_parts"

    sell_spare_parts_id=Column(UUID(as_uuid=True),primary_key=True,nullable=False,server_default=text("gen_random_uuid()"))
    phone_number = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    spare_parts_id = Column(UUID(as_uuid=True), ForeignKey("spare_parts.spare_parts_id",ondelete="CASCADE"), nullable=False)
    date_create = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    description=Column(String, nullable=True)
    city_id=Column(UUID(as_uuid=True), ForeignKey("ciry.city_id",ondelete="CASCADE"), nullable=False)
    date_update = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())
    
    spare_parts=relationship("spare_parts")
    city=relationship("city")