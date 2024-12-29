from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import get_db
from fastapi import Depends,HTTPException,status
from App.domain.schemas.city_schema import (
    city_list
)
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.sell_car import car
import json
from App.infranstructure.repositories.province_repository import ProvinceRepository

class CarRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)]):
        self.db=db
        
        
    def create_car(self,carr:car):
        self.db.add(carr)
        self.db.commit()
        self.db.refresh(carr)
        return carr
    
    
    def delete_car(self,carr:car):
        carr.delete(synchronize_session=False)
        self.db.commit()
            
    def get_car_id(self, car_id: UUID):
        carr=self.db.query(car).filter(car.car_id==car_id)
        if not carr.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" آگهی ماشین با این شناسه موجود نیست")
        return carr  
    
    def update_car_id(self, car_id: UUID,data:json):
        
        self.db.query(car).filter(car.car_id==car_id).update(data,synchronize_session=False)
        self.db.commit()

    