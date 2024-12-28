from typing import Annotated
from fastapi import Depends, HTTPException, status
from App.domain.schemas.model_car_schema import (Add_model_car,massage_model_car,massage,model_car_info)
from App.domain.models.model_and_car_compony import model
from App.infranstructure.repositories.model_car_repository import ModelCarRepository
from App.Service.base_service import BaseService

from uuid import UUID

class ModelCarService(BaseService):
    def __init__(
        self,
        model_car_repository: Annotated[ModelCarRepository, Depends()],
    ) -> None:
        super().__init__()

        self.model_car_repository = model_car_repository
        
    async def Add_model_car(self,model_car:Add_model_car):
        model_car=model(
            model_name=model_car.model_car_name,
            car_compony_id=model_car.car_compony_id
        )
        car_save=self.model_car_repository.create_model_car(model_car=model_car)
        return massage_model_car(massage="مدل خودرو مورد نظر با موفقیت اضافه شد",model_id=car_save.model_id)

    async def delete_model_car(self,model_car_id:UUID):
        car= self.model_car_repository.get_model_car_id(model_car_id=model_car_id)
        self.model_car_repository.delete_model_car(model_car=car)
        return massage(massage="مدل خودرو مورد نظر با موفقیت حذف شد")
    
    async def update_model_car(self,model_car_id:UUID,newDetail:str):
        self.model_car_repository.update_model_car(model_car_id=model_car_id,NewDetail=newDetail)
        return massage(massage="مدل خودرو مورد نظر با موفقیت بروز شد")
    
    async def get_all_model_compony(self,car_compony_id:UUID):
        cars=self.model_car_repository.get_all_model_car(car_compony_id=car_compony_id)
        return cars
    
    async def get_model_car_id(self,car_model_id:UUID):
        cars=self.model_car_repository.get_model_car_name_by_id(car_model_id)
        return model_car_info(car_compony_name=cars.car_compony.car_compony_name,model_car_name=cars.model_name)