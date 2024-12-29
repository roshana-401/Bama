from typing import Annotated
from fastapi import Depends, HTTPException, status
from App.domain.models.sell_car import (car,SellCar)
from App.infranstructure.repositories.sell_car_repository import SellCarRepository
from App.infranstructure.repositories.car_repository import CarRepository
from App.infranstructure.repositories.user_repository import UserRepository
from App.infranstructure.repositories.city_repository import CityRepository
from App.infranstructure.repositories.model_car_repository import ModelCarRepository
from datetime import datetime
from App.Service.base_service import BaseService
from App.domain.schemas.sell_car_schema import (massage_sell_car,Add_sell_car,sell_car_form,massage,updata_sell_car,filter_data_sell_car)
from uuid import UUID

class SellCarService(BaseService):
    def __init__(
        self,
        sell_car_repository: Annotated[SellCarRepository, Depends()],
        car_repository:Annotated[CarRepository,Depends()],
        user_repository:Annotated[UserRepository,Depends()],
        city_repository:Annotated[CityRepository,Depends()],
        model_repository:Annotated[ModelCarRepository,Depends()],
        
    ) -> None:
        super().__init__()

        self.sell_car_repository = sell_car_repository
        self.car_repository = car_repository
        self.user_repository=user_repository
        self.city_repository=city_repository
        self.model_repository=model_repository
        
    async def Add_sell_car(self,sell_car:Add_sell_car):
        user=self.user_repository.get_user_by_id(sell_car.user_id)
        self.city_repository.get_city_id(sell_car.city_id)
        self.model_repository.get_model_car_id(sell_car.model_id)
        if sell_car.gearbox=='new':
            sell_car.KM=0
        carr=car(
            car_name=sell_car.car_name,
            model_id=sell_car.model_id,
            price=sell_car.price,
            color=sell_car.color,
            gearbox=sell_car.gearbox,
            KM=sell_car.KM,
            Operation=sell_car.Operation,
            year=sell_car.year
        )
        car_save=self.car_repository.create_car(carr)
        sell_car=SellCar(
            phone_number=user.phone_number,
            user_id=sell_car.user_id,
            car_id=car_save.car_id,
            description=sell_car.description,
            city_id=sell_car.city_id,
            date_update=datetime.utcnow()
            
        )
        sell_car=self.sell_car_repository.create_sell_car(sell_car=sell_car)
        return massage_sell_car(massage=" آگهی مورد نظر با موفقیت اضافه شد",sell_car_id=sell_car.sell_car_id)

    async def get_sell_car_id(self,sell_car_id:UUID):
        sell_car=self.sell_car_repository.get_sell_car_id(sell_car_id=sell_car_id)
        
        return sell_car_form(
            phone_number=sell_car.phone_number,
            description=sell_car.description,
            dateUpdate=str(sell_car.date_update),
            dateCreate=str(sell_car.date_create),
            city_name=sell_car.city.city_name,
            province_name=sell_car.city.province.province_name,
            car_name=sell_car.car.car_name,
            color=sell_car.car.color,
            KM=sell_car.car.KM,
            year=sell_car.car.year,
            price=sell_car.car.price,
            gearbox=sell_car.car.gearbox,
            Operation=sell_car.car.Operation,
            model_name=sell_car.car.model.model_name,
            car_compony_name=sell_car.car.model.car_compony.car_compony_name
        )
    async def delete_sell_car_id(self,sell_car_id:UUID,user_id:UUID,role_id:int,role_Admin:int):
        sell_car=self.sell_car_repository.get_sell_car_id(sell_car_id)
        if role_id!=role_Admin and sell_car.user_id!=user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")
        
        self.sell_car_repository.delete_sell_car(sell_car=sell_car)
        carr=self.car_repository.get_car_id(sell_car.car_id)
        self.car_repository.delete_car(carr)
        return massage(massage="آگهی مورد نظر با موفقیت حذف شد")
    
    async def update_sell_car_id(self,sell_car_id:UUID,newDetail:updata_sell_car,user_id:UUID,role_id:int,role_Admin:int):
        sell_car=self.sell_car_repository.get_sell_car_id(sell_car_id)
        
        if role_id!=role_Admin and sell_car.user_id!=user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")
        
        if newDetail.model_id!=None:
            self.model_repository.get_model_car_id(newDetail.model_id)
        if newDetail.city_id!=None:
            self.city_repository.get_city_id(newDetail.city_id)
        self.car_repository.get_car_id(sell_car.car_id)
        
        self.sell_car_repository.update_sell_car(updated_sell_car=sell_car,NewDetail=newDetail)

        return massage(massage="آگهی مورد نظر با موفقیت بروزرسانی شد")
    
    async def get_sell_car_with_filter(self,filter_data:filter_data_sell_car):
        sells_car=self.sell_car_repository.get_all_sell_car(filter_data=filter_data)
        sells=[sell_car_form(
            phone_number=sell.phone_number,
            description=sell.description,
            dateUpdate=str(sell.date_update),
            dateCreate=str(sell.date_create),
            city_name=sell.city.city_name,
            province_name=sell.city.province.province_name,
            car_name=sell.car.car_name,
            color=sell.car.color,
            KM=sell.car.KM,
            year=sell.car.year,
            price=sell.car.price,
            gearbox=sell.car.gearbox,
            Operation=sell.car.Operation,
            model_name=sell.car.model.model_name,
            car_compony_name=sell.car.model.car_compony.car_compony_name
        )for sell in sells_car]
        return sells
   