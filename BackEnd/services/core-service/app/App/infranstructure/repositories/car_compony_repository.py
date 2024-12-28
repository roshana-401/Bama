
from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import get_db
from fastapi import Depends,HTTPException,status
from App.domain.schemas.car_compony_schema import (
    car_compony_list
)
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.model_and_car_compony import car_compony

class CarComponyRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)]):
        self.db=db
        
    def create_car_compony(self,car:car_compony):
        self.db.add(car)
        self.db.commit()
        self.db.refresh(car)
        return car
    
    
    def delete_car_compony(self,car:car_compony):
        car.delete(synchronize_session=False)
        self.db.commit()
    
    def update_car_compony(self,car_componyy:car_compony,NewDetail:str):
    
        car_componyy.update({"car_compony_name":NewDetail},synchronize_session=False)
        self.db.commit()
        return car_componyy.first()

    def get_car_compony_id(self, car_compony_id: UUID):
        car_componyy=self.db.query(car_compony).filter(car_compony.car_compony_id==car_compony_id)
        if not car_componyy.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="شرکت خودرویی با این شناسه موجود نیست")
        return car_componyy
        

    def get_car_compony_name(self,name):
        car_compony_name=self.db.query(car_compony).filter(car_compony.car_compony_name==name)
        if car_compony_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="شرکت خودرویی با این نام موجود است")
        
        
    def get_all_car_compony(self):
        cars = self.db.query(car_compony).all()
        return [car_compony_list.from_orm(car) for car in cars]
    
    def get_car_compony_name_by_id(self,id:UUID):
        car_compony_name=self.db.query(car_compony).filter(car_compony.car_compony_id==id)
        if not car_compony_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="شرکت خودرویی با این شناسه موجود نیست")
        return car_compony_name.first()
    
    def get_car_compony_id_by_name(self,name:str):
        car_compony_name=self.db.query(car_compony).filter(car_compony.car_compony_name==name)
        if not car_compony_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="شرکت خودرویی با این نام موجود نیست")
        return car_compony_name.first()