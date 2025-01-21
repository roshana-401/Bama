from sqlalchemy import Column, String, TIMESTAMP, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from ...core.db.database import get_Base_Class
from App.domain.models.user import users
from App.domain.models.sell_car import SellCar
from sqlalchemy.orm import relationship

Base=get_Base_Class()


class saveSellCar(Base):
    __tablename__="saveCar"
    user_id = Column(UUID(as_uuid=True),ForeignKey(users.user_id,ondelete="CASCADE"),primary_key=True, nullable=False)
    sell_car_id=Column(UUID(as_uuid=True),ForeignKey(SellCar.sell_car_id,ondelete="CASCADE"),primary_key=True,nullable=False)
    
    sellCar = relationship("SellCar", back_populates="save_cars")