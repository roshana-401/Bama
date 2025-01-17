from typing import Annotated
from fastapi import Depends, HTTPException, status
from App.domain.schemas.city_schema import (Add_city,massage_city,massage,city_info)
from App.domain.models.city_and_province import city
from App.infranstructure.repositories.city_repository import CityRepository
from App.infranstructure.repositories.province_repository import ProvinceRepository

from App.Service.base_service import BaseService

from uuid import UUID

class CityService(BaseService):
    def __init__(
        self,
        city_repository: Annotated[CityRepository, Depends()],
        province_repository: Annotated[ProvinceRepository, Depends()]
    ) -> None:
        super().__init__()

        self.city_repository = city_repository
        self.province_repository=province_repository
        
    async def Add_city(self,cityy:Add_city):
        self.province_repository.get_province_id(cityy.province_id)
        self.city_repository.get_city_name(cityy.city_name,cityy.province_id)
        cityy=city(
            city_name=cityy.city_name,
            province_id=cityy.province_id
        )
        city_save=self.city_repository.create_city(cityy=cityy)
        return massage_city(massage=" شهر مورد نظر با موفقیت اضافه شد",city_id=city_save.city_id)

    async def delete_city(self,city_id:UUID):
        city= self.city_repository.get_city_id(city_id=city_id)
        self.city_repository.delete_city(cityy=city)
        return massage(massage=" شهر مورد نظر با موفقیت حذف شد")
    
    async def update_city(self,city_id:UUID,newDetail:str):
        cityy=self.city_repository.get_city_id(city_id=city_id)
        self.city_repository.get_city_name(newDetail,cityy.first().province_id)
        
        self.city_repository.update_city(cityy=cityy,NewDetail=newDetail)
        return massage(massage=" شهر مورد نظر با موفقیت بروز شد")
    
    async def get_all_city(self,province_id:UUID):
        self.province_repository.get_province_id(province_id=province_id)
        cities=self.city_repository.get_all_city(provincee_id=province_id)
        return cities
    
    async def get_city_id(self,city_id:UUID):
        city=self.city_repository.get_city_name_by_id(city_id)
        return city_info(city_name=city.city_name,province_name=city.province.province_name)