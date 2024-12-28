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

    # def create_city(self,cityy:city):
    #     self.get_city_name(cityy.city_name)
    #     self.province_repository.get_province_id(cityy.province_id)
    #     self.db.add(cityy)
    #     self.db.commit()
    #     self.db.refresh(cityy)
    #     return cityy
    
    
    # def delete_city(self,cityy:city):
    #     cityy.delete(synchronize_session=False)
    #     self.db.commit()
    
    # def update_city(self,city_id:UUID,NewDetail:str):
        
    #     updated_city=self.get_city_id(city_id=city_id)
    #     self.get_city_name(NewDetail)
    #     updated_city.update({"city_name":NewDetail},synchronize_session=False)
    #     self.db.commit()
    #     return updated_city.first()

    # def get_city_id(self, city_id: UUID):
    #     cityy=self.db.query(city).filter(city.city_id==city_id)
    #     if not cityy.first():
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" شهر با این شناسه موجود نیست")
    #     return cityy
        

    # def get_city_name(self,name):
    #     city_name=self.db.query(city).filter(city.city_name==name)
    #     if city_name.first():
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" شهر با این نام موجود است")
        
    # def get_city_name_by_id(self,city_id:UUID):
    #     city_name=self.db.query(city).filter(city.city_id==city_id)
    #     if not city_name.first():
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" شهر با این شناسه موجود نیست")
    #     return city_name.first()
    
    # def get_city_id_by_name(self,name:str):
    #     city_name=self.db.query(city).filter(city.city_name==name)
    #     if not city_name.first():
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" شهر با این نام موجود نیست")
    #     return city_name.first()
        
    # def get_all_city(self,provincee_id:UUID):
    #     self.province_repository.get_province_id(province_id=provincee_id)
    #     cities = self.db.query(city).filter(city.province_id==provincee_id)
    #     return [city_list(city_name=city.city_name,city_id=city.city_id) for city in cities]