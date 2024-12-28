from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import get_db
from fastapi import Depends,HTTPException,status
from App.domain.schemas.model_car_schema import (
    model_car_list
)
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.model_and_car_compony import model
from App.infranstructure.repositories.car_compony_repository import CarComponyRepository

class ModelCarRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)],car_compony:Annotated[CarComponyRepository,Depends()]):
        self.db=db
        self.car_compony=car_compony
        
    def create_model_car(self,model_car:model):
        self.get_model_car_name(model_car.model_name)
        self.car_compony.get_car_compony_id(model_car.car_compony_id)
        self.db.add(model_car)
        self.db.commit()
        self.db.refresh(model_car)
        return model_car
    
    
    def delete_model_car(self,model_car:model):
        model_car.delete(synchronize_session=False)
        self.db.commit()
    
    def update_model_car(self,model_car_id:UUID,NewDetail:str):
        
        updated_model_car=self.get_model_car_id(model_car_id=model_car_id)
        self.get_model_car_name(NewDetail)
        updated_model_car.update({"model_name":NewDetail},synchronize_session=False)
        self.db.commit()
        return updated_model_car.first()

    def get_model_car_id(self, model_car_id: UUID):
        model_car=self.db.query(model).filter(model.model_id==model_car_id)
        if not model_car.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="مدل خودرویی با این شناسه موجود نیست")
        return model_car
        

    def get_model_car_name(self,name):
        model_car_name=self.db.query(model).filter(model.model_name==name)
        if model_car_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="مدل خودرویی با این نام موجود است")
        
    def get_model_car_id_by_name(self,name):
        model_car_name=self.db.query(model).filter(model.model_name==name)
        if not model_car_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="مدل خودرویی با این شناسه موجود نیست")
        return model_car_name.first()
        
    def get_all_model_car(self,car_compony_id:UUID):
        self.car_compony.get_car_compony_id(car_compony_id=car_compony_id)
        cars_model = self.db.query(model).filter(model.car_compony_id==car_compony_id)
        return [model_car_list(model_car_name=car_model.model_name,model_id=car_model.model_id) for car_model in cars_model]