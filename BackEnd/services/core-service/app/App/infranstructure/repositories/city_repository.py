from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import get_db
from fastapi import Depends,HTTPException,status
from App.domain.schemas.city_schema import (
    city_list
)
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.city_and_province import city
from App.infranstructure.repositories.province_repository import ProvinceRepository

class CityRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)],province_repository:Annotated[ProvinceRepository,Depends()]):
        self.db=db
        self.province_repository=province_repository
        
    def create_city(self,cityy:city):

        self.db.add(cityy)
        self.db.commit()
        self.db.refresh(cityy)
        return cityy
    
    
    def delete_city(self,cityy:city):
        cityy.delete(synchronize_session=False)
        self.db.commit()
    
    def update_city(self,cityy:city,NewDetail:str):
        
        
        cityy.update({"city_name":NewDetail},synchronize_session=False)
        self.db.commit()
        return cityy.first()

    def get_city_id(self, city_id: UUID):
        cityy=self.db.query(city).filter(city.city_id==city_id)
        if not cityy.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" شهر با این شناسه موجود نیست")
        return cityy
        

    def get_city_name(self,name,province_id:UUID):
        city_name=self.db.query(city).filter(city.city_name==name,city.province_id==province_id)
        if city_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" شهر با این نام موجود است")
        
    def get_city_name_by_id(self,city_id:UUID):
        city_name=self.db.query(city).filter(city.city_id==city_id)
        if not city_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" شهر با این شناسه موجود نیست")
        return city_name.first()
    
    def get_city_id_by_name(self,name:str):
        city_name=self.db.query(city).filter(city.city_name==name)
        if not city_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" شهر با این نام موجود نیست")
        return city_name.first()
        
    def get_all_city(self,provincee_id:UUID):
        cities = self.db.query(city).filter(city.province_id==provincee_id)
        return [city_list(city_name=city.city_name,city_id=city.city_id) for city in cities]