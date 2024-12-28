from sqlalchemy import Column, String, TIMESTAMP, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from App.core.db.database import get_Base_Class
Base=get_Base_Class()

class car_compony(Base):
    __tablename__="car_compony"
    car_compony_id = Column(UUID(as_uuid=True),primary_key=True,nullable=False,server_default=text("gen_random_uuid()"))
    car_compony_name=Column(String,nullable=False,unique=True)

class model(Base):
    __tablename__ = "model"

    model_id = Column(UUID(as_uuid=True),primary_key=True,nullable=False,server_default=text("gen_random_uuid()"))
    model_name = Column(String, unique=True, nullable=False)
    car_compony_id = Column(UUID(as_uuid=True), ForeignKey("car_compony.car_compony_id",ondelete="CASCADE"), nullable=False)
    car_compony=relationship("car_compony")
