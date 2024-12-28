from typing import Annotated
from fastapi import Depends, HTTPException, status
from App.domain.schemas.city_schema import (Add_city,massage_city,massage,city_id)
from App.domain.models.city_and_province import city
from App.infranstructure.repositories.city_repository import CityRepository
from App.Service.base_service import BaseService

from uuid import UUID

class CityService(BaseService):
    def __init__(
        self,
        city_repository: Annotated[CityRepository, Depends()],
    ) -> None:
        super().__init__()

        self.city_repository = city_repository
        
    async def Add_city(self,cityy:Add_city):
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
        self.city_repository.update_city(city_id=city_id,NewDetail=newDetail)
        return massage(massage=" شهر مورد نظر با موفقیت بروز شد")
    
    async def get_all_city(self,province_id:UUID):
        cities=self.city_repository.get_all_city(provincee_id=province_id)
        return cities
    
    async def get_city_id(self,city_name:str):
        city=self.city_repository.get_city_id_by_name(city_name)
        return city_id(city_id=city.city_id)