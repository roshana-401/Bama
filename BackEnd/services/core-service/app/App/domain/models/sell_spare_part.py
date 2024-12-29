from sqlalchemy import Column, String, TIMESTAMP, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from .operation_status import OperationStatus
from ...core.db.database import get_Base_Class
from App.domain.models.city_and_province import city
from sqlalchemy.orm import relationship
Base=get_Base_Class()

class spareParts(Base):
    __tablename__="spare_parts"
    spare_parts_id=Column(UUID(as_uuid=True),primary_key=True,nullable=False,server_default=text("gen_random_uuid()"))
    spare_parts_name=Column(String,nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey("model.model_id",ondelete="CASCADE"), nullable=False)
    price=Column(String, nullable=False)
    Operation=Column(Enum(OperationStatus), nullable=False)
    model = relationship("model", back_populates="spareparts")
    sell_spare_parts = relationship("SellSpareParts", back_populates="spare_parts")
class SellSpareParts(Base):
    __tablename__ = "Sell_spare_parts"

    sell_spare_parts_id=Column(UUID(as_uuid=True),primary_key=True,nullable=False,server_default=text("gen_random_uuid()"))
    phone_number = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    spare_parts_id = Column(UUID(as_uuid=True), ForeignKey("spare_parts.spare_parts_id",ondelete="CASCADE"), nullable=False)
    date_create = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    description=Column(String, nullable=True)
    city_id=Column(UUID(as_uuid=True), ForeignKey(city.city_id,ondelete="CASCADE"), nullable=False)
    date_update = Column(TIMESTAMP(timezone=True), nullable=True)

    spare_parts=relationship("spareParts",back_populates="sell_spare_parts")
    city = relationship("city", back_populates="sell_spare_parts")