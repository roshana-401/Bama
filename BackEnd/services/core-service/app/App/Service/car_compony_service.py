from typing import Annotated
from fastapi import Depends, HTTPException, status
from App.domain.schemas.car_compony_schema import Add_car_compony
from App.domain.models.model_and_car_compony import car_compony
from App.infranstructure.repositories.car_compony_repository import CarComponyRepository
from App.Service.base_service import BaseService
from App.domain.schemas.car_compony_schema import (massage_car_compony,massage,get_car_compony_id)
from uuid import UUID

class CarComponyService(BaseService):
    def __init__(
        self,
        car_compony_repository: Annotated[CarComponyRepository, Depends()],
    ) -> None:
        super().__init__()

        self.car_compony_repository = car_compony_repository
        
    async def Add_car_compony(self,car:Add_car_compony):
        car=car_compony(
            car_compony_name=car.car_compony_name
        )
        car_save=self.car_compony_repository.create_car_compony(car=car)
        return massage_car_compony(massage="شرکت خودرو مورد نظر با موفقیت اضافه شد",car_compony_id=car_save.car_compony_id)

    async def delete_car_compony(self,car:UUID):
        car= self.car_compony_repository.get_car_compony_id(car)
        self.car_compony_repository.delete_car_compony(car=car)
        return massage(massage="شرکت خودرو مورد نظر با موفقیت حذف شد")
    
    async def update_car_compony(self,car_compony_id:UUID,newDetail:str):
        self.car_compony_repository.update_car_compony(car_compony_id=car_compony_id,NewDetail=newDetail)
        return massage(massage="شرکت خودرو مورد نظر با موفقیت بروز شد")
    
    async def get_all_car_compony(self):
        cars=self.car_compony_repository.get_all_car_compony()
        return cars
    
    async def get_car_compony_id(self,car_compony_name:str):
        cars=self.car_compony_repository.get_car_compony_id_by_name(car_compony_name)
        return get_car_compony_id(car_compony_id=cars.car_compony_id)