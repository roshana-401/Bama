from sqlalchemy import Column, String, TIMESTAMP, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from App.core.db.database import get_Base_Class
Base=get_Base_Class()

class province(Base):
    __tablename__="province"
    province_id = Column(UUID(as_uuid=True),primary_key=True,nullable=False,server_default=text("gen_random_uuid()"))
    province_name=Column(String,nullable=False,unique=True)

class city(Base):
    __tablename__ = "city"

    city_id = Column(UUID(as_uuid=True),primary_key=True,nullable=False,server_default=text("gen_random_uuid()"))
    city_name = Column(String, nullable=False)
    province_id = Column(UUID(as_uuid=True), ForeignKey("province.province_id",ondelete="CASCADE"), nullable=False)
    province=relationship("province")
    
    sell_cars = relationship("SellCar", back_populates="city")
    sell_spare_parts = relationship("SellSpareParts", back_populates="city")
