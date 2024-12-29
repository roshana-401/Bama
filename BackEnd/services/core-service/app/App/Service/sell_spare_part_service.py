from typing import Annotated
from fastapi import Depends, HTTPException, status
from App.domain.models.sell_spare_part import (spareParts,SellSpareParts)
from App.infranstructure.repositories.sell_spare_parts_repository import SellSparePartRepository
from App.infranstructure.repositories.spare_part_repository import SparePartRepository
from App.infranstructure.repositories.user_repository import UserRepository
from App.infranstructure.repositories.city_repository import CityRepository
from App.infranstructure.repositories.model_car_repository import ModelCarRepository
from datetime import datetime
from App.Service.base_service import BaseService
from App.domain.schemas.sell_spare_part import (massage_sell_spare_part,Add_sell_spare_part,sell_spare_part_form,massage,updata_sell_spare_part,filter_data_sell_spare_part)
from uuid import UUID

class SellSparePartService(BaseService):
    def __init__(
        self,
        sell_spare_part_repository: Annotated[SellSparePartRepository, Depends()],
        spare_part_repository:Annotated[SparePartRepository,Depends()],
        user_repository:Annotated[UserRepository,Depends()],
        city_repository:Annotated[CityRepository,Depends()],
        model_repository:Annotated[ModelCarRepository,Depends()],
        
    ) -> None:
        super().__init__()

        self.sell_spare_part_repository = sell_spare_part_repository
        self.spare_part_repository = spare_part_repository
        self.user_repository=user_repository
        self.city_repository=city_repository
        self.model_repository=model_repository
        
    async def Add_sell_spare_part(self,sell_spare_part:Add_sell_spare_part):
        user=self.user_repository.get_user_by_id(sell_spare_part.user_id)
        self.city_repository.get_city_id(sell_spare_part.city_id)
        self.model_repository.get_model_car_id(sell_spare_part.model_id)
        
        spare_part=spareParts(
            spare_parts_name=sell_spare_part.spare_part_name,
            model_id=sell_spare_part.model_id,
            price=sell_spare_part.price,
            Operation=sell_spare_part.Operation,
        )
        spare_part_save=self.spare_part_repository.create_spare_part(spare_part)
        
        sell_spare_part=SellSpareParts(
            phone_number=user.phone_number,
            user_id=sell_spare_part.user_id,
            spare_parts_id=spare_part_save.spare_parts_id,
            description=sell_spare_part.description,
            city_id=sell_spare_part.city_id,
            date_update=datetime.utcnow()
            
        )
        sell_spare_part=self.sell_spare_part_repository.create_sell_spare_part(sell_spare_part=sell_spare_part)
        return massage_sell_spare_part(massage=" آگهی مورد نظر با موفقیت اضافه شد",sell_spare_part_id=sell_spare_part.sell_spare_parts_id)

    async def get_sell_spare_part_id(self,sell_spare_part_id:UUID):
        sell_spare_part=self.sell_spare_part_repository.get_sell_spare_part_id(sell_spare_part_id=sell_spare_part_id)
        
        return sell_spare_part_form(
            phone_number=sell_spare_part.phone_number,
            description=sell_spare_part.description,
            dateUpdate=str(sell_spare_part.date_update),
            dateCreate=str(sell_spare_part.date_create),
            city_name=sell_spare_part.city.city_name,
            province_name=sell_spare_part.city.province.province_name,
            spare_part_name=sell_spare_part.spare_parts.spare_parts_name,
            price=sell_spare_part.spare_parts.price,
            Operation=sell_spare_part.spare_parts.Operation,
            model_name=sell_spare_part.spare_parts.model.model_name,
            car_compony_name=sell_spare_part.spare_parts.model.car_compony.car_compony_name
        )
        
    async def delete_sell_spare_part_id(self,sell_spare_part_id:UUID,user_id:UUID,role_id:int,role_Admin:int):
        sell_spare_part=self.sell_spare_part_repository.get_sell_spare_part_id(sell_spare_part_id=sell_spare_part_id)
        
        if role_id!=role_Admin and sell_spare_part.user_id!=user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="کاربر اجازه دسترسی ندارد")
        
        self.sell_spare_part_repository.delete_sell_spare_part(sell_spare_part=sell_spare_part)
        spare_part=self.spare_part_repository.get_spare_part_id(sell_spare_part.spare_parts_id)
        self.spare_part_repository.delete_spare_part(spare_part)
        return massage(massage="آگهی مورد نظر با موفقیت حذف شد")
    
    async def update_sell_spare_part_id(self,sell_spare_part_id:UUID,newDetail:updata_sell_spare_part,user_id:UUID,role_id:int,role_Admin:int):
        sell_spare_part=self.sell_spare_part_repository.get_sell_spare_part_id(sell_spare_part_id)
        
        if role_id!=role_Admin and sell_spare_part.user_id!=user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="کاربر اجازه دسترسی ندارد")
        
        if newDetail.model_id!=None:
            self.model_repository.get_model_car_id(newDetail.model_id)
        if newDetail.city_id!=None:
            self.city_repository.get_city_id(newDetail.city_id)
        self.spare_part_repository.get_spare_part_id(sell_spare_part.spare_parts_id)
        
        self.sell_spare_part_repository.update_sell_spare_part(updated_sell_spare_part=sell_spare_part,NewDetail=newDetail)

        return massage(massage="آگهی مورد نظر با موفقیت بروزرسانی شد")
    
    async def get_sell_spare_part_with_filter(self,filter_data:filter_data_sell_spare_part):
        sells_spare=self.sell_spare_part_repository.get_all_sell_spare_part(filter_data=filter_data)
        sells=[sell_spare_part_form(
            phone_number=sell.phone_number,
            description=sell.description,
            dateUpdate=str(sell.date_update),
            dateCreate=str(sell.date_create),
            city_name=sell.city.city_name,
            province_name=sell.city.province.province_name,
            spare_part_name=sell.spare_parts.spare_parts_name,
            price=sell.spare_parts.price,
            Operation=sell.spare_parts.Operation,
            model_name=sell.spare_parts.model.model_name,
            car_compony_name=sell.spare_parts.model.car_compony.car_compony_name
        )for sell in sells_spare]
        return sells
    
    async def get_sell_spare_part_id_for_check(self,sell_spare_part_id:UUID):
       return self.sell_spare_part_repository.get_sell_spare_part_id_and_check(sell_spare_part_id=sell_spare_part_id)
   